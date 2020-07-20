#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/29 9:52
# @Author  : yangmingming
# @Site    : 
# @File    : process_temp.py
# @Software: PyCharm
import json
import datetime
import pandas as pd
from CommenScript.update_data.update_txt import strQ2B


class ProcessXiaowen(object):

    def json_to_tsv(self, file):
        """
        json结果转tsv文件
        :return:
        """
        with open(file, 'r', encoding='utf8')as f, open("data.txt", 'a', encoding='utf8')as data_f:
            for line in f:
                try:
                    file_name, res_json = line.strip().split("\t")
                    data_list = json.loads(res_json).get("data")
                except Exception as e:
                    pass
                else:
                    for json_id, item in enumerate(data_list):
                        gender = item.get("gender")
                        text = item.get("text").replace("\n", '')
                        speaker = item.get("speaker")
                        time = item.get("time")
                        data_f.write("{file_name}\t{json_id}\t{gender}\t{text}\t{speaker}\t{time}\n".format(**locals()))

    def process_error_file(self, error_file):
        """
        处理错误的文件
        :param error_file:
        :return:
        """
        file_name_flag, content_sum = "", ""
        with open(error_file, 'r', encoding='utf8')as f, open("data.txt", 'a', encoding='utf8')as data_f:
            for line in f:
                res = line.strip().split("\t")
                file_name = res[0].strip()
                content = " ".join(res[1:]).strip()
                if file_name != file_name_flag:
                    if content_sum:
                        data_list = json.loads(content_sum).get("data")
                        for json_id, item in enumerate(data_list):
                            gender = item.get("gender")
                            text = item.get("text").replace("\n", '')
                            speaker = item.get("speaker")
                            time = item.get("time")
                            data_f.write(
                                "{file_name_flag}\t{json_id}\t{gender}\t{text}\t{speaker}\t{time}\n".format(**locals()))

                        content_sum = ''
                content_sum += content
                file_name_flag = file_name

    def check_data(self, file):
        """
        检查文件
        :param file:
        :return:
        """
        with open(file, 'r', encoding='utf8')as f, open("error_time.txt", 'a', encoding='utf8')as w_f:
            for line in f:
                file_name, json_id, gender, text, speaker, time_s = line.strip().split("\t")
                print(file_name)

                if gender not in {"男", "女"}:
                    w_f.write(line)

                # special_symble = ['}', '{', '0', '2', '5', 'α', '1', '3', '6', '7', '9', '<', '>', 'Ω', 'β', 'π', 'Ⅱ']
                # flag = [True if item in text else False for item in special_symble]
                # if any(flag):
                #     w_f.write(line)
                #
                # new_text = text.replace("[N]", "")
                # if "[" in new_text or "]" in new_text or "【" in new_text or "】" in new_text:
                #     w_f.write(line)

                start_time, end_time = time_s.split("-")
                for item in [start_time, end_time]:
                    try:
                        item_time, microsecond = item.split(".")
                        hour, minute, second = item_time.split(":")
                        a = datetime.time(int(hour), int(minute), int(second), int(microsecond))
                    except Exception as e:
                        w_f.write(line)

    def merge_data(self):
        """
        合并数据
        :return:
        """
        info = dict()
        with open("temp.tsv", 'r', encoding='utf8')as f:
            for line in f:
                file_name, json_id, gender, text, speaker, time = line.strip().split("\t")
                info[(file_name, json_id)] = text

        with open("data.txt", 'r+', encoding='utf8')as data_f, open("new_data.txt", 'a', encoding='utf8')as new_data_f:
            for line in data_f:
                file_name, json_id, gender, text, speaker, time = line.strip().split("\t")
                if (file_name, json_id) in info:
                    text = info[(file_name, json_id)]
                text = strQ2B(text)
                new_data_f.write("\t".join([file_name, json_id, gender, text, speaker, time]) + "\n")

    def run(self):
        """
        逻辑控制
        :return:
        """
        json_file = r"json结果测试=.txt"
        # self.json_to_tsv(json_file)
        # self.process_error_file(r"error.txt")
        self.check_data(r"C:\Users\Administrator\Desktop\json结果测试=.txt")

        # self.merge_data()


if __name__ == '__main__':
    px = ProcessXiaowen()
    px.run()
