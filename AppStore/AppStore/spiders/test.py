# -*- coding: utf-8 -*-
import scrapy
from ..items import CategoryItem


class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["apple.com"]
    start_urls = (
        'https://itunes.apple.com/ie/genre/ios/id36?mt=8',
    )

    def parse(self, response):
        category_url_list = []
        for sel in response.xpath('//ul[@class="list column first"]/li/a'):
            category_url_list.append(sel.xpath('@href').extract())
        for sel in response.xpath('//ul[@class="list column"]/li/a'):
            category_url_list.append(sel.xpath('@href').extract())
        for sel in response.xpath('//ul[@class="list column last"]/li/a'):
            category_url_list.append(sel.xpath('@href').extract())
        for url in category_url_list:
            print url