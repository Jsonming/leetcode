#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/25 19:51
# @Author  : yangmingming
# @Site    : 
# @File    : process_sgcc_data.py
# @Software: PyCharm
import os
import json

import pandas as pd


class ProcessSGCC(object):
    def __init__(self):
        pass

    def process_result(self, src, dest):
        """
        修改文件文件json 格式修改为tsv 格式，并去重
        :param src: 源文件
        :param dest: 目的文件
        :return:
        """
        flags, projects = set(), []
        with open(src, 'r', encoding='utf8') as s_f:
            for line in s_f:
                item = json.loads(line.strip().strip(","))
                values = []
                for k, v in item.items():
                    values.append(v)
                flag = "\t".join(values[:3])
                if flag not in flags:
                    flags.add(flag)
                    projects.append(item)
        return projects

    def process_txt(self, file):
        """
        处理txt 文件中的数据
        :param file:
        :return:
        """
        with open(file, 'r', encoding="utf8") as f:
            line = f.readlines()[0].strip()
            titles = line.split("\t")
            flag = [True for title in titles if title in bid_name]
            if not flag:
                print(titles)

    def run(self):
        """
        处理抓取的数据
        :return:
        """
        # result 文件
        src = "result.txt"
        dest = "result.txt"
        projects = self.process_result(src=src, dest=dest)

        # 循环项目
        for project in projects:
            files = project.get("files")
            for file in files:
                file = os.path.join(os.getcwd() + "\\sgcc", file)
                if file.endswith("txt"):
                    self.process_txt(file)
                elif file.endswith("pdf"):
                    pass
                elif file.endswith("docx"):
                    pass
                elif file.endswith("doc"):
                    pass


if __name__ == '__main__':
    psgcc = ProcessSGCC()
    psgcc.run()
