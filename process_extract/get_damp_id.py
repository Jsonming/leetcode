#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/16 15:14
# @Author  : yangmingming
# @Site    : 
# @File    : get_damp_id.py
# @Software: PyCharm
import pandas as pd
from requests import Session
import json
import copy
import os


class DampId(object):
    def __init__(self):
        pass

    def read_xlsx(self):
        """
        读取要抓取的数据文件
        :param xlsx_file:
        :return:
        """
        xlsx_file = r"damp_keyword.xlsx"
        return pd.read_excel(xlsx_file)

    def get_id(self, keyword):
        """
        根据关键词获取连接id
        :param keyword:
        :return:
        """
        session = Session()
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Connection": "keep-alive",
            "Cookie": "Hm_lvt_c11a8399d964da0bb1f13ee5438d021d=1574392765,1574418656; JSESSIONID=2617E01A7F39D93D8334B81176229670",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        }

        data = {
            'fullsearchvalue': keyword,
            "onlineFlag": 1,
            "currentPage": 1,
            "pageSize": 20

        }
        url = "http://damp.datatang.com/fullSearch/searchProduct"
        response = session.post(url, headers=headers, data=data)
        content = json.loads(response.text)
        count = content.get("count")
        if count == 1:
            sample = content.get("rows")[0].get("bbom")
            product_name = content.get("rows")[0].get("productname")
            return [product_name, sample]

    def process_data(self, df):
        """
        获取到数据循环数据，拿到id
        :param df:
        :return:
        """
        result = []
        for row in df.iterrows():
            result.append([row[1]["序号"], row[1]["名称"], row[1]["数据"]])
        return result

    def run(self):
        data_path_s = [
            r"\\10.10.30.14\d\图像",
            r"\\10.10.30.14\e\图像数据\图像数据2016",
            r"\\10.10.30.14\e\图像数据\图像数据2017",

            r"\\10.10.30.14\d\语音",
            r"\\10.10.30.14\d\语音\语音数据_2016",
            r"\\10.10.30.14\d\语音\语音数据_2017",
            r"\\10.10.30.14\e\老版本数据",
            r"\\10.10.30.14\e\老版本数据\十四国返修",

            r"\\10.10.30.14\d\文本",
            r"\\10.10.30.14\d\文本\文本数据_2016",
            r"\\10.10.30.14\d\文本\文本数据_2017"
        ]

        data_path = []
        for folder in data_path_s:
            sub_folder = [os.path.join(folder, sub_f) for sub_f in os.listdir(folder)]
            data_path.extend(sub_folder)

        dataframe = self.read_xlsx()
        origin_data = self.process_data(dataframe)
        with open("id_info.txt", 'a', encoding='utf8')as f:
            for origin_data_item in origin_data:
                product_info = self.get_id(origin_data_item[-1])
                combination_info = copy.deepcopy(origin_data_item)
                dest_path = r"\\10.10.8.123\刘晓东\liuxd_share\实验数据\200个课外\{}、{}\data".format(combination_info[0], combination_info[1])
                if product_info:
                    combination_info.extend(product_info)
                    combination_info.append(dest_path)
                    for sub in data_path:
                        if product_info[1] in sub:
                            combination_info.append(sub)

                f.write("\t".join([str(info) for info in combination_info]) + "\n")


if __name__ == '__main__':
    dd = DampId()
    dd.run()
