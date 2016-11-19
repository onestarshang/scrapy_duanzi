# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import time
import MySQLdb
import MySQLdb.cursors


from scrapy import log


class DuanziPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
            host = HOST,
            db = DB,
            user = USER,
            passwd = PWD,
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = True
        )

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)

    def _conditional_insert(self, tx, item):
        sql = '''insert into duanzi (duanzi_id, duanzi_txt, create_date, publish_date,
                 status, pic_urls)
                 values (%s, %s, %s, %s, %s, %s);'''
        tx.execute(sql, (item['duanzi_id'], item['duanzi_txt'], item['duanzi_date'],
                         '', 2, '')
                )

    def handle_error(self, e):
        log.err(e)
