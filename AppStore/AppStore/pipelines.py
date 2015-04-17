# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import re

class AppstorePipeline(object):
    def process_item(self, item, spider):
        return item


class AppstoreItemPipeline(object):

    def __init__(self):
        self.conn = MySQLdb.connect(
            user='root', passwd='crawlURL',
            db='app_store', host='127.0.0.1', charset="utf8", use_unicode=True
        )
        self.cursor = self.conn.cursor()

    def get_app_id(self, url):
        # "https://itunes.apple.com/ie/app/a-1-cab-taxi-booking/id937336120?mt=8"
        p = re.compile("/id(\d+)\?")
        m = p.search(str(url))
        return int(m.group(1))

    def process_item(self, item, spider):
        print item
        print "-" * 150
        item_dict = dict(item)
        item_dict["app_id"] = self.get_app_id(item_dict["url"])
        try:
            sql = ("""
                INSERT INTO app_id(app_id, name, url)
                VALUES (%(app_id)s,%(name)s,%(url)s);
            """)
            self.cursor.execute(sql, item_dict)
            self.conn.commit()
        except MySQLdb.Error, ex:
            print "Error %d: %s" % (ex.args[0], ex.args[1])
        return item