# -*- coding: utf8 -*-
__author__ = 'Xiaohuan_Wang'

from lxml import html
import requests
from colorclass import Color, Windows
from terminaltables import SingleTable
import sys

class AppItem(object):

    def __init__(self):
        self.title = "Unknown"
        self.category = "Unknown"
        self.url = "Unknown"
        self.developer = "Unknown"
        self.price = "Unknown"
        self.release = "Unknown"
        self.version = "Unknown"
        self.size = "Unknown"
        self.language = "Unknown"
        self.compatibility = "Unknown"
        self.description = "Unknown"
        self.page_source_code = ""


def get_html_response(url):
    try:
        source = requests.get(url)
    except:
        print "Error to get HTTP response."
        sys.exit(1)
    return source


def parse_app_item(html_reponse):
    if html_reponse == "":
        print "Not page source to parse in AppItem object."
        sys.exit(1)
    app = AppItem()
    app.page_source_code = html_reponse.text
    tree = html.fromstring(app.page_source_code)
    app.title = tree.xpath('//div[@id="title"]//h1[@itemprop="name"]/text()')[0]
    app.category = tree.xpath('//span[@itemprop="applicationCategory"]/text()')[0]
    app.developer = tree.xpath('//span[@itemprop="name"]/text()')[0]
    app.price = tree.xpath('//div[@itemprop="price"]/text()')[0]
    app.release = tree.xpath('//span[@itemprop="datePublished"]/text()')[0].strip()
    app.version = tree.xpath('//span[@itemprop="softwareVersion"]/text()')[0]
    app.size = tree.xpath('//span[@class="label" and text()="Size: "]/../text()')[0]
    app.language = tree.xpath('//*[contains(text(), "Language")]/../text()')[0]
    app.compatibility = tree.xpath('//span[@itemprop="operatingSystem"]/text()')[0]
    app.description = tree.xpath('//p[@itemprop="description"]/text()')[0].strip()
    return app


def get_url():
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = 'https://itunes.apple.com/ie/app/myvideo-mobile-tv-hd/id557524762?mt=8'
        #url = 'https://itunes.apple.com/ie/app/apanclub/id978231645?mt=8'
    return url


def fill_tabel(app):
    table_data = [
        ['{0: <20}'.format('Title'),Color('{autoblue}%-50s{/autoblue}' % app.title)],
        ['{0: <20}'.format('URL'), Color('{autocyan}%s{/autocyan}' % app.url)],
        ['{0: <20}'.format('Price'), Color('{autogreen}%s{/autogreen}' % app.price)],
        ['{0: <20}'.format('Category'),Color('{autogreen}%s{/autogreen}' % app.category)],
        ['{0: <20}'.format('Release'),Color('{autogreen}%s{/autogreen}' % app.release)],
        ['{0: <20}'.format('Version') ,Color('{autogreen}%s{/autogreen}' % app.version)],
        ['{0: <20}'.format('Size'),Color('{autogreen}%s{/autogreen}' % app.size)],
        ['{0: <20}'.format('Language(s)'),Color('{autogreen}%s{/autogreen}' % app.language)],
        ['{0: <20}'.format('Developer'),Color('{autogreen}%s{/autogreen}' % app.developer)],
        ['{0: <20}'.format('Compatibility'),Color('{autogreen}%s...{/autogreen}' % ".".join(app.compatibility.split('.')[:2]))],
        ['{0: <20}'.format('Description:'),Color('{autocyan}%-50s{/autocyan}' % app.description)],
    ]
    table = SingleTable(table_data)
    table.inner_column_border = False
    table.inner_heading_row_border = False
    return table


def print_table(table):
    print(table.table)


def main():
    url = get_url()
    html = get_html_response(url)
    app = parse_app_item(html)
    app.url = url
    table = fill_tabel(app)
    print_table(table)


def test():
    #Windows.enable(auto_colors=True, reset_atexit=True)
    table_data = [
        [Color('{autogreen}TITLE{/autogreen}'), '192.168.0.100, 192.168.0.101'],
        [Color('{autocyan}10ms <= 100ms{/autocyan}'), '192.168.0.102, 192.168.0.103'],
        [Color('{autored}>100ms{/autored}'), '192.168.0.105'],
    ]
    table = SingleTable(table_data)
    table.inner_heading_row_border = False
    print(table.table)


if __name__ == '__main__':
    main()
    #test()
