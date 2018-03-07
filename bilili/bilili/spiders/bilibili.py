# -*- coding: utf-8 -*-
import scrapy, re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import requests


class BilibiliSpider(CrawlSpider):
    name = 'bilibili'
    allowed_domains = ['bilibili.com']
    start_urls = ['https://www.bilibili.com/']

    rules = (
        Rule(LinkExtractor(allow=r'/video/'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'v/'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'bilibili.com/'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/[0-9]{2,12}'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/space'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = {}
        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # i['name'] = response.xpath('//div[@id="name"]').extract()
        # i['description'] = response.xpath('//div[@id="description"]').extract()
        url = response.url
        print("--------------------------------------------------------------------------------------")
        print(url)
        user_id = re.findall(re.compile(r'https://space\.bilibili\.com/([0-9]{2,20}).*?'), str(url))
        print(user_id)
        # print(response.text)
        if user_id != None or user_id != "":
            user_url = "https://space.bilibili.com/ajax/member/GetInfo"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'http://space.bilibili.com/{}'.format(user_id),
                'Origin': 'http://space.bilibili.com',
                'Host': 'space.bilibili.com',
                'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
                'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
            }
            post_data = {
                "mid": "{}".format(user_id),
                "csrf": "null",
            }
            user_response = requests.post(user_url, headers=headers, data=post_data)
            print(user_response.json())
        return i
