#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/30 11:27
# @Author  : yangmingming
# @Site    : 
# @File    : cookbook.py
# @Software: PyCharm
import time
import os


def transpose_two_dimensional_arrays(arr_1: list):
    """
        转换二维数组
    :param arr_1: 二维数组
    :return:
    """
    return [[row[i] for row in arr_1] for i in range(len(arr_1[0]))]


def string_translate(s: str):
    """
    多种字符串映射
    :param s:
    :return:
    """
    return s.translate(str.maketrans("abcxyz", "xyzabc"))


def int_to_roman(input):
    if not isinstance(input, int):
        raise TypeError("expected integer, got %s".format(input))
    if not 0 < input < 4000:
        raise ValueError("Argument must be between 1 and 3999")

    ints = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    nums = ("M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I")
    result = []

    for i in range(len(ints)):
        count = int(input / ints[i])
        result.append(nums[i] * count)
        input -= ints[i] * count
    return "".join(result)


def timeo(fun, n=10):
    """
    测试函数运行时间，判断效率
    :param fun:测试函数
    :param n:测试次数
    :return:
    """
    start = time.clock()
    for i in range(n): fun()
    end = time.clock()
    the_time = end - start
    return fun.__name__, the_time


def linecount_wc(file_name):
    """
    shell 方法统计行数
    :param file_name: 文件名
    :return:
    """
    return os.popen("wc -l {}".format(file_name)).read().split()[0]


def linecount_1(file_name):
    """
    第二种方法判断句子行数，
    :param file_name: 文件名
    :return:
    """
    return len(open(file_name, 'r', encoding='utf8').readlines())


def linecount_2(file_name):
    """
    第三种方法
    :param file_name:
    :return:
    """
    num = 0
    with open(file_name, 'r', encoding='utf8')as f:
        for line in f:
            num += 1
    return num


if __name__ == '__main__':
    # arr = [[1, 2], [3, 4]]
    # print(transpose_two_dimensional_arrays(arr))
    # translate_s = "abc123xyz"
    # res = string_translate(translate_s)
    # r = int_to_roman(2002)
    # print(r)
    file_name = r"英英剩余单词表.txt"
    # for f in linecount_wc, linecount_1, linecount_2:
    #     print(f.__name__, f(file_name))
    linecount_wc(file_name)
