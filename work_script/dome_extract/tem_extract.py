#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/16 14:00
# @Author  : yangmingming
# @Site    : 
# @File    : tem_extract.py
# @Software: PyCharm
import re
import os
import shutil
import random
import pandas as pd


class TemExtract(object):
    def __init__(self):
        pass

    def extract(self, src_folder, dest_folder, info: dict):
        """
        抽取项目的样例
        :param src_folder:项目
        :param dest_folder: 样例目的文件夹
        :param info: set抽取的人数，content_num 抽取的txt, wav, metadata套数
        :return: None
        """
        # 创建项目名称文件夹
        item_folder = os.path.join(dest_folder, os.path.split(src_folder)[1])
        if not os.path.exists(item_folder):
            os.makedirs(item_folder)

        data = random.sample(os.listdir(src_folder), info.get("set", 1))  # 随机抽取指定人数的数据
        for person in data:
            person_path = os.path.join(src_folder, person)
            all_txt = [os.path.join(root, file) for root, dirs, files in os.walk(person_path) for file in files if
                       file.endswith("txt")]  # 获取所有txt文件
            tem_path = os.path.split(all_txt[0])

            dest_person_path = tem_path[0].replace(src_folder, item_folder)  # 选取一个txt文件创建目标文件夹
            if not os.path.exists(dest_person_path):
                os.makedirs(dest_person_path)  # 在目的文件夹创建选取人文件夹

            content_extract = random.sample(all_txt, info.get("content_num"))  # 选取txt 内容
            for txt_file in content_extract:
                txt_path = os.path.join(person_path, txt_file)
                dest_txt_path = txt_path.replace(src_folder, item_folder)
                shutil.copyfile(txt_path, dest_txt_path)

                wav_path = os.path.join(person_path, txt_file.replace("txt", "wav"))
                dest_wav_path = wav_path.replace(src_folder, item_folder)
                shutil.copyfile(wav_path, dest_wav_path)

                meta_path = os.path.join(person_path, txt_file.replace("txt", "metadata"))
                dest_meta_path = meta_path.replace(src_folder, item_folder)
                shutil.copyfile(meta_path, dest_meta_path)

    def count_info(self, project_folder):
        """
        统计抽取样例的信息
        :param project_folder: 抽取的项目样例文件夹
        :return:
        """
        df = pd.DataFrame()
        for root, dirs, files in os.walk(project_folder):
            for file in files:
                if file.endswith("txt"):
                    file_path = os.path.join(root, file)
                    item_path_info = re.sub(".*?extract", "", file_path)
                    item_info = item_path_info.split("\\")
                    with open(file_path, 'r', encoding='utf8') as f:
                        content = f.read()
                    df = df.append(
                        {"国家说英语文件夹名": item_info[1], "抽取id号": item_info[2], "文本": content,
                         "文本文件名": item_info[-1]}, ignore_index=True)
        df.to_excel('info.xlsx', index=False)

    def run(self):
        """
        抽取逻辑控制，在这里调试
        :return:
        """
        # item_path_list = [
        #     "G:\给明明\中国人英语",
        #     "G:\给明明\俄罗斯英语",
        #     "G:\给明明\葡萄牙英语",
        #     "G:\给明明\日本英语",
        #     "G:\给明明\西班牙英语",
        # ]

        # item_path_list = [
        #     "G:\给明明\加拿大英语",
        #     "G:\给明明\印度英语",
        #     "G:\给明明\美式英语",
        #     "G:\给明明\英式英语",
        #     "G:\给明明\韩国英语",
        # ]

        # dest_folder = r'C:\Users\Administrator\Desktop\extract'  # 抽取demo存放的路径
        # for item in item_path_list:
        #     info = {"set": 1, "content_num": 20}
        #     self.extract(item, dest_folder, info)

        self.count_info(r"C:\Users\Administrator\Desktop\extract")


if __name__ == '__main__':
    te = TemExtract()
    te.run()
