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


s = "abcabcbb"
max_length_substring(s)