#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/3 10:19
# @Author  : yangmingming
# @Site    : 
# @File    : process_one.py
# @Software: PyCharm
import os
import re
import time
import pandas as pd
from pybloom_live import ScalableBloomFilter, BloomFilter


class ProcessOne(object):
    def __init__(self):
        self.bloom = ScalableBloomFilter(initial_capacity=100, error_rate=0.00000001)

    def process_116(self):
        """
        处理116W  多轮交互数据
        :return:
        """
        group, group_n = [], 0
        file = r"\\10.10.30.14\apy170101226_116万组人人多轮对话文本数据\完整数据包\data\116万组移动端交互文本数据.txt"
        new_file = r"\\10.10.30.14\apy170101226_116万组人人多轮对话文本数据\完整数据包\data\116万组移动端交互文本数据_s.txt"
        with open(file, 'r', encoding='utf8')as f, open(new_file, 'a', encoding='utf8')as w_f:
            for line in f:
                content = line.strip()
                print(content)
                # if content == "_______________":
                #     if group:
                #         w_f.write("_______________\n")
                #         w_f.write("\n".join(group) + "\n")
                #         group = []
                # else:
                #     if content:
                #         if content not in group:
                #             group.append(content)

    def process_move(self):
        """
        处理1亿移动用户文本
        :return:
        """
        i = 0
        file = r"\\10.10.30.14\apy161201218_1亿条移动用户实网文本数据\数据\第一批_s.txt"
        with open(file, 'r', encoding='utf8')as f:
            for line in f:
                content = line.strip()
                if content not in self.bloom:
                    self.bloom.add(content)
                else:
                    print(content)

    def process_multi_poly(self):
        """
        处理多音字
        :return:
        """
        i = 0
        folder = r"\\10.10.30.14\apy190921001_汉语多音字语料库\完整数据包\data"
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            with open(file_path, 'r', encoding='utf8')as f:
                for line in f:
                    i += 1
        print(i)

    def process_chinese(self):
        """
        处理二十万中文韵律
        :return:
        """
        content_s = 0
        file = r"\\10.10.30.14\apy190717001_20万条中文文本韵律语料库\完整数据包\data\20万句中文韵律语料库.txt"
        with open(file, 'r', encoding='utf8')as f:
            for line in f:
                content_s += 1

        print(content_s)

    def process_changsha(self):
        """
        长沙方言
        :return:
        """
        line_s = 0
        file = r"\\10.10.30.14\apy190509003_d_6万条长沙方言发音词典\完整数据包\data\长沙词典.txt"
        with open(file, 'r', encoding='utf8')as f:
            for line in f:
                line_s += 1
        print(line_s)

    def process_kunming(self):
        file = r"\\10.10.30.14\apy190509001_d_9.1万条武汉方言发音词典\完整数据包\data\武汉词典.xlsx"
        df = pd.read_excel(file)
        print(len(df["发音"]))
        print(len(df["发音"].drop_duplicates()))


if __name__ == '__main__':
    po = ProcessOne()
    # po.process_116()
    po.process_move()
    # po.process_multi_poly()
    # po.process_chinese()
    # po.process_changsha()
    # po.process_kunming()
