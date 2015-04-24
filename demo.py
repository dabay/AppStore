# -*- coding: utf8 -*-
__author__ = 'Xiaohuan_Wang'

import sys
import subprocess
import signal
import os
import re

from lxml import html
import requests
from colorclass import Color
from terminaltables import SingleTable
from requests.exceptions import RequestException


DEMO_URL = 'https://itunes.apple.com/ie/app/myvideo-mobile-tv-hd/id557524762?mt=8'
DEMO_URL = 'https://itunes.apple.com/ie/app/train4top/id942553423?mt=8'
WORKER_USER = "nardev"
WORKER_IP = "172.16.88.15"
IPA_REMOTE_FOLDER = "/cygdrive/c/Users/nardev/Music/iTunes/iTunes\ Media/Mobile\ Applications/"
IPA_LOCAL_FOLDER = "/home/cdag/ipa/"


class AppItem(object):
    def __init__(self):
        self.id = "Unknown"
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


def pre_exec():
    """
    Ignore the SIGINT signal by setting the handler to the standard signal handler SIG_IGN.
    """
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def exec_cmd(cmd, *args):
    cmd_str = cmd + " " + " ".join(args)
    res = subprocess.Popen(
        cmd_str, shell=True, bufsize=2048,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        preexec_fn=pre_exec
    )
    return res.communicate()[0]


def ssh_exec_cmd(cmd):
    """
    Put double -t is crucial to prevent various status messages popping up
    """
    ssh_command_prefix = str(
        "ssh {0}@{1} -t -t -i ~/.ssh/id_rsa "
    ).format(WORKER_USER, WORKER_IP)
    return exec_cmd(ssh_command_prefix, cmd)


def get_app_id(url):
    # "https://itunes.apple.com/ie/app/a-1-cab-taxi-booking/id937336120?mt=8"
    p = re.compile("/id(\d+)\?")
    m = p.search(str(url))
    return int(m.group(1))


def get_app_item(app_url):
    a = AppItem()
    a.url = app_url
    try:
        page = requests.get(a.url)
    except RequestException:
        print "Error to get HTTP response."
        sys.exit(1)
    a.id = get_app_id(a.url)
    tree = html.fromstring(page.text)
    a.title = tree.xpath('//div[@id="title"]//h1[@itemprop="name"]/text()')[0]
    a.category = tree.xpath('//span[@itemprop="applicationCategory"]/text()')[0]
    a.developer = tree.xpath('//span[@itemprop="name"]/text()')[0]
    a.price = tree.xpath('//div[@itemprop="price"]/text()')[0]
    a.release = tree.xpath('//span[@itemprop="datePublished"]/text()')[0].strip()
    a.version = tree.xpath('//span[@itemprop="softwareVersion"]/text()')[0]
    a.size = tree.xpath('//span[@class="label" and text()="Size: "]/../text()')[0]
    a.language = tree.xpath('//*[contains(text(), "Language")]/../text()')[0]
    a.compatibility = tree.xpath('//span[@itemprop="operatingSystem"]/text()')[0]
    a.description = tree.xpath('//p[@itemprop="description"]/text()')[0]
    if len(a.description) > 100:
        a.description = a.description[:100] + "..."
    return a


def show_app_item(a):
    x = lambda s: Color('{autogreen}%s{/autogreen}' % s)
    y = lambda s: '{0: <20}'.format(s)
    table_data = [
        [y('Title'), x(a.title)],
        [y('URL'), x(a.url)],
        [y('Price'), x(a.price)],
        [y('Category'), x(a.category)],
        [y('Release'), x(a.release)],
        [y('Version'), x(a.version)],
        [y('Size'), x(a.size)],
        [y('Language(s)'), x(a.language)],
        [y('Developer'), x(a.developer)],
        [y('Compatibility'), x(a.compatibility)],
        [y('Description:'), x(a.description)],
    ]
    table = SingleTable(table_data)
    table.inner_column_border = False
    table.inner_heading_row_border = False
    print(table.table)


def scp_cmd(cmd):
    ssh_command_prefix = str("scp -i ~/.ssh/id_rsa ")
    return exec_cmd(ssh_command_prefix, cmd)


def list_files(folder_path):
    ipa_files = [f for f in os.listdir(folder_path) if str(f).endswith(".ipa")]
    table_data = [[' * ', Color('{autoblue}%-40s{/autoblue}' % f)] for f in ipa_files]
    table = SingleTable(table_data)
    table.title = "All ipa files:"
    table.inner_column_border = False
    table.inner_heading_row_border = False
    print(table.table)


def confirm_to_continue(question):
    print Color('{autoyellow}%s{/autoyellow}' % question)
    answer = raw_input("Continue? (Y/n):")
    if answer.lower() == "n":
        print "Quit!"
        sys.exit(0)


def show_message(message):
    print Color('{autoyellow}%s{/autoyellow}' % message)
    print


if __name__ == '__main__':
    confirm_to_continue("Crawl data from {}?".format(DEMO_URL))
    app = get_app_item(DEMO_URL)
    show_message("Successfully got data.")

    confirm_to_continue("Show meta data for app?")
    show_app_item(app)

    confirm_to_continue("Send the app to VM to download ipa file?")
    autoit_cmd = "./AutoIt3.exe install_app.au3 %s 0" % app.id
    ssh_exec_cmd(autoit_cmd)
    show_message("Command sent to VM.")

    confirm_to_continue("Retrieve ipa file from VM?")
    scp_sub_cmd = '{}@{}:"{}*" {}'.format(WORKER_USER, WORKER_IP, IPA_REMOTE_FOLDER, IPA_LOCAL_FOLDER)
    scp_cmd(scp_sub_cmd)
    show_message("Copied back, listing files the local folder.")
    list_files(IPA_LOCAL_FOLDER)
