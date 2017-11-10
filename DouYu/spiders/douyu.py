# -*- coding: utf-8 -*-
import scrapy
import json
from DouYu.items import DouyuItem

class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ['douyucdn.cn']
    base_url='http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset='
    offset=0

    start_urls = [base_url+str(offset)]

    def parse(self, response):
        data_list=json.loads(response.body)['data']

        if not data_list:
            return

        for data in data_list:
            item = DouyuItem()
            item['room_link'] = "http://www.douyu.com/" + data['room_id']
            item['image_link'] = data['vertical_src']
            item['nick_name'] = data['nickname']
            item['city'] = data['anchor_city']

            yield item

        self.offset += 20
        yield scrapy.Request(self.base_url + str(self.offset), callback=self.parse)

