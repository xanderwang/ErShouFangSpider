import codecs
import csv

from . import path


class BaseData(object):

    def _load_data(self):
        """加载数据"""
        pass

    def has_recoder(self):
        """是否有记录"""
        pass

    def insert_item(self, key: object, data: object):
        """插入数据"""
        pass


class CsvData(BaseData):

    def __init__(self, csv_file_path: str):
        self.recoder_key_list = None
        self.csv_writer = None
        self.csv_file = None
        self.csv_file_path = csv_file_path

    def _load_data(self):
        path.make_dir(self.csv_file_path)
        # a 表示追加, codecs 用于支持中文写入
        self.csv_file = codecs.open(self.csv_file_path, 'a', 'utf_8_sig')
        self.csv_writer = csv.writer(self.csv_file)
        self.recoder_key_list = []
        with codecs.open(self.csv_file_path, 'r', 'utf_8_sig') as csv_file:
            csv_reader = csv.reader(csv_file)
            csv_headers = next(csv_reader, "")
            if csv_headers is not None and csv_headers != "":
                for item in csv_reader:
                    self.recoder_key_list.append(item[0])

    def has_recoder(self):
        if self.csv_file is None:
            self._load_data()
        return len(self.recoder_key_list) > 0

    def insert_item(self, key: str, data: list):
        if self.csv_file is None:
            self._load_data()
        if key not in self.recoder_key_list:
            self.csv_writer.writerow(data)
            self.recoder_key_list.append(key)

    def __del__(self):
        if self.csv_file is not None:
            self.csv_file.close()
