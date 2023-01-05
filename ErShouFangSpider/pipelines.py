# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os.path

from .util import path
from .util.config import CONFIG_LJ
from .util.config import CONFIG_5I5J

from .util.data import CsvData

from .items import EsfLianjiaItem
from .items import Esf5i5jItem

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ErShouFangPipeline:

    def __init__(self):
        file_path_lianjia = os.path.join(path.DATA_PATH, 'lianjia', f'{CONFIG_LJ.LAST_DATE}.csv')
        self.csv_lianjia = CsvData(file_path_lianjia)
        file_path_5i5j = os.path.join(path.DATA_PATH, '5i5j', f'{CONFIG_5I5J.LAST_DATE}.csv')
        self.csv_5i5j = CsvData(file_path_5i5j)

    def process_item(self, item, spider):
        if isinstance(item, EsfLianjiaItem):
            fang: EsfLianjiaItem = item
            if not self.csv_lianjia.has_recoder():
                self.csv_lianjia.insert_item('headers', EsfLianjiaItem.csv_headers())
            row_data = fang.csv_row()
            self.csv_lianjia.insert_item(row_data[0], row_data)
        elif isinstance(item, Esf5i5jItem):
            fang: Esf5i5jItem = item
            if not self.csv_5i5j.has_recoder():
                self.csv_5i5j.insert_item('headers', Esf5i5jItem.csv_headers())
            row_data = fang.csv_row()
            self.csv_5i5j.insert_item(row_data[0], row_data)
        return item
