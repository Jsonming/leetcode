#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/20 11:04
# @Author  : yangmingming
# @Site    : 
# @File    : new_process_data.py
# @Software: PyCharm
import asyncio
import os
import re
import time
from multiprocessing import Pool


class NewProcessData(object):
    """
    新处理老数据脚本
    """

    def __init__(self):
        pass

    def check_chinese(self, file):
        """
        异步处理文件
        :param file:
        :return:
        """
        z = re.compile(u'[\u4e00-\u9fa5]')

        with open(file, 'r', encoding='utf8')as f, open("chinese.txt", 'a', encoding='utf8')as w_f:
            for line in f:
                if z.search(line):
                    w_f.write("\t".join([file, line]))

    def output_meta_contain_chinese(self, dest):
        """
        输出metadata中字段是中文
        :return:
        """
        file_set = set()
        if os.path.isfile(dest):
            with open(dest, 'r', encoding='utf8') as error_f:
                for line in error_f:
                    file = line.strip().split("\t")[0]
                    file_set.add(file)
        elif os.path.isdir(dest):
            for root, dirs, files in os.walk(dest):
                for file in files:
                    if file.endswith("metadata"):
                        file_path = os.path.join(root, file)
                        file_set.add(file_path)
        else:
            print("不知道参数是什么")

        meta_files = list(file_set)
        pool = Pool(processes=4)
        pool.map(self.check_chinese, meta_files)
        pool.close()
        pool.join()

    def temp_process_file(self, error_file):
        """
        临时处理文件
        :param error_file:
        :return:
        """
        tem = set()
        with open(error_file, 'r', encoding='utf8')as error_f:
            for line in error_f:
                try:
                    file, field, content = line.strip().split("\t")
                except Exception as e:
                    pass

                tem.add(field)
        print(tem)

    def run(self):
        """
        主要逻辑控制
        :return:
        """
        # error_file = "error_content_contains_chinese.txt"
        # self.output_meta_contain_chinese(error_file)

        error_file = "chinese.txt"

        self.temp_process_file(error_file)


if __name__ == '__main__':
    npd = NewProcessData()
    npd.run()
