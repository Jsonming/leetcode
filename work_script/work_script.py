#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/9 14:23
# @Author  : yangmingming
# @Site    : 
# @File    : work_script.py
# @Software: PyCharm
import pandas as pd
from common.db import SSDBCon


class WorkScript(object):
    """
    工作脚本文件
    """

    def process_data_format(self):
        """
        医疗数据格式化函数
        :return:
        """
        i = 0
        df = pd.DataFrame({"疾病类型": [], '对话ID': [], "角色类型（对话方）": [], "角色ID": [], "对话内容": [], "对话类型": []})
        with open('demo.txt', 'r', encoding='utf8')as f:
            for line in f:
                i += 1
                content = line.split("\t")
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
                        # content_text.append('<picture>')
                        # content_type.append("图片")
                        content_text.append('')
                        content_type.append("")

                data_dict = {"疾病类型": illness, '对话ID': case_id, "角色类型（对话方）": role, "角色ID": role_id, "对话内容": content_text,
                             "对话类型": content_type}
                item_df = pd.DataFrame(data_dict)
                df = df.append(item_df, ignore_index=True)
        df.to_excel("demo.xlsx", index=False, encoding="utf8")

    def insert_db_data(self):
        """
        将单词插入ssdb数据库中,用于并发抓取
        :return:
        """
        db = SSDBCon()
        file = r"D:\Workspace\workspace\work\English_word\commen_words.txt"
        with open(file, 'r', encoding="utf8")as f:
            for line in f:
                word = line.strip()
                db.insert_to_list("words", word)
        db.close()

    def run(self):
        """
        脚本执行函数， 每次的脚本作为一个函数，不再新开文件
        :return:
        """
        # self.process_data_format()
        self.insert_db_data()


if __name__ == '__main__':
    work = WorkScript()
    work.run()
