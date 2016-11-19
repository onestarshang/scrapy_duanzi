# -*- coding: utf-8 -*-

from datetime import datetime
import re

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

from duanzi.items import DuanziItem


def filter_at(text):
    reg = re.compile('(@.*)')
    m = reg.search(text)
    if m:
        text = text.split('@')[0][:-1]
    return text


class DuanziSpider(CrawlSpider):
    name = "duanzi"
    allowed_domains = ["jandan.net"]
    rules = [Rule(SgmlLinkExtractor(allow=('duan/page-\d+#comments'),
                                    ),
                  callback='parse_item',
                  follow=True)
    ]

    def __init__(self, *args, **kwargs):
        super(DuanziSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://jandan.net/duan/page-1#comments']

    def parse_item(self, response):
        sel = Selector(response)
        items = []
        comments = sel.xpath('//*[starts-with(@id, "comment-")]')
        for comment in comments:
            item = DuanziItem()
            item['duanzi_id'] = comment.xpath('@id').extract()[0].split('-')[-1]
            text = comment.xpath('div[1]/div/div[2]/p/text()').extract()[0].strip()
            if not text:
                continue
            item['duanzi_txt'] = filter_at(text)
            item['duanzi_date'] = datetime.now()
            items.append(item)
        return items

