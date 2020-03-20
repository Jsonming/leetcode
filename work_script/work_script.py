#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/9 14:23
# @Author  : yangmingming
# @Site    : 
# @File    : work_script.py
# @Software: PyCharm
import pandas as pd

from common.db import MysqlCon


class WorkScript(object):
    """
    工作脚本文件
    """

    def process_data_format(self, input_file: str, output: str):
        """
        医疗数据格式化函数
        :return:
        """
        i = 0
        df = pd.DataFrame({"疾病类型": [], '对话ID': [], "角色类型（对话方）": [], "角色ID": [], "对话内容": [], "对话类型": []})
        with open(input_file, 'r', encoding='utf8')as f:
            for line in f:
                line = line.strip()
                if self.judge_content_complete(line):
                    i += 1  # 累加content条数

                    # 解析那内容
                    article_id, content = line.split("\t")[0], line.split("\t")[1:]
                    illness, case_id, role, role_id, content_text, content_type = [], [], [], [], [], []
                    for item in content[1:]:
                        illness.append(content[0])
                        case_id.append(i)

                        if "patient:" in item:
                            item = item.replace("patient:", "")
                            role.append("病人")
                            role_id.append("p_{}".format(i))
                        elif "doctor:" in item:
                            item = item.replace("doctor:", "")
                            role.append("医生")
                            role_id.append("d_{}".format(i))

                        if item:
                            content_text.append(item)
                            content_type.append("文本")
                        else:
                            content_text.append('<picture>')
                            content_type.append("图片")

                    # 构建dataframe
                    data_dict = {"疾病类型": illness, '对话ID': case_id, "角色类型（对话方）": role, "角色ID": role_id,
                                 "对话内容": content_text, "对话类型": content_type}
                    item_df = pd.DataFrame(data_dict)

                    # 导出到execl 文件
                    if i % 10000:
                        df = df.append(item_df, ignore_index=True)
                        with open('article_id.txt', "a", encoding='utf8') as a_f:
                            a_f.write(article_id + "\n")
                    else:
                        df = df.append(item_df, ignore_index=True)
                        df.to_excel("content_{}.xlsx".format(str(int(i / 10000))), index=False, encoding="utf8",
                                    engine='xlsxwriter')
                        df = pd.DataFrame(
                            {"疾病类型": [], '对话ID': [], "角色类型（对话方）": [], "角色ID": [], "对话内容": [], "对话类型": []})

    def count_data_space(self, input_file: str):
        """
        统计含有语音的数据
        :param input_file: 输入文件
        :return:
        """
        from collections import defaultdict

        illness_type = defaultdict(int)
        i = 0
        with open(input_file, 'r', encoding='utf8')as f:
            for line in f:
                content = line.strip()
                if self.judge_content_complete(content):
                    i += 1
                    illness = content.split("\t")[1]
                    illness_type[illness] += 1
                if i > 70000:
                    break

        return sorted(illness_type.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)

    def judge_content_complete(self, content):
        """
        查看对话的完整性
        :param content: 对话
        :return:
        """
        content = content.split("\t")
        for item in content[1:]:
            if "patient:" in item:
                item = item.replace("patient:", "")
            elif "doctor:" in item:
                item = item.replace("doctor:", "")
            if not item:
                return False
        return True

    def count_word_freq(self, dict_file, word_file):
        """
        统计词频 并将词频输入到mysql 中
        :return:
        """
        con = MysqlCon()

        # 制作词频表
        freq_dict = dict()
        with open(dict_file, 'r', encoding='utf')as d_f:
            for line in d_f:
                word, freq = line.strip().split()
                freq_dict[word] = freq

        # 根据单词表和词频表获取词频
        i = 1
        with open(word_file, 'r', encoding='utf8')as w_f:
            for line in w_f.readlines():
                word_id, word = line.strip().split()
                frequency = freq_dict.get(word)
                if not frequency:
                    frequency = freq_dict.get(word.lower())

                if frequency:
                    sql = "update English_word_phonetic set frequency={} where id={}".format(int(frequency), int(word_id))
                    con.db_cur.execute(sql)
                i += 1
                if i % 5000 == 0:
                    con.db_conn.commit()

        con.close()

    def run(self):
        """
        脚本执行函数， 每次的脚本作为一个函数，不再新开文件
        :return:
        """
        # input_file = r"dxy_content.tsv"
        # output_file = r"demo.xlsx"
        # self.process_data_format(input_file, output_file)
        # count_res = self.count_data_space(input_file)

        # 统计词频
        dict_file = r"wordfreq.txt"
        word_file = r"English_word.tsv"
        self.count_word_freq(dict_file, word_file)


if __name__ == '__main__':
    work = WorkScript()
    work.run()
