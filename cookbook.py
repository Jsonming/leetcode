#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/30 11:27
# @Author  : yangmingming
# @Site    : 
# @File    : cookbook.py
# @Software: PyCharm


def transpose_two_dimensional_arrays(arr_1: list):
    """
        转换二维数组
    :param arr_1: 二维数组
    :return:
    """
    return [[row[i] for row in arr_1] for i in range(len(arr_1[0]))]


if __name__ == '__main__':
    arr = [[1, 2], [3, 4]]
    print(transpose_two_dimensional_arrays(arr))

