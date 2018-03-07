# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BilicrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    mid = scrapy.Field()
    name = scrapy.Field()
    sex = scrapy.Field()
    face = scrapy.Field()
    coins = scrapy.Field()
    spacesta = scrapy.Field()

    birthday = scrapy.Field()
    place = scrapy.Field()

    description = scrapy.Field()
    article = scrapy.Field()
    following = scrapy.Field()
    fans = scrapy.Field()
    playnum = scrapy.Field()
    sign = scrapy.Field()
    level = scrapy.Field()
    exp = scrapy.Field()
