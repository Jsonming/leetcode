#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/20 11:24
# @Author  : yangmingming
# @Site    : 
# @File    : phonetic_standard.py
# @Software: PyCharm
import re
from CommenScript.update_data.update_txt import strQ2B


class PhoneticStandard(object):
    def __init__(self):
        pass

    def view_phonetic_data(self, file):
        """
        查看音标数据
        :param file:
        :return:
        """
        with open(file, 'r', encoding='utf8')as f:
            for line in f:
                data = line.strip().split("\t")
                print(data)

    def process_phonetic(self, phonetic):
        """
        处理修改音标
        :param phonetic:
        :return:
        """
        en_phonetic_charactor = phonetic.replace('"', '')
        if en_phonetic_charactor:
            en_phonetic_charactor = en_phonetic_charactor.replace("]", '').replace("[", '')  # 删除左右中括号

            en_phonetic_charactor = en_phonetic_charactor.replace("英", '').replace("美", '')  # 删除出现"英"， "美"
            en_phonetic_charactor = en_phonetic_charactor.replace("/", '')  # 删除出现"/"
            en_phonetic_charactor = strQ2B(en_phonetic_charactor)

            if ";" in en_phonetic_charactor:
                en_phonetic_charactor = en_phonetic_charactor.split(";")[0]  # 有;分隔情况，只要第一部分

            if "-" in en_phonetic_charactor:
                en_phonetic_charactor = en_phonetic_charactor.split(" ")[0].rstrip(
                    ",")  # 有-替换的情况，空格前部分表示真实音标

            en_phonetic_charactor = re.sub("\(.*?\)", "", en_phonetic_charactor)  # 替换掉小括号的内容
            en_phonetic_charactor = en_phonetic_charactor.replace("'", 'ˈ')  # 替换单引号表示重音的情况
            en_phonetic_charactor = en_phonetic_charactor.replace(",", 'ˌ')  # 替换逗号表示次重音的情况
            en_phonetic_charactor = en_phonetic_charactor.replace(":", 'ː')  # 替换音标分号

            en_phonetic_charactor = en_phonetic_charactor.replace("əː", 'ɜː')  # 字符替换部分
            en_phonetic_charactor = en_phonetic_charactor.replace("oʊ", 'əʊ')  # 字符替换部分
            en_phonetic_charactor = en_phonetic_charactor.replace("ɒ", 'ɔ')  # 字符替换部分
            en_phonetic_charactor = en_phonetic_charactor.replace("ɛ", 'e')  # 字符替换部分
            en_phonetic_charactor = en_phonetic_charactor.replace("ε", 'e')  # 字符替换部分
            en_phonetic_charactor = en_phonetic_charactor.replace("g", 'ɡ')  # 字符替换部分
        return en_phonetic_charactor

    def process_all_character(self, file):
        """
        数据预处理
        :param file: 文件名
        :return:
        """
        re_repr = "[iː|ɜː|ɔː|uː|ɑː|eɪ|aɪ|ɔɪ|aʊ|əʊ|ɪə|eə|ʊə|tʃ|tr|ts|dʒ|dr|dz|ɑ|i|ə|ɔ|ʊ|ʌ|e|æ|p|t|k|f|s|θ|ʃ|b|d|ɡ|v|z|ð|ʒ|m|n|ŋ|h|r|l|w|j|ˈ|ˌ]"
        with open(file, 'r', encoding='utf8')as f:
            for line in f:
                word, show_word, en_phonetic, am_phonetic = line.strip().split("\t")
                if "-" not in word:  # 客户不要含有-的连接词
                    en_phonetic_charactor = self.process_phonetic(en_phonetic)
                    am_phonetic_charactor = self.process_phonetic(am_phonetic)

                    flg = re.sub(re_repr, "", am_phonetic_charactor.replace(" ", ''))
                    if flg:
                        print(word, show_word, en_phonetic_charactor, am_phonetic_charactor)
                        print(flg)

    def run(self):
        """
        程序逻辑入口
        :return:
        """
        phonetic_src = r"youdao_word.tsv"
        # self.view_phonetic_data(phonetic_src)   # 查看一下数据
        self.process_all_character(phonetic_src)  # 处理一下所有字符


if __name__ == '__main__':
    ps = PhoneticStandard()
    ps.run()
