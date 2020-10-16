#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/15 20:14
# @Author  : yangmingming
# @Site    : 
# @File    : extract.py
# @Software: PyCharm
import os
import shutil

old = [r"\\10.10.8.123\刘晓东2\提取数据\陈丽芳\美式英语\202.3小时美式英语\data\category",
       r"\\10.10.8.123\刘晓东2\提取数据\陈丽芳\101.4小时美式英语\data\category"]

new = r"\\10.10.8.123\外国人说英语\美英\结果数据\1-16\data\category"

old_folder = set()
for old_i in old:
    for o_folder in os.listdir(old_i):
        old_folder.add(o_folder)

dest = r"\\10.10.8.123\刘晓东2\提取数据\陈丽芳\美式英语\美式英语1015"
for folder in os.listdir(new):
    if folder not in old_folder:
        folder_path = os.path.join(new, folder)
        dest_path = os.path.join(dest, folder)
        shutil.copytree(folder_path, dest_path)
