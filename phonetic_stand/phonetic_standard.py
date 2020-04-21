#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/20 11:24
# @Author  : yangmingming
# @Site    : 
# @File    : phonetic_standard.py
# @Software: PyCharm
import re
import pandas as pd
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

    def charactor_sub(self, phonetic_string):
        """
        音标字符替换
        :param phonetic_string:
        :return:
        """
        phonetic_charactor = ''
        phonetic_string_longth, i = len(phonetic_string), 0
        char_limit = phonetic_string_longth - 1
        while i < phonetic_string_longth:
            char = phonetic_string[i]
            if char == "a":
                if i < char_limit and phonetic_string[i + 1] == "ː":
                    phonetic_charactor += "ɑː"
                    i += 1
                elif i < char_limit and phonetic_string[i + 1] == "ʊ":
                    phonetic_charactor += "aʊ"
                    i += 1
                elif i < char_limit and phonetic_string[i + 1] == "i":
                    phonetic_charactor += "aɪ"
                    i += 1
                elif i < char_limit and phonetic_string[i + 1] == "ɪ":
                    phonetic_charactor += "aɪ"
                    i += 1
                else:
                    print("a 有问题")
            elif char == "t":
                if i < char_limit and phonetic_string[i + 1] == "ʃ":
                    phonetic_charactor += "ɑː"
                    i += 1
                    phonetic_charactor += "tʃ"
                    i += 1
                elif i < char_limit and phonetic_string[i + 1] == "r":
                    phonetic_string += "tr"
                    i += 1
                elif i < char_limit and phonetic_string[i + 1] == "s":
                    phonetic_string += "ts"
                    i += 1
                else:
                    phonetic_string += "t"
            elif char == "d":
                if i < char_limit and phonetic_string[i + 1] == "ʒ":
                    phonetic_charactor += "dʒ"
                    i += 1
                elif i < char_limit and phonetic_string[i + 1] == "r":
                    phonetic_charactor += "dr"
                    i += 1
                elif i < char_limit and phonetic_string[i + 1] == "z":
                    phonetic_charactor += "dz"
                    i += 1
                else:
                    phonetic_charactor += "d"
            elif char == "e":
                if i < char_limit and phonetic_string[i + 1] == "ə":
                    phonetic_charactor += "eə"
                    i += 1
                elif i < char_limit and phonetic_string[i + 1] == "i":
                    phonetic_charactor += "eɪ"
                    i += 1
                elif i < char_limit and phonetic_string[i + 1] == "ɪ":
                    phonetic_charactor += "eɪ"
                    i += 1
                else:
                    phonetic_charactor += "e"
            elif char == "ɔ":
                if i < char_limit and phonetic_string[i + 1] == "ː":
                    phonetic_charactor += "ɔː"
                    i += 1
                elif i < char_limit and phonetic_string[i + 1] == "i":
                    phonetic_charactor += "ɔɪ"
                    i += 1
                elif i < char_limit and phonetic_string[i + 1] == "ɪ":
                    phonetic_charactor += "ɔɪ"
                    i += 1
                else:
                    phonetic_charactor = "ɔ"
            elif char == "ɪ":
                if i < char_limit and phonetic_string[i + 1] == "ə":
                    phonetic_charactor += "ɪə"
                    i += 1
                else:
                    phonetic_charactor += "i"
            elif char == "ʊ":
                if i < char_limit and phonetic_string[i + 1] == "ə":
                    phonetic_charactor += "ʊə"
                    i += 1
                else:
                    phonetic_charactor += "ʊ"
            elif char == "i":
                if i < char_limit and phonetic_string[i + 1] == "ː":
                    phonetic_charactor += "iː"
                    i += 1
                else:
                    phonetic_charactor += "i"
            elif char == "u":
                if i < char_limit and phonetic_string[i + 1] == "ː":
                    phonetic_charactor += "uː"
                    i += 1
                else:
                    phonetic_charactor += "ʊ"
            elif char == "ɜ":
                if i < char_limit and phonetic_string[i + 1] == "ː":
                    phonetic_charactor += "ɜː"
                    i += 1
                else:
                    phonetic_charactor += "ə"
            elif char == "o":
                if i < char_limit and phonetic_string[i + 1] == "u":
                    phonetic_charactor += "əʊ"
                    i += 1
                elif i < char_limit and phonetic_string[i + 1] == "ʊ":
                    phonetic_charactor += "əʊ"
                    i += 1
                else:
                    print("o 有问题")
            elif char == "ə":
                if i < char_limit and phonetic_string[i + 1] == "ː":
                    phonetic_charactor += "ɜː"
                    i += 1
                else:
                    phonetic_charactor += "ə"
            elif char == "ɛ":
                phonetic_charactor += "e"
            elif char == "ε":
                phonetic_charactor += "e"
            elif char == "ɒ":
                phonetic_charactor += "ɔ"
            elif char == "g":
                phonetic_charactor += "ɡ"
            else:
                phonetic_charactor += char
            i += 1

        return phonetic_charactor

    def process_phonetic(self, phonetic):
        """
        处理修改音标
        :param phonetic:
        :return:
        """
        phonetic_charactor = phonetic.replace('"', '')
        if phonetic_charactor:
            phonetic_charactor = phonetic_charactor.replace("]", '').replace("[", '')  # 删除左右中括号

            phonetic_charactor = phonetic_charactor.replace("英", '').replace("美", '')  # 删除出现"英"， "美"
            phonetic_charactor = phonetic_charactor.replace("/", '')  # 删除出现"/"
            phonetic_charactor = strQ2B(phonetic_charactor)

            if ";" in phonetic_charactor:
                phonetic_charactor = phonetic_charactor.split(";")[0]  # 有;分隔情况，只要第一部分

            if "-" in phonetic_charactor:
                phonetic_charactor = phonetic_charactor.split(" ")[0].rstrip(
                    ",")  # 有-替换的情况，空格前部分表示真实音标

            phonetic_charactor = re.sub("\(.*?\)", "", phonetic_charactor)  # 替换掉小括号的内容
            phonetic_charactor = phonetic_charactor.replace("'", 'ˈ')  # 替换单引号表示重音的情况
            phonetic_charactor = phonetic_charactor.replace("‘", 'ˈ')  # 替换单引号表示重音的情况
            phonetic_charactor = phonetic_charactor.replace("’", 'ˈ')  # 替换单引号表示重音的情况
            phonetic_charactor = phonetic_charactor.replace(",", 'ˌ')  # 替换逗号表示次重音的情况
            phonetic_charactor = phonetic_charactor.replace(":", 'ː')  # 替换音标分号

            # 有道出现的特殊音标，通过与百度词典对比，找出的映射
            phonetic_charactor = phonetic_charactor.replace("ɝ", 'ɜː')  # 替换音标分号
            phonetic_charactor = phonetic_charactor.replace("ɚ", 'ə')  # 替换音标分号

            phonetic_charactor = self.charactor_sub(phonetic_charactor)

        return phonetic_charactor

    def process_all_character(self, file):
        """
        数据预处理
        :param file: 文件名
        :return:
        """
        re_repr = "[iː|ɜː|ɔː|uː|ɑː|eɪ|aɪ|ɔɪ|aʊ|əʊ|ɪə|eə|ʊə|tʃ|tr|ts|dʒ|dr|dz|ɑ|i|ə|ɔ|ʊ|ʌ|e|æ|p|t|k|f|s|θ|ʃ|b|d|ɡ|v|z|ð|ʒ|m|n|ŋ|h|r|l|w|j|ˈ|ˌ]"
        with open(file, 'r', encoding='utf8')as f, open("result.txt", 'a', encoding='utf8')as r_f:
            for line in f:
                word, show_word, en_phonetic, am_phonetic = line.strip().split("\t")
                if "-" not in word:  # 客户不要含有-的连接词
                    en_phonetic_charactor = self.process_phonetic(en_phonetic)
                    am_phonetic_charactor = self.process_phonetic(am_phonetic)

                    en_flg = re.sub(re_repr, "", en_phonetic_charactor.replace(" ", '')).strip()
                    am_flg = re.sub(re_repr, "", am_phonetic_charactor.replace(" ", '')).strip()
                    if en_flg or am_flg:
                        pass  # 英式或美式
                    else:
                        if en_phonetic_charactor:
                            en_phonetic_charactor = "[" + en_phonetic_charactor + "]"
                        else:
                            en_phonetic_charactor = '""'
                        if am_phonetic_charactor:
                            am_phonetic_charactor = "[" + am_phonetic_charactor + "]"
                        else:
                            am_phonetic_charactor = '""'
                        new_phentic = "\t".join(
                            [word, show_word, en_phonetic, en_phonetic_charactor, am_phonetic, am_phonetic_charactor])
                        r_f.write(new_phentic + "\n")

    def diff_old_data(self, old_data, result):
        """
        对标晓文已经处理的数据，
        与晓文相同的单词跟晓文的修改做对标，
        晓文没有修改的单词单独输出
        :param old_data:
        :param result:
        :return:
        """
        old_df = pd.read_excel(old_data, index_col="单词")
        new_df = pd.read_csv(result, sep='\t', header=None, names=["单词", "查到的单词", "英音原始", "英音修改后", "美音原始", "美音修改后"],
                             index_col="单词")
        res = new_df.loc[~(new_df.index.isin(old_df.index.to_list())),]
        res.to_excel("res.xlsx")

    def run(self):
        """
        程序逻辑入口
        :return:
        """
        phonetic_src = r"youdao_word.tsv"
        # self.view_phonetic_data(phonetic_src)  # 查看一下数据
        self.process_all_character(phonetic_src)  # 处理一下所有字符
        #
        # old_data = r'C:\Users\Administrator\Desktop\work_temp\百万发音词典\4万9单词.xlsx'
        # new_result = 'result.txt'
        # self.diff_old_data(old_data, new_result)


if __name__ == '__main__':
    ps = PhoneticStandard()
    ps.run()
