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


if __name__ == '__main__':
    s = "dfgsabccbadfgs"
    result = longst_plalindrome(s)
    print(result)
