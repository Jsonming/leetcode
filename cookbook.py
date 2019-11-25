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

    ints = (1000, 900, 500, 400, 100, 90, 50,40, 10, 9, 5, 4, 1)
    nums = ("M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I")
    result = []

    for i in range(len(ints)):
        count = int(input/ints[i])
        result.append(nums[i] * count)
        input -= ints[i] * count
    return "".join(result)


if __name__ == '__main__':
    # arr = [[1, 2], [3, 4]]
    # print(transpose_two_dimensional_arrays(arr))
    # translate_s = "abc123xyz"
    # res = string_translate(translate_s)
    r = int_to_roman(2002)
    print(r)