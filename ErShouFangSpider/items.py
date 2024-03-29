# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from typing import List

import scrapy


class EsfLianjiaItem(scrapy.Item):
    # 链接
    url = scrapy.Field()
    # 名称：保利全南两房  满五 精装修 可拎包入住 诚意出售
    title = scrapy.Field()
    # 小区：保利湖畔阳光苑
    xiaoqu = scrapy.Field()
    # 小区链接：https://sh.lianjia.com/xiaoqu/5011000010990/
    xiaoqu_url = scrapy.Field()
    # 板块：嘉定新城
    bankuai = scrapy.Field()
    # 板块链接
    bankuai_url = scrapy.Field()
    # 封面
    poster = scrapy.Field()
    # 户型：2室2厅
    house_huxing = scrapy.Field()
    # 房间面积：
    house_area = scrapy.Field()
    # 朝向
    house_chaoxiang = scrapy.Field()
    # 房间楼层
    house_floor = scrapy.Field()
    # 房屋建造时间：
    house_create_time = scrapy.Field()
    # 热度：关注信息
    follow_info = scrapy.Field()
    # 发布时间
    upload_time = scrapy.Field()
    # 总价
    total_price = scrapy.Field()
    # 单价
    unit_price = scrapy.Field()

    @staticmethod
    def csv_headers() -> List[str]:
        return ['链接', '名称', '小区', '小区链接', '板块', '板块链接', '封面', '户型', '面积(平米)', '朝向', '楼层',
                '建造时间', '热度', '发布时间', '总价(万)', '单价(元)']

    def csv_row(self) -> List[str]:
        return [self['url'], self['title'], self['xiaoqu'], self['xiaoqu_url'], self['bankuai'], self['bankuai_url'],
                self['poster'], self['house_huxing'], self['house_area'], self['house_chaoxiang'], self['house_floor'],
                self['house_create_time'], self['follow_info'], self['upload_time'], self['total_price'],
                self['unit_price']]


class EsfLianjiaDetailItem(scrapy.Item):
    # 详细信息
    # define the fields for your item here like:
    # 链接
    link = scrapy.Field()
    # 名称
    title = scrapy.Field()
    # 封面
    poster = scrapy.Field()
    # 地理位置
    position = scrapy.Field()
    # 房间信息
    house = scrapy.Field()
    # 价格
    price = scrapy.Field()


class Esf5i5jItem(scrapy.Item):
    # 链接
    url = scrapy.Field()
    # 名称：保利全南两房  满五 精装修 可拎包入住 诚意出售
    title = scrapy.Field()
    # 小区：保利湖畔阳光苑
    xiaoqu = scrapy.Field()
    # 小区链接：https://sh.lianjia.com/xiaoqu/5011000010990/
    xiaoqu_url = scrapy.Field()
    # 板块：嘉定新城
    bankuai = scrapy.Field()
    # # 板块链接
    # bankuai_url = scrapy.Field()
    # 地段
    diduan = scrapy.Field()
    # 封面
    poster = scrapy.Field()
    # 户型：2室2厅
    house_huxing = scrapy.Field()
    # 房间面积：
    house_area = scrapy.Field()
    # 朝向
    house_chaoxiang = scrapy.Field()
    # 房间楼层
    house_floor = scrapy.Field()
    # 房屋建造时间：
    house_create_time = scrapy.Field()
    # 热度：关注信息
    follow_info = scrapy.Field()
    # 发布时间
    upload_time = scrapy.Field()
    # 总价
    total_price = scrapy.Field()
    # 单价
    unit_price = scrapy.Field()

    @staticmethod
    def csv_headers() -> List[str]:
        return ['链接', '名称', '小区', '小区链接', '板块', '地段', '封面', '户型', '面积(平米)', '朝向',
                '楼层', '建造时间', '热度', '发布时间', '总价(万)', '单价(元)']

    def csv_row(self) -> List[str]:
        return [self['url'], self['title'], self['xiaoqu'], self['xiaoqu_url'], self['bankuai'],
                self['diduan'], self['poster'], self['house_huxing'], self['house_area'], self['house_chaoxiang'],
                self['house_floor'], self['house_create_time'], self['follow_info'], self['upload_time'],
                self['total_price'], self['unit_price']]
