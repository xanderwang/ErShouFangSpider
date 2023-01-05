# !/usr/bin/env python3
import json
import os.path

from . import path
from . import date


class BaseConfig(object):

    def __init__(self):
        # 当前日期，用来保存不同时期的数据
        self.LAST_DATE = ""
        # 上一次的 URL
        self.LAST_URL = ""
        self._load_config()

    def _file_name(self) -> str:
        return 'base_config.json'

    def _set_last_date(self, last_date: str):
        self.LAST_DATE = last_date

    def _last_date(self) -> str:
        return self.LAST_DATE

    def _set_last_url(self, last_url: str):
        self.LAST_URL = last_url

    def _last_url(self) -> str:
        return self.LAST_URL

    def _load_config(self):
        config_file = os.path.join(path.ROOT_PATH, 'config', self._file_name())
        if not os.path.exists(config_file):
            self._set_last_date(date.get_date_string())
            return
        with open(config_file, "r") as file:
            config_dict: dict = json.load(file)
            self._set_last_date(config_dict.get('last_date', ''))
            if len(self._last_date()) == 0:
                self._set_last_date(date.get_date_string())
            self._set_last_url(config_dict.get('last_url', ''))

    def save_config(self):
        config_file = os.path.join(path.ROOT_PATH, 'config', self._file_name())
        path.make_dir(config_file)
        with open(config_file, "w+") as file:
            json.dump({
                'last_date': self._last_date(),
                'last_url': self._last_url()
            }, file)


class ConfigLianJia(BaseConfig):
    def _file_name(self) -> str:
        return "lianjia.json"


class Config5i5j(BaseConfig):
    def _file_name(self) -> str:
        return "5i5j.json"


CONFIG_LJ = ConfigLianJia()
CONFIG_5I5J = Config5i5j()


def test():
    print(CONFIG_LJ.LAST_DATE)
    print(CONFIG_LJ.LAST_URL)
    CONFIG_LJ.LAST_URL = "lianjia"
    CONFIG_LJ.save_config()
    print(CONFIG_LJ.LAST_DATE)
    print(CONFIG_LJ.LAST_URL)
    print(CONFIG_LJ.LAST_DATE)
    print(CONFIG_LJ.LAST_URL)
    CONFIG_5I5J.LAST_URL = "5i5j"
    CONFIG_5I5J.save_config()
    print(CONFIG_LJ.LAST_DATE)
    print(CONFIG_LJ.LAST_URL)


if __name__ == '__main__':
    test()
