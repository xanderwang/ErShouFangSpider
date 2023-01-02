# !/usr/bin/env python3
import json
import os.path

from . import path
from . import date


class LianJiaConfig(object):
    # 当前日期，用来保存不同时期的数据
    LAST_DATE = ""
    # 上一次的 URL
    LAST_URL = ""

    @staticmethod
    def load_config():
        config_file = os.path.join(path.ROOT_PATH, 'config', 'lianjia.json')
        if not os.path.exists(config_file):
            LianJiaConfig.LAST_DATE = date.get_date_string()
            return
        with open(config_file, "r") as file:
            config_dict: dict = json.load(file)
            LianJiaConfig.LAST_DATE = config_dict.get('last_date', '')
            if len(LianJiaConfig.LAST_DATE) == 0:
                LianJiaConfig.LAST_DATE = date.get_date_string()
            LianJiaConfig.LAST_URL = config_dict.get('last_url', '')

    @staticmethod
    def save_config():
        config_file = os.path.join(path.ROOT_PATH, 'config', 'lianjia.json')
        path.make_dir(config_file)
        with open(config_file, "w+") as file:
            json.dump({
                'last_date': LianJiaConfig.LAST_DATE,
                'last_url': LianJiaConfig.LAST_URL
            }, file)


LianJiaConfig.load_config()
