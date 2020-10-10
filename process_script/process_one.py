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
import json
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
        group, group_n, group_flag = [], 0, set()
        file = r"\\10.10.30.14\apy170101226_116万组人人多轮对话文本数据\完整数据包\data\116万组移动端交互文本数据.txt"
        new_file = r"\\10.10.30.14\apy170101226_116万组人人多轮对话文本数据\完整数据包\data\116万组移动端交互文本数据_s.txt"
        with open(file, 'r', encoding='utf8')as f, open(new_file, 'a', encoding='utf8')as w_f:
            for line in f:
                content = line.strip()
                if content == "_______________":
                    if len(group) >= 2:
                        # w_f.write("_______________\n")
                        # w_f.write("\n".join(group) + "\n")
                        pass
                    else:
                        group_n += 1
                        print(group)
                    group = []
                else:
                    if content:
                        content_txt = content[14:]
                        if content_txt not in group_flag:
                            group_flag.add(content_txt)
                            group.append(content)
            print(group_n)

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

    def process_mandarin(self):
        """
        处理3125普通话数据，重命名
        :return:
        """
        i_name = 1
        project_path = r"\\10.10.30.14\语音数据_2016\apy161101003_3125小时语音助手普通话实网采集语音数据\完整数据包_加密后数据\data\category"
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith("wav"):
                    file_name = os.path.splitext(file)[0]
                    new_file_name = str(i_name).zfill(8)
                    old_wav = os.path.join(root, file)
                    new_wav = os.path.join(root, file.replace(file_name, new_file_name))
                    os.rename(old_wav, new_wav)
                    os.rename(old_wav.replace("wav", "metadata"), new_wav.replace("wav", "metadata"))
                    os.rename(old_wav.replace("wav", "txt"), new_wav.replace("wav", "txt"))
                    i_name += 1

    def process_american(self):
        """
        数据包含wav文件的情况
        :return:
        """
        project_path = r"\\10.10.30.14\语音数据_2017\APY170701046_2_远场家居采集语音数据_噪音数据\完整数据包\Gnoise1\session01"
        # project_path = r"\\10.10.30.14\语音数据_2016\APY161101043_R_204人台湾普通话手机采集数据_朗读\完整数据包_加密后数据\data\category"
        re_repr = re.compile("\s*[0-9A-Za-z_]+\.wav\s*")
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith("txt"):
                    file_path = os.path.join(root, file)
                    print(file_path)
                    try:
                        with open(file_path, 'r+', encoding='utf8')as f:
                            content = f.readline()
                            new_content = re_repr.sub("", content)
                            f.seek(0)
                            f.truncate()
                            f.write(new_content)
                    except Exception as e:
                        with open(file_path, 'r+', encoding='gbk')as f, \
                                open(file_path.replace(".txt", "_tem.txt"), 'w', encoding='utf8')as w_f:
                            content = f.readline()
                            new_content = re_repr.sub("", content)
                            w_f.write(new_content)
                        os.remove(file_path)
                        os.rename(file_path.replace(".txt", "_tem.txt"), file_path)

    def process_uk(self):
        """
        处理英国儿童麦克风数据文本中多余部分
        :return:
        """
        # project_path = r"\\10.10.30.14\语音数据_2016\apy161101023_201人英国儿童麦克风采集语音数据\完整数据包_加密后数据\data\category"
        # re_repr = re.compile("\w+\.wav\s+")
        # for root, dirs, files in os.walk(project_path):
        #     for file in files:
        #         if file.endswith("txt"):
        #             file_path = os.path.join(root, file)
        #             with open(file_path, 'r+', encoding='utf8')as f:
        #                 content = f.readlines()[0]
        #                 new_content = re_repr.sub("", content)
        #                 f.seek(0)
        #                 f.truncate()
        #                 f.write(new_content)
        with open('error_the_file_is.txt', 'r+', encoding='utf8')as f:
            for line in f:
                file_path, *_ = line.strip().split("\t")
                with open(file_path, 'r+', encoding='utf8')as new_f:
                    ll = new_f.readlines()
                    if not ll:
                        print(file_path)

    def process_noise(self):
        """
        检查噪音数据文本格式是否在正确
        :return:
        """
        project_path = r"\\10.10.30.14\语音数据_2017\apy170101041_531小时麦克风手机采集车载噪音数据\完整数据包_加密后数据\data"
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith("txt"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r+', encoding='utf8')as f:
                        content = f.readlines()
                        if len(content[1].strip().split("\t")) != 11:
                            print(file_path)

    def process_utf_bom(self):
        """处理有标签的数据"""
        project_path = r"\\10.10.30.14\语音数据_2016\apy161101025_739人中国儿童麦克风采集语音数据\完整数据包_processed\data\category"
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith("txt"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r+', encoding='utf8')as f:
                        content = f.read()
                        new_content = content.strip("﻿")
                        f.seek(0)
                        f.truncate()
                        f.write(new_content)

    def process_json(self):
        """
        处理json文件报错的问题
        :return:
        """
        file = r"C:\Users\Administrator\Desktop\dingxiangyu_2.txt"
        with open(file, 'r', encoding='utf8')as f:
            content = json.load(f)
            print(content)


if __name__ == '__main__':
    po = ProcessOne()
    # po.process_116()
    # po.process_move()
    # po.process_multi_poly()
    # po.process_chinese()
    # po.process_changsha()
    # po.process_kunming()
    # po.process_mandarin()
    # po.process_noise()
    # po.process_american()
    # po.process_utf_bom()
    po.process_json()
