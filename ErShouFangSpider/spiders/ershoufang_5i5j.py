import re

import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import Selector
from ..util import ua
from ..items import Esf5i5jItem

_header = {
    'User-Agent': ua.get_ua(),
}


class ErShouFang5i5jSpider(scrapy.Spider):
    name = 'esf_5i5j'
    allowed_domains = ['5i5j.com']

    def start_requests(self):
        start_url = ""
        if len(start_url) == 0:
            start_url = 'https://sh.5i5j.com/ershoufang/'
        yield scrapy.Request(url=start_url, headers=_header, dont_filter=True)

    def parse(self, response: HtmlResponse):
        # 尝试解析数据
        house_list = response.xpath('/html/body/div[6]/div[1]/div[2]/ul/li')
        for item in house_list:
            fang = self._parse_house_item(response, item)
            if fang is None:
                continue
            yield fang
        # 模拟翻页
        next_page = self._fake_next_page(response)
        if next_page is not None:
            yield next_page

    def _parse_house_item(self, response: HtmlResponse, selector: Selector):
        fang = Esf5i5jItem()
        fang['url'] = response.urljoin(selector.xpath('div[2]/h3/a/@href').extract_first().strip())
        if fang['url'] is None:
            return None
        fang['title'] = selector.xpath('div[2]/h3/a/text()').extract_first().strip()
        # 甘泉宜川 宜川一村 · 内环至中环 · 距中潭路地铁站-4口1373米（步行）
        location_info = selector.xpath('div[2]/div[1]/p[2]').xpath('string(.)').extract_first().split('·')
        fang['xiaoqu'] = selector.xpath('div[2]/div[1]/p[2]/a[1]/text()').extract_first().strip()
        fang['xiaoqu_url'] = response.urljoin(selector.xpath('div[2]/div[1]/p[2]/a[1]/@href').extract_first())
        fang['bankuai'] = selector.xpath('div[2]/div[1]/p[2]/text()').extract_first().strip()
        # fang['bankuai_url'] = selector.xpath('div[1]/div[2]/div/a[2]/@href').extract_first()
        diduan = location_info[2] if len(location_info) > 2 else ''
        fang['diduan'] = diduan.strip()
        fang['poster'] = selector.xpath('div[1]/a/img/@src').extract_first()
        # 1室1厅1卫 · 30.53 平米 · 南 · 低楼层/5层 · 简装
        house_info = selector.xpath('div[2]/div[1]/p[1]').xpath('string(.)').extract_first().split('·')
        fang['house_huxing'] = house_info[0].strip() if len(house_info) > 0 else ''
        area: str = house_info[1].strip() if len(house_info) > 1 else ''
        fang['house_area'] = ''.join(re.findall(r"\d+.\d+", area))
        fang['house_chaoxiang'] = house_info[2].strip() if len(house_info) > 2 else ''
        fang['house_floor'] = house_info[3].strip() if len(house_info) > 3 else ''
        fang['house_create_time'] = house_info[5].strip() if len(house_info) > 5 else ''
        # 14 人关注 · 近30天带看8 次 · 2022-10-25
        follow_info = selector.xpath('div[2]/div[1]/p[3]').xpath('string(.)').extract_first().split('·')
        fang['follow_info'] = follow_info[0].strip() if len(follow_info) > 0 else ''
        fang['upload_time'] = follow_info[2].strip() if len(follow_info) > 2 else ''
        # 价格信息
        fang['total_price'] = selector.xpath('div[2]/div[1]/div/p[1]/strong/text()').extract_first()
        unit_price: str = selector.xpath('div[2]/div[1]/div/p[2]/text()').extract_first()
        fang['unit_price'] = ''.join(re.findall(r"\d+", unit_price))
        return fang

    def _fake_next_page(self, response: HtmlResponse):
        next_url = response.xpath('/html/body/div[6]/div[1]/div[3]/div[2]/a[1]/@href').extract_first()
        if len(next_url) == 0:
            return None
        next_url = response.urljoin(next_url)
        return scrapy.Request(url=next_url, headers=_header, dont_filter=True)
