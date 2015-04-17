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
        for sel in response.xpath('//ul[@class="list column first"]/li/a'):
            item = CategoryItem()
            item['category_name'] = sel.xpath('text()').extract()
            item['category_url'] = sel.xpath('@href').extract()
            yield item

        for sel in response.xpath('//ul[@class="list column"]/li/a'):
            item = CategoryItem()
            item['category_name'] = sel.xpath('text()').extract()
            item['category_url'] = sel.xpath('@href').extract()
            yield item

        for sel in response.xpath('//ul[@class="list column last"]/li/a'):
            item = CategoryItem()
            item['category_name'] = sel.xpath('text()').extract()
            item['category_url'] = sel.xpath('@href').extract()
            yield item