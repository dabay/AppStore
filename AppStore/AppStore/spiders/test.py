# -*- coding: utf-8 -*-
import scrapy
from ..items import CategoryItem
from scrapy.http import Request


class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["apple.com"]
    start_urls = (
        'https://itunes.apple.com/ie/genre/ios/id36?mt=8',
    )

    def parse(self, response):
        category_url_hash = {}
        # https://itunes.apple.com/ie/genre/ios-books/id6018?mt=8
        for sel in response.xpath('//ul[@class="list column first"]/li/a'):
            category = sel.xpath('text()').extract()[0]
            url = sel.xpath('@href').extract()[0]
            category_url_hash[category] = url
        for sel in response.xpath('//ul[@class="list column"]/li/a'):
            category = sel.xpath('text()').extract()[0]
            url = sel.xpath('@href').extract()[0]
            category_url_hash[category] = url
        for sel in response.xpath('//ul[@class="list column last"]/li/a'):
            category = sel.xpath('text()').extract()[0]
            url = sel.xpath('@href').extract()[0]
            category_url_hash[category] = url
        self.generate_requests_for_category(category_url_hash)

    def generate_requests_for_category(self, category_url_hash):
        # https://itunes.apple.com/ie/genre/ios-books/id6018?mt=8&letter=A&page=1
        for category in category_url_hash.keys():
            for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ*":
                url = "{0}&letter={1}&page=1#page".format(category_url_hash[category], c)
                print url
                yield Request(
                    url,
                    callback=self.parse_pages,
                    meta={'category': category}
                )
                # TODO: remove return
                return

    def parse_pages(self, response):
        # TODO: uncomment
        # for sel in response.xpath('//div[@class="column first"]/ul/li/a'):
        #     name = sel.xpath('text()').extract()[0]
        #     url = sel.xpath('@href').extract()[0]
        # for sel in response.xpath('//div[@class="column"]/ul/li/a'):
        #     name = sel.xpath('text()').extract()[0]
        #     url = sel.xpath('@href').extract()[0]
        # for sel in response.xpath('//div[@class="column last"]/ul/li/a'):
        #     name = sel.xpath('text()').extract()[0]
        #     url = sel.xpath('@href').extract()[0]
        print response.url
        for url in response.xpath('//ul[@class="list paginate"][1]/li[position()=last()]/a[text()="Next"]/@href'):
            yield Request(
                url,
                callback=self.parse_pages,
                meta={'category': response.meta['category']}
            )