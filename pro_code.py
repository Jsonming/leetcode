#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/17 11:33
# @Author  : yangmingming
# @Site    : 
# @File    : max_length_substring.py
# @Software: PyCharm
from leetcode.sub_string import string_substring


def max_length_substring(parent_string):
    """
        无重复最长子串
    :return:
    """
    max_substring = ''
    substring = string_substring(parent_string)
    for string_ in substring:
        if len(string_) == len(list(set(string_))):
            if len(string_) > len(max_substring):
                max_substring = string_
    print(max_substring, len(max_substring))


def is_plalindrome(is_string):
    """
        判断字符串是否是回文字符串
    :return:
    """
    sign = True
    for i in range(len(is_string)):
        if is_string[i] != is_string[-(i + 1)]:
            sign = False
            break
    return sign


def longst_plalindrome(parent_string):
    """
        最长回文字符串暴力破解方法
    :param parent_string:
    :return:
    """
    longst_plalindrome = ""
    substring_list = string_substring(parent_string)
    for substring in substring_list:
        if is_plalindrome(substring) and len(substring) > len(longst_plalindrome):
            longst_plalindrome = substring

    return longst_plalindrome


def convert(s, n):
    """
        字符串Z字型排列，用列表嵌套列表的形式表示二维表格，以表格填充的形式组合出相应的字符串, numpy中有narray pandas
        中有DataFrame,都可以表示这样的形式
    :param s: 字符串
    :param n: Z 的高度
    :return:
    """

    table = [[" " for i in range(len(s))] for i in range(n)]  # 已知次数的循环 用for 比较合适，这是最近才理解的，以前只知道用
    row = 0
    for i, item in enumerate(s):
        if i < n:
            col = 0
        else:
            col = i - n + 1
        table[row][col] = item

        sing = (i // (n-1)) % 2
        if not sing:
            row += 1
        else:
            row -= 1

    return ''.join([''.join(item) for item in table]).replace(' ', '')


if __name__ == '__main__':
    s = "PAYPALISHIRING"
    result = convert(s, 3)
    print(result)
