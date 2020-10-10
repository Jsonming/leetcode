#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/17 11:21
# @Author  : yangmingming
# @Site    : 
# @File    : tem.py
# @Software: PyCharm

import pandas as pd
import numpy as np
import os

folder = r"C:\Users\Administrator\Desktop\res"
for file in os.listdir(folder):
    file_path = os.path.join(folder, file)
    df = pd.read_excel(file_path)
    with open('tem.tsv', "a", encoding='utf8')as f:
        f.write("{}\t{}\n".format(file, df.shape[0]))
