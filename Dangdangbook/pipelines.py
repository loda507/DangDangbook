# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import log
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors

class DangdangbookPipeline(object):
    def __init__(self):

        dbargs = dict(
            host='localhost',
            db='test',
            user='root',
            passwd='123456',
            charset='utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode= True,
        )
        self.dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)

    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upinsert, item)
        d.addErrback(self.handle_error)

        return item

    def _do_upinsert(self, conn, item):
        if item.get('name'):
            conn.execute(\
                "insert into Dangdangbooks (name, url, price)\
                values (%s, %s, %s)",
                (item['name'],
                 item['url'],
                 item['price'])
                )
    def handle_error(self, e):
        log.err(e)

