#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/28 10:52
# @Author  : yangmingming
# @Site    : 
# @File    : word.py
# @Software: PyCharm

import nltk
from nltk.corpus import gutenberg, webtext

new_words = set()
words = webtext.words()
for word in words:
    if word.isalpha():
        # new_words.add(word)
        print(word)
# word_all = set()
# with open("English_word_all.tsv", 'r', encoding='utf8')as f:
#     for item in f:
#         word_all.add(item.strip().lower())
#
#
# with open("gutenbeg_diff.txt", 'a', encoding='utf8')as f:
#     for word in new_words:
#         if word.lower() not in word_all:
#             f.write("{}\n".format(word))
#             print(word)
