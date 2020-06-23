#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/6 11:24
# @Author  : yangmingming
# @Site    : 
# @File    : tts.py
# @Software: PyCharm
from work.temporary.temp_task_urls import task_urls

import requests
import re
import pprint
import json
from lxml import etree


class DemoSpider(object):
    def __init__(self):
        self.headers = {
            'cache-control': "no-cache",
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }
        self.resp = None

    def crawl_get(self, url, headers=None):
        if not headers:
            _headers = headers
        else:
            _headers = self.headers

        response = requests.request("GET", url, headers=_headers)
        print(response.content)
        print(response.status_code)
        with open('pig.mp3', 'wb')as f:
            f.write(response.content)

    def crawl_post(self, url, data, headers=None):
        if not headers:
            _headers = headers
        else:
            _headers = self.headers

        response = requests.request("POST", url, data=data, headers=_headers)
        self.resp = response.content.decode("gb2312")

    def parse_html(self):
        # with open("weibo.html", 'a', encoding='gb2312')as f:
        #     f.write(self.resp)

        print(self.resp)
        html = etree.HTML(self.resp)

    def parse_json(self):

        names = []
        response = json.loads(self.resp)
        stores = response.get("stores")
        for store in stores:
            store_name = store.get("business").get("name")
            names.append(store_name)

    def run(self):
        # url = task_urls[0]
        # print(url)
        url = 'https://translate.google.cn/translate_tts?ie=UTF-8&q=boy&tl=en&total=1&idx=0&textlen=3&tk=491828.80597&client=webapp&prev=input'

        self.crawl_get(url)
        # self.parse_html()
        # self.parse_json()


if __name__ == '__main__':
    demo = DemoSpider()
    demo.run()
