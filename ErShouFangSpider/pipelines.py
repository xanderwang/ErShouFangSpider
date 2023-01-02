# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import csv
import json
import os.path

from .util import path
from .util.config import LianJiaConfig

from .items import ErShouFangItem

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ErShouFangPipeline:

    def __init__(self):
        self.csv_file_path = os.path.join(path.DATA_PATH, 'lianjia', f'{LianJiaConfig.LAST_DATE}.csv')
        path.make_dir(self.csv_file_path)
        # a 表示追加, codecs 用于支持中文写入
        self.cur_csv_file = codecs.open(self.csv_file_path, 'a', 'utf_8_sig')
        self.csv_writer = csv.writer(self.cur_csv_file)
        self.cur_url_list = []
        self._load_cur_csv()

    def _load_cur_csv(self):
        """加载当前的 csv """
        with codecs.open(self.csv_file_path, 'r', 'utf_8_sig') as csv_file:
            csv_reader = csv.reader(csv_file)
            headers = next(csv_reader)
            if headers is None:
                return
            for item in csv_reader:
                self.cur_url_list.append(item[0])

    def __del__(self):
        self.cur_csv_file.close()

    def process_item(self, item, spider):
        if isinstance(item, ErShouFangItem):
            fang: ErShouFangItem = item
            if len(self.cur_url_list) == 0:
                self.csv_writer.writerow(ErShouFangItem.csv_headers())
                self.cur_url_list.append('header')
            if fang['url'] not in self.cur_url_list:
                self.cur_url_list.append(fang['url'])
                self.csv_writer.writerow(fang.csv_row())
        return item
