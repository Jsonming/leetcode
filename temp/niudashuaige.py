#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/10 11:10
# @Author  : yangmingming
# @Site    : 
# @File    : xiaoyu.py
# @Software: PyCharm
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas


def normfun(x, mu, sigma):
    pdf = np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) / (sigma * np.sqrt(2 * np.pi))
    return pdf


class ProcessData(object):
    def __init__(self):
        pass

    def plot_data(self, data, file):
        """
        数据绘图
        :param data:
        :return:
        """
        plt.style.use('seaborn-white')
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

        for item in data.columns:
            bins = np.linspace(min(data[item]), max(data[item]), 50)
            min_x, max_x = min(bins), max(bins)
            x = np.arange(min_x, max_x, 0.1)
            y = normfun(x, data[item].mean(), data[item].std())
            plt.plot(x, y, label=item)
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=len(data.columns),
                   ncol=3, mode="expand", borderaxespad=0.)
        plt.savefig(file.replace("xlsx", 'png'))

    def run(self):
        """
        主要逻辑控制
        :return:
        """
        for root, dirs, files in os.walk('./'):
            for file in files:
                if file.endswith("xlsx"):
                    data = pandas.read_excel(file)
                    self.plot_data(data, file)


if __name__ == '__main__':
    pd = ProcessData()
    pd.run()
