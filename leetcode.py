#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/16 9:32
# @Author  : yangmingming
# @Site    : 
# @File    : leetcode.py
# @Software: PyCharm
from itertools import product


class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def letter_combinations(self, digits: str):
        """
            第17题，根据手机九键的字幕排序，根据给定数字串生产字母可能的组合
        :param digits: 给出的数字串
        :return:
        """
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

    def four_sum(self, nums, target: int):
        """
            四数之和
        :param nums: 数字列表
        :param target: 目标值
        :return:
        """

    def remove_element_from_end(self, head, n):
        """
        :type head: ListNode
        :type n: int
        :rtype: ListNode
        """
        dummy = ListNode(-1)
        dummy.next = head
        fast = slow = dummy

        while n and fast:
            fast = fast.next
            n -= 1

        while fast.next and slow.next:
            fast = fast.next
            slow = slow.next

        slow.next = slow.next.next
        return dummy.next

    def is_valid(self, s: str) -> bool:
        """
            判断括号是否合法, 这里默认只有这个六个符号
        :param s:
        :return:
        """
        bracket_pair = {"}": "{", ")": "(", "]": "["}
        bracket_queue = []
        if s:
            for bracket in s:
                if bracket in bracket_pair.values():
                    bracket_queue.append(bracket)
                else:
                    if bracket_queue:
                        left_v = bracket_queue.pop()
                        if left_v != bracket_pair[bracket]:
                            return False
                    else:
                        return False
        if bracket_queue:
            return False
        else:
            return True

    def generate_parenthesis(self, n):
        """
        :type n: int
        :rtype: List[str]
        """
        res = set(['()'])
        for i in range(n - 1):
            tmp = set()
            for r in res:
                tmp.update(set([r[:j] + '()' + r[j:] for j in range(len(r))]))
            res = tmp
        return list(res)


if __name__ == '__main__':
    result = Solution()
    print(result.generate_parenthesis(3))
