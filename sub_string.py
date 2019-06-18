#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/17 11:01
# @Author  : yangmingming
# @Site    : 
# @File    : sub_string.py
# @Software: PyCharm


def string_substring(parent_string):
    substring = []
    for i in range(len(parent_string)):
        for j in range(i + 1, len(parent_string) + 1):
            substring.append(parent_string[i:j])
    return substring


