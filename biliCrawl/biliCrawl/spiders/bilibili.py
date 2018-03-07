# -*- coding: utf-8 -*-
import scrapy
from biliCrawl.items import BilicrawlItem
import json
import requests


class BilibiliSpider(scrapy.Spider):
    name = 'bilibili'
    allowed_domains = ['bilibili.com']
    start_urls = ['https://www.bilibili.com/']

    def parse(self, response):
        user_url = "https://space.bilibili.com/ajax/member/GetInfo"

        for mid in range(100, 100000000):
            # for mid in range(1, 100):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'http://space.bilibili.com/{}'.format(mid),
                'Origin': 'http://space.bilibili.com',
                'Host': 'space.bilibili.com',
                'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
                'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
            }
            post_data = {
                "mid": "{}".format(mid),
                "csrf": "null",
            }
            yield scrapy.FormRequest(
                url=user_url,
                formdata=post_data,
                headers=headers,
                callback=self.parse_page

            )

    def parse_page(self, response):
        itme = BilicrawlItem()

        jscontent = response.text
        jsDict = json.loads(jscontent)
        statusJson = jsDict['status'] if 'status' in jsDict.keys() else False
        if statusJson == True:
            if 'data' in jsDict.keys():
                jsData = jsDict['data']
                itme["mid"] = jsData['mid']
                itme["name"] = jsData['name']
                itme["sex"] = jsData['sex']
                itme["face"] = jsData['face']
                itme["coins"] = jsData['coins']
                itme["spacesta"] = jsData['spacesta']
                itme["birthday"] = jsData['birthday'] if 'birthday' in jsData.keys() else 'nobirthday'
                itme["place"] = jsData['place'] if 'place' in jsData.keys() else 'noplace'
                itme["description"] = jsData['description']
                itme["article"] = jsData['article']
                itme["playnum"] = jsData['playNum']
                itme["sign"] = jsData['sign']
                itme["level"] = jsData['level_info']['current_level']
                itme["exp"] = jsData['level_info']['current_exp']
                itme["following"] = 0
                itme["fans"] = 0

                # print(mid, name, sex, face, coins, spacesta,
                #       birthday, place, description, article, following, fans, playnum, sign, level, exp)
        print(jscontent)
        return itme
