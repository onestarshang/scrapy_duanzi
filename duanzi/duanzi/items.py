# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DuanziItem(scrapy.Item):
    duanzi_id = scrapy.Field()
    duanzi_txt = scrapy.Field()
    duanzi_date = scrapy.Field()
