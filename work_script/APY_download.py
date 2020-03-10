#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/5 16:54
# @Author  : yangmingming
# @Site    : 
# @File    : APY_download.py
# @Software: PyCharm
import requests
import urllib
import pandas as pd


class APYDownload(object):
    def __init__(self):
        self.headers = {
            'cache-control': "no-cache",
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }

    def get_link(self, file_path: str):
        """
        从execl文件中获取连接和将要命名的文件名
        :param file_path: execl 文件
        :param limit: 要获取的限制
        :return:
        """
        links = pd.read_excel(file_path, header=None)
        return links.values.tolist()

    def download(self, file_name, file_link):
        """
        下载文件
        :param file_name: 文件名
        :param file_link: 文件连接
        :return:
        """
        try:
            response = requests.get(url=file_link, timeout=240)
        except Exception as e:
            with open('links.txt', 'a', encoding="utf8")as f:
                f.write(file_name + "\t" + file_link + "\n")
        else:
            with open('{}.zip'.format(file_name), 'wb', )as f:
                f.write(response.content)

    def run(self):
        file_path = r"mingming.xlsx"
        file_name_links = self.get_link(file_path=file_path)  # 读取连接内容

        sub_links = file_name_links[26:50]  # 截取出一部分，便于在多台机器上下载
        for link in sub_links:
            file_name, _, file_link = link

            if " " in file_link:
                # print(file_link)
                pass
            else:
                print(file_name, file_link)
                self.download(file_name, file_link)


if __name__ == '__main__':
    apy = APYDownload()
    apy.run()
