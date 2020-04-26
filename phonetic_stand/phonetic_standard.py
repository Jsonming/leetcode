#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/20 11:24
# @Author  : yangmingming
# @Site    : 
# @File    : phonetic_standard.py
# @Software: PyCharm
import re
import os
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
                elif i < char_limit and phonetic_string[i + 1] == "u":
                    phonetic_charactor += "aʊ"
                    i += 1
                else:
                    phonetic_charactor += "a有问题"
            elif char == "t":
                if i < char_limit and phonetic_string[i + 1] == "ʃ":
                    phonetic_charactor += "tʃ"
                    i += 1
                elif i < char_limit and phonetic_string[i + 1] == "r":
                    phonetic_charactor += "tr"
                    i += 1
                elif i < char_limit and phonetic_string[i + 1] == "s":
                    phonetic_charactor += "ts"
                    i += 1
                else:
                    phonetic_charactor += "t"
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
                    phonetic_charactor += "ɔ"
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
                elif i < char_limit and phonetic_string[i + 1] == "ə":
                    phonetic_charactor += "ɪə"
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
                    phonetic_charactor += "əʊ"
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

    def process_all_character(self, file, res_file):
        """
        数据预处理
        :param file: 文件名
        :return:
        """
        if os.path.exists(res_file):
            os.remove(res_file)

        re_repr = "[iː|ɜː|ɔː|uː|ɑː|eɪ|aɪ|ɔɪ|aʊ|əʊ|ɪə|eə|ʊə|tʃ|tr|ts|dʒ|dr|dz|ɑ|i|ə|ɔ|ʊ|ʌ|e|æ|p|t|k|f|s|θ|ʃ|b|d|ɡ|v|z|ð|ʒ|m|n|ŋ|h|r|l|w|j|ˈ|ˌ]"
        with open(file, 'r', encoding='utf8')as f, open(res_file, 'a', encoding='utf8')as r_f:
            for line in f:
                data = line.strip().split("\t")
                if len(data) > 4:
                    word, show_word, en_phonetic, am_phonetic, uncertain_phonetic = data[0], data[1], \
                                                                                    data[2], data[3], data[4]
                else:
                    word, show_word, en_phonetic, am_phonetic = data[0], data[1], data[2], data[3]
                    uncertain_phonetic = '""'  # 没有其他读音， 抓取的时候跳转到其他页面没有抓到

                if "-" not in word:  # 客户不要含有-的连接词
                    en_phonetic_charactor = self.process_phonetic(en_phonetic)
                    am_phonetic_charactor = self.process_phonetic(am_phonetic)

                    en_flg = re.sub(re_repr, "", en_phonetic_charactor.replace(" ", '')).strip()
                    am_flg = re.sub(re_repr, "", am_phonetic_charactor.replace(" ", '')).strip()

                    if len(data) > 4:
                        uncertaion_charactor = self.process_phonetic(uncertain_phonetic)
                        un_flg = re.sub(re_repr, "", uncertaion_charactor.replace(" ", '')).strip()
                        if un_flg:
                            pass
                        else:
                            if uncertaion_charactor:
                                uncertaion_charactor = "[" + uncertaion_charactor + "]"
                            else:
                                uncertaion_charactor = '""'  # 抓到处理完成是空
                    else:
                        uncertaion_charactor = '""'

                    if en_flg or am_flg:
                        pass  # 匹配出不合法的字符，量特别少 舍弃
                    else:
                        if en_phonetic_charactor:
                            en_phonetic_charactor = "[" + en_phonetic_charactor + "]"
                        else:
                            en_phonetic_charactor = '""'
                        if am_phonetic_charactor:
                            am_phonetic_charactor = "[" + am_phonetic_charactor + "]"
                        else:
                            am_phonetic_charactor = '""'
                        new_phentic = "\t".join([word, show_word, en_phonetic, en_phonetic_charactor, am_phonetic,
                                                 am_phonetic_charactor, uncertain_phonetic, uncertaion_charactor])
                        r_f.write(new_phentic + "\n")

    def diff_old_data(self, old_data, result, out_file):
        """
        对标晓文已经处理的数据，
        与晓文相同的单词跟晓文的修改做对标，
        晓文没有修改的单词单独输出
        :param old_data:
        :param result:
        :return:
        """
        if os.path.exists(out_file):
            os.remove(out_file)

        old_df = pd.read_excel(old_data, index_col="单词")
        new_df = pd.read_csv(result, sep='\t', header=None, names=["单词", "查到的单词", "英音原始", "英音修改后",
                                                                   "美音原始", "美音修改后", "其他音标原始", "其他修改后"],
                             index_col="单词")
        new_res = new_df.loc[~(new_df.index.isin(old_df.index.to_list())),]
        res = new_res.fillna("")
        res["英音修改后长度差"] = res["英音修改后"].apply(lambda x: re.sub(r"[\]|\[]", '', x)).str.len() - res["英音原始"].apply(
            lambda x: re.sub(r"[\]|\[]|\(.*?\)", '', x)).str.len()
        res["美音修改后长度差"] = res["美音修改后"].apply(lambda x: re.sub(r"[\]|\[]", '', x)).str.len() - res["美音原始"].apply(
            lambda x: re.sub(r"[\]|\[]|\(.*?\)", '', x)).str.len()
        res["其他修改后长度差"] = res["其他修改后"].apply(lambda x: re.sub(r"[\]|\[]", '', x)).str.len() - res["其他音标原始"].apply(
            lambda x: re.sub(r"[\]|\[]|\(.*?\)", '', x)).str.len()

        # res.index = res.index.map(str.lower)
        sort_res = res.sort_index()
        sort_res.to_excel(out_file)

    def fusion_data(self, source):
        """
        融合数据
        :return:
        """
        youdao_result, baidu_result, bing_result, dict_result = source
        youdao_df = pd.read_excel(youdao_result, index_col="单词")
        baidu_df = pd.read_excel(baidu_result, index_col="单词")
        bing_df = pd.read_excel(bing_result, index_col="单词")
        dict_df = pd.read_excel(dict_result, index_col="单词")

        words, words_set = [], set()
        for item in [youdao_df, baidu_df, bing_df, dict_df]:
            for word in item.index.to_list():
                if word not in words_set:
                    words.append(word)

        if os.path.exists("result.txt"):
            os.remove("result.txt")

        with open("result.txt", 'a', encoding='utf8') as f:
            for word_s in words:
                try:
                    youdao_data = youdao_df.loc[word_s]
                except KeyError as e:
                    youdao_data = {}
                try:
                    baidu_data = baidu_df.loc[word_s]
                except KeyError as e:
                    baidu_data = {}
                try:
                    bing_data = bing_df.loc[word_s]
                except KeyError as e:
                    bing_data = {}
                try:
                    dict_data = dict_df.loc[word_s]
                except KeyError as e:
                    dict_data = {}

                data = {"待查单词": word_s, "其他音标": '', "其他音标来源": ""}
                show_word = youdao_data.get("查到的单词")
                if pd.isna(show_word):
                    data["查到的单词"] = "nan"
                else:
                    data["查到的单词"] = show_word

                other_phonetic = youdao_data.get("其他修改后")
                if other_phonetic and not pd.isna(other_phonetic):
                    data["其他音标"] = youdao_data.get("其他修改后")
                    data["其他音标来源"] = "有道"

                # 英式音标
                en_phonetic = youdao_data.get("英音修改后")
                if en_phonetic and not pd.isna(en_phonetic):
                    data["英音"] = en_phonetic
                    data["英音来源"] = "有道"
                else:
                    en_phonetic = baidu_data.get("英音修改后")
                    if en_phonetic and not pd.isna(en_phonetic):
                        data["英音"] = en_phonetic
                        data["英音来源"] = "百度"
                    else:
                        en_phonetic = bing_data.get("英音修改后")
                        if en_phonetic and not pd.isna(en_phonetic):
                            data["英音"] = en_phonetic
                            data["英音来源"] = "bing"
                        else:
                            en_phonetic = dict_data.get("英音修改后")
                            if en_phonetic and not pd.isna(en_phonetic):
                                data["英音"] = en_phonetic
                                data["英音来源"] = "海词"
                            else:
                                data["英音"] = ""
                                data["英音来源"] = ""

                # 美式音标
                en_phonetic = youdao_data.get("美音修改后")
                if en_phonetic and not pd.isna(en_phonetic):
                    data["美音"] = en_phonetic
                    data["美音来源"] = "有道"
                else:
                    en_phonetic = baidu_data.get("美音修改后")
                    if en_phonetic and not pd.isna(en_phonetic):
                        data["美音"] = en_phonetic
                        data["美音来源"] = "百度"
                    else:
                        en_phonetic = bing_data.get("美音修改后")
                        if en_phonetic and not pd.isna(en_phonetic):
                            data["美音"] = en_phonetic
                            data["美音来源"] = "bing"
                        else:
                            en_phonetic = dict_data.get("美音修改后")
                            if en_phonetic and not pd.isna(en_phonetic):
                                data["美音"] = en_phonetic
                                data["美音来源"] = "海词"
                            else:
                                data["美音"] = ""
                                data["美音来源"] = ""
                print(data)
                f.write("\t".join([data["待查单词"], data["查到的单词"], data["英音"], data["英音来源"],
                                   data["美音"], data["美音来源"], data["其他音标"], data["其他音标来源"]]) + "\n")

    def run(self):
        """
        程序逻辑入口
        :return:
        """
        # source_list = ["youdao", "baidu", "bing", "dict"]
        # for source in source_list:
        #     phonetic_src = r"{}_word.tsv".format(source)
        #     new_result = '{}_result.txt'.format(source)
        #     result_execl = "{}_result.xlsx".format(source)
        #     old_data = r'C:\Users\Administrator\Desktop\work_temp\百万发音词典\4万9单词.xlsx'
        #     self.process_all_character(phonetic_src, new_result)
        #     self.diff_old_data(old_data, new_result, result_execl)

        # source = ["youdao_result.xlsx", 'baidu_result.xlsx', 'bing_result.xlsx', 'dict_result.xlsx']
        # self.fusion_data(source)

        # df = pd.read_csv("result.txt", sep='\t', names=["待查单词", "查到的单词", "英音", "英音来源",
        #                                                 "美音", "美音来源", "其他音标", "其他音标来源"])
        # df.to_excel("result.xlsx", index=False)


if __name__ == '__main__':
    ps = PhoneticStandard()
    ps.run()
