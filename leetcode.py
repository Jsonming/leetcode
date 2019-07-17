#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/16 9:32
# @Author  : yangmingming
# @Site    : 
# @File    : leetcode.py
# @Software: PyCharm
from itertools import product


class Solution:

    def letter_combinations(self, digits: str) -> list[str]:
        """
            第17题，根据手机九键的字幕排序，根据给定数字串生产字母可能的组合
        :param digits: 给出的数字串
        :return:
        """
        # digits_letter_maping = {
        #     '2': ['a', 'b', 'c'],
        #     '3': ['d', 'e', 'f'],
        #     '4': ['g', 'h', 'i'],
        #     '5': ['j', 'k', 'l'],
        #     '6': ['m', 'n', 'o'],
        #     '7': ['p', 'q', 'r', 's'],
        #     '8': ['t', 'u', 'v'],
        #     '9': ['w', 'x', 'y', 'z'],
        # }
        # result = []
        table = {'2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl', '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'}

        if not len(digits):
            return []

        result = []
        for x in digits:
            if not len(result):
                result.extend(list(table[x]))
            else:
                result = [old + new for old, new in product(result, table[x])]
        return result


if __name__ == '__main__':
    result = Solution()
    print(result.letter_combinations('239'))
