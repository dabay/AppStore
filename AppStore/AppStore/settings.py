# -*- coding: utf-8 -*-

# Scrapy settings for AppStore project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'AppStore'

SPIDER_MODULES = ['AppStore.spiders']
NEWSPIDER_MODULE = 'AppStore.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'AppStore (+http://www.yourdomain.com)'
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
COOKIES_ENABLED = False
COOKIES_DEBUG = False

ITEM_PIPELINES = {'AppStore.pipelines.AppstoreItemPipeline': 300 }