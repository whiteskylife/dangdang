# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class DangdangItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'dangdang_python'
    title = Field()
    buy_links = Field()
    detail = Field()

    now_price = Field()
    pre_price = Field()
    discount = Field()

    favorites_ratio = Field()
    comment_num = Field()

    author = Field()
    pub_time = Field()
    publisher = Field()

    pass
