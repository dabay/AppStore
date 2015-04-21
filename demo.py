# -*- coding: utf8 -*-
__author__ = 'Xiaohuan_Wang'

from lxml import html
import requests
from colorclass import Color
from terminaltables import SingleTable
import sys
import subprocess
import signal
import os
import re


DEMO_URL = 'https://itunes.apple.com/ie/app/myvideo-mobile-tv-hd/id557524762?mt=8'
WORKER_USER = "nardev"
WORKER_IP = "172.16.88.15"
IPA_REMOTE_FOLDER = "/cygdrive/c/Users/nardev/Music/iTunes/iTunes\ Media/Mobile\ Applications/"
IPA_LOCAL_FOLDER = "~/ipa/"


class AppItem(object):

    def __init__(self):
        id = "Unknown"
        title = "Unknown"
        category = "Unknown"
        url = "Unknown"
        developer = "Unknown"
        price = "Unknown"
        release = "Unknown"
        version = "Unknown"
        size = "Unknown"
        language = "Unknown"
        compatibility = "Unknown"
        description = "Unknown"


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
    app = AppItem()
    app.url = app_url
    try:
        page = requests.get(app.url)
    except:
        print "Error to get HTTP response."
        sys.exit(1)
    app.id = get_app_id(app.url)
    tree = html.fromstring(page.text)
    app.title = tree.xpath('//div[@id="title"]//h1[@itemprop="name"]/text()')[0]
    app.category = tree.xpath('//span[@itemprop="applicationCategory"]/text()')[0]
    app.developer = tree.xpath('//span[@itemprop="name"]/text()')[0]
    app.price = tree.xpath('//div[@itemprop="price"]/text()')[0]
    app.release = tree.xpath('//span[@itemprop="datePublished"]/text()')[0].strip()
    app.version = tree.xpath('//span[@itemprop="softwareVersion"]/text()')[0]
    app.size = tree.xpath('//span[@class="label" and text()="Size: "]/../text()')[0]
    app.language = tree.xpath('//span[@class="label" and text()="Language: "]/../text()')[0]
    app.compatibility = tree.xpath('//span[@itemprop="operatingSystem"]/text()')[0]
    app.description = tree.xpath('//p[@itemprop="description"]/text()')[0]
    return app


def show_app_item(app):
    table_data = [
        ['{0: <20}'.format('Title'),Color('{autoblue}%s{/autoblue}' % app.title)],
        ['{0: <20}'.format('URL'), Color('{autocyan}%s{/autocyan}' % app.url)],
        ['{0: <20}'.format('Price'), Color('{autogreen}%s{/autogreen}' % app.price)],
        ['{0: <20}'.format('Category'),Color('{autogreen}%s{/autogreen}' % app.category)],
        ['{0: <20}'.format('Release'),Color('{autogreen}%s{/autogreen}' % app.release)],
        ['{0: <20}'.format('Version') ,Color('{autogreen}%s{/autogreen}' % app.version)],
        ['{0: <20}'.format('Size'),Color('{autogreen}%s{/autogreen}' % app.size)],
        ['{0: <20}'.format('Language'),Color('{autogreen}%s{/autogreen}' % app.language)],
        ['{0: <20}'.format('Developer'),Color('{autogreen}%s{/autogreen}' % app.developer)],
        ['{0: <20}'.format('Compatibility'),Color('{autogreen}%s{/autogreen}' % app.compatibility)],
        ['{0: <20}'.format('Description:'),Color('{autocyan}%s{/autocyan}' % app.description)],
    ]
    table = SingleTable(table_data)
    table.inner_column_border = False
    table.inner_heading_row_border = False
    print(table.table)


def pre_exec():
    """
    Ignore the SIGINT signal by setting the handler to the standard signal handler SIG_IGN.
    """
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def exec_cmd(cmd, *args):
    cmd_str = cmd + " " + " ".join(args)
    res = subprocess.Popen(
        cmd_str, shell=True, bufsize=2048,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=pre_exec
    )
    return res.communicate()[0]


def scp_cmd(cmd):
    ssh_command_prefix = str("scp -i ~/.ssh/id_rsa ")
    return exec_cmd(ssh_command_prefix, cmd)


def list_files(folder_path):
    ipa_files = [f for f in os.listdir(folder_path) if str(f).endswith(".ipa")]
    table_data = [[' * ', Color('{autoblue}%-40s{/autoblue}'%f)] for f in ipa_files]
    table = SingleTable(table_data)
    table.title = "All ipa files:"
    table.inner_column_border = False
    table.inner_heading_row_border = False
    print(table.table)


def confirm_to_continue(question):
    print Color('{autoyellow}%s{/autoyellow}'%question)
    answer = raw_input("Continue? (Y/n):")
    if answer.lower() == "n":
        print "Quit!"
        sys.exit(0)


def show_message(message):
    print Color('{autoyellow}%s{/autoyellow}'%message)


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
    scp_sub_cmd = '{}@{}:"{}*" {}'.format(WORKER_USER, WORKER_IP,IPA_REMOTE_FOLDER, IPA_LOCAL_FOLDER)
    scp_cmd(scp_sub_cmd)
    show_message("Copied back, listing files the local folder.")
    list_files(IPA_LOCAL_FOLDER)
