#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/24 10:31
# @Author  : yangmingming
# @Site    : ${SITE}
# @File    : test_pro_code.py
# @Software: PyCharm

from unittest import TestCase
from practice_questions.pro_code import palindromic_number


class TestLeetCode(TestCase):
    def test_palindromic_number(self):
        # self.fail()
        self.assertEqual(palindromic_number(-121), False)
        self.assertEquals(palindromic_number(1.1), False)
        self.assertEqual(palindromic_number(121), True)
