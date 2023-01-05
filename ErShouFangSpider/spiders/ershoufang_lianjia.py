import json
import random
import re
import time

import scrapy

from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import Selector
from ..items import EsfLianjiaItem
from ..util import ua
from ..util.config import CONFIG_LJ

_header = {
    'User-Agent': ua.get_ua(),
    'Referer': 'https://sh.lianjia.com/ershoufang/'
}


class LianjiaErShowFangSpider(scrapy.Spider):
    # 名称
    name = 'esf_lianjia'
    # 允许域名
    allowed_domains = ['lianjia.com']

    def start_requests(self):
        start_url = CONFIG_LJ.LAST_URL
        if len(start_url) == 0:
            start_url = 'https://sh.lianjia.com/ershoufang/'
        yield scrapy.Request(url=start_url, headers=_header)

    def parse(self, response: HtmlResponse):
        CONFIG_LJ.LAST_URL = response.url
        CONFIG_LJ.save_config()
        # 爬取列表
        house_list = response.xpath('//*[@id="content"]/div[1]/ul/li')
        for item_selector in house_list:
            fang = self._parse_house_item(item_selector)
            if fang is None:
                continue
            yield fang
            # 抓取细节
            # yield scrapy.Request(url=fang['link'], headers=_get_headers(), callback=self._parse_house_detail)
        # 模拟翻页
        next_page = self._fake_next_page(response)
        if next_page is not None:
            yield next_page

    def _parse_house_item(self, selector: Selector) -> EsfLianjiaItem:
        fang = EsfLianjiaItem()
        fang['url'] = selector.xpath('div[1]/div[1]/a/@href').extract_first()
        if fang['url'] is None:
            return None
        fang['title'] = selector.xpath('div[1]/div[1]/a/text()').extract_first()
        fang['xiaoqu'] = selector.xpath('div[1]/div[2]/div/a[1]/text()').extract_first()
        fang['xiaoqu_url'] = selector.xpath('div[1]/div[2]/div/a[1]/@href').extract_first()
        fang['bankuai'] = selector.xpath('div[1]/div[2]/div/a[2]/text()').extract_first()
        fang['bankuai_url'] = selector.xpath('div[1]/div[2]/div/a[2]/@href').extract_first()
        fang['poster'] = selector.xpath('a/img[2]/@src').extract_first()
        # 2室2厅 | 87.78平米 | 南 | 精装 | 低楼层(共18层) | 2012年建 | 板楼
        house_info = selector.xpath('div[1]/div[3]/div/text()').extract_first().split('|')
        fang['house_huxing'] = house_info[0].strip() if len(house_info) > 0 else ''
        area: str = house_info[1].strip() if len(house_info) > 1 else ''
        fang['house_area'] = ''.join(re.findall(r"\d+.\d+", area))
        fang['house_chaoxiang'] = house_info[2].strip() if len(house_info) > 2 else ''
        fang['house_floor'] = house_info[4].strip() if len(house_info) > 4 else ''
        fang['house_create_time'] = house_info[5].strip() if len(house_info) > 5 else ''
        # 9人关注 / 1个月以前发布
        follow_info = selector.xpath('div[1]/div[4]/text()').extract_first().split('/')
        fang['follow_info'] = follow_info[0].strip() if len(follow_info) > 0 else ''
        fang['upload_time'] = follow_info[1].strip() if len(follow_info) > 1 else ''
        # 价格信息
        total_price = selector.xpath('div[1]/div[6]/div[1]').xpath('string(.)').extract_first()
        fang['total_price'] = ''.join(re.findall(r"\d+", total_price))
        unit_price: str = selector.xpath('div[1]/div[6]/div[2]/span/text()').extract_first()
        fang['unit_price'] = ''.join(re.findall(r"\d+", unit_price))
        return fang

    def _fake_next_page(self, response: HtmlResponse):
        try:
            page_data_str = response.xpath('//*[@id="content"]/div[1]/div[7]/div[2]/div').attrib['page-data']
            page_data = json.loads(page_data_str)
            cur_page = int(page_data['curPage'])
            url_page = 1
            re_find_list = re.findall(r"(\d+)", response.url)
            if len(re_find_list) > 0:
                url_page = int(re_find_list[0])
            next_page = max(cur_page, url_page) + 1
            total_page = int(page_data['totalPage'])
            _header['Referer'] = response.url
            if next_page <= total_page:
                time.sleep(random.uniform(1, 3))
                return scrapy.Request(url=f'https://sh.lianjia.com/ershoufang/pg{next_page}', headers=_header,
                                      callback=self.parse)
        except Exception as e:
            print('fake next page error!', e)
            return None

    def _parse_house_detail(self, response: HtmlResponse):
        pass
