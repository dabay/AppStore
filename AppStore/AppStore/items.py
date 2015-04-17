# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AppstoreItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    app_id = scrapy.Field()

class CategoryItem(scrapy.Item):
    category_name = scrapy.Field()
    category_url = scrapy.Field()
