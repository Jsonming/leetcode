#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/12 15:07
# @Author  : yangmingming
# @Site    : 
# @File    : ekma.py
# @Software: PyCharm

# 导入模块
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def tran(data: list):
    """
    数据转换
    :param data:
    :return:
    """
    tem_data = []
    for item in data:
        if item < 54:
            tem_data.append(27)
        elif item < 104:
            tem_data.append(77)
        elif item < 154:
            tem_data.append(127)
        elif item < 204:
            tem_data.append(177)
        elif item < 254:
            tem_data.append(227)
        else:
            tem_data.append(277)

    return tem_data


data = pd.read_excel("数据.xlsx")
new_data = data.dropna()

hc = new_data["VOC小时浓度(ug/m3)"]
no = new_data['NOx']
o3 = new_data['实际O3浓度']
x = hc.to_list()
y = no.tolist()
z = o3.tolist()
z = tran(z)
print(z)
Z = np.zeros([len(x), len(y)])
for i, _x in enumerate(x):
    for j, _j in enumerate(y):
        if i == j:
            Z[i][j] = z[i]

X, Y = np.meshgrid(x, y)  # 将原始数据变成网格数据形式
plt.contour(X, Y, Z)
plt.show()
