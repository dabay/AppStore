# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import re
from scrapy.exceptions import DropItem

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

    def row_count_in_table(self, app_id):
        try:
            sql = ("""select count(*) from app_id where app_id='%s'""")
            self.cursor.execute(sql, [app_id])
            result = self.cursor.fetchone()
            if result:
                if result[0]:
                    return result[0]
                else:
                    return 0
            else:
                return 0
        except MySQLdb.Error, ex:
            print "Error {}: {}".format(ex.args[0], ex.args[1])
        return 0

    def process_item(self, item, spider):
        item_dict = dict(item)
        item_dict["app_id"] = self.get_app_id(item_dict["url"])
        if self.row_count_in_table(item_dict["app_id"]) > 0:
            raise DropItem("Already in DB: {}".format(item_dict["app_id"]))
        try:
            sql = ("""
                INSERT INTO app_id(app_id, category,name, url)
                VALUES (%(app_id)s,%(category)s,%(name)s,%(url)s);
            """)
            self.cursor.execute(sql, item_dict)
            self.conn.commit()
        except MySQLdb.Error, ex:
            raise DropItem("Error {}: {}".format(ex.args[0], ex.args[1]))
        return item