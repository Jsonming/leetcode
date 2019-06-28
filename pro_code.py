#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/17 11:33
# @Author  : yangmingming
# @Site    : 
# @File    : max_length_substring.py
# @Software: PyCharm
from leetcode.sub_string import string_substring
import heapq


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

        sing = (i // (n - 1)) % 2
        if not sing:
            row += 1
        else:
            row -= 1

    return ''.join([''.join(item) for item in table]).replace(' ', '')


def over_int(n: int):
    """
        翻转整数
    :param n:
    :return:
    """

    def over_str(s: str):
        s_t = s[::-1]
        for i, t in enumerate(s_t):
            if t != "0":
                s_t = s_t[i:]
                break
        return s_t

    if -2 ** 31 < n < (2 ** 31 - 1):
        str_int = str(n)
        sign_int = str_int[0]
        if sign_int != "-":
            r_int = over_str(str_int)
            if r_int:
                r_int = int(r_int)
        else:
            r_int = over_str(str_int[1:])
            if r_int:
                r_int = -int(r_int)
        return r_int
    else:
        return 0


def auto_turn(parent_string: str):
    process_string = parent_string.strip()
    result = 0
    if process_string:
        sign = parent_string[0]
        if sign == "-":
            for char in parent_string[1:]:
                if char.isdigit():
                    result = result * 10 + int(char)
                else:
                    break
            result = -result
        elif sign.isdigit():
            for char in parent_string:
                if char.isdigit():
                    result = result * 10 + int(char)
                else:
                    break
        if -2 ** 32 < result < 2 ** 32 - 1:
            pass
        else:
            result = 0
    return result


def palindromic_number(n):
    """
        不通过字符串的方法判断是不是回文数
    :param n: 原始数
    :return:
    """

    number_list = []
    if not isinstance(n, int):
        return False
    if n > 0 and n % 10:
        while n:
            number_list.append(n % 10)
            n = n // 10
    else:
        return False
    for i, item in enumerate(number_list):
        if item != number_list[-i - 1]:
            return False
    return True


def limit_turn(n):
    """
        返回一个最高为的值得罗马数字表示
    :param n: 数
    :return:
    """
    if 1000 <= n:
        return "M", n - 1000
    elif 900 <= n:
        return "CM", n - 900
    elif 500 <= n:
        return "D", n - 500
    elif 400 <= n:
        return "CD", n - 400
    elif 100 <= n:
        return "C", n - 100
    elif 90 <= n:
        return "XC", n - 90
    elif 50 <= n:
        return "L", n - 50
    elif 40 <= n:
        return "XL", n - 40
    elif 10 <= n:
        return "X", n - 10
    elif 9 <= n:
        return "IX", n - 9
    elif 5 <= n:
        return "V", n - 5
    elif 4 <= n:
        return "IV", n - 4
    elif 0 < n:
        return "I" * n, 0
    else:
        print("负数不能转")


def num_turn(n):
    """
        将数字转化为罗马数字
    :param n:
    :return:
    """
    result = ''
    while n:
        l_num, n = limit_turn(n)
        result += l_num

    print(result)


def longest_prefix_match(str_list: list):
    """
        获取字符串列表，得到最大子串
    :param str_list:
    :return:
    """
    length_heapq = []
    str_length = [len(item) for item in str_list]

    # 这个地方就是为了应用一下堆排序，有点图裤子放屁的意思
    for length in str_length:
        heapq.heappush(length_heapq, length)

    max_prefix = ''
    for i in range(1, length_heapq[0] + 1):
        temp_prefix = ''
        for element in str_list:
            sub_str = element[:i]
            if temp_prefix:
                if temp_prefix == sub_str:
                    pass
                else:
                    temp_prefix = ''
                    break
            else:
                temp_prefix = sub_str
        if temp_prefix:
            max_prefix = temp_prefix

    return max_prefix


if __name__ == '__main__':
    str_list = ["folw", 'fowersdfjklas', 'fowesdjklfa']
    result = longest_prefix_match(str_list)
    print(result)
