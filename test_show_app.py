# -*- coding: utf8 -*-
__author__ = 'Xiaohuan_Wang'

from show_app import get_html_response, parse_app_item

import mock
import unittest
import requests

class ShowAppTestCase(unittest.TestCase):

    def setUp(self):
        self.url = "https://itunes.apple.com/ie/app/myvideo-mobile-tv-hd/id557524762?mt=8"
        self.reponse = requests.get(self.url)

    @mock.patch('show_app.html')
    @mock.patch('show_app.requests')
    def test_requests_get(self, mock_requests, mock_html):
        self.assertTrue(mock_requests.get.assert_called, "requets.get is called.")

    def test_url(self):
        response = get_html_response(self.url)
        self.assertTrue(len(unicode(response.text)) > 100)

    def test_parse_app_item(self):
        app = parse_app_item(self.reponse)
        self.assertTrue(app.title, "Myvideo Mobile TV HD")

