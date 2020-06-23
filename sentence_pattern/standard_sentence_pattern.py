#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/13 11:24
# @Author  : yangmingming
# @Site    : 
# @File    : standard_sentence_pattern.py
# @Software: PyCharm
import os
import pandas as pd
import numpy as np
import datetime
import copy


class StandardSentence(object):
    def __init__(self):
        pass

    def run(self):
        """
        逻辑控制函数
        :return:
        """
        original_folders = [
            # "D:\Workspace\workscript\sentence_pattern\Weather-31500",
            # 'D:\Workspace\workscript\sentence_pattern\天气Weather-31500'
            'D:\Workspace\workscript\sentence_pattern\数据堂-中英语料-20万条-20200424\中文语料-10万条',
            'D:\Workspace\workscript\sentence_pattern\数据堂-中英语料-20万条-20200424\英文语料-10万条'
        ]

        for original_folder in original_folders:
            folder_name = original_folder.split("\\")[-1]
            sum_df, sum_text_df = pd.DataFrame(), pd.DataFrame()
            for root, dirs, files in os.walk(original_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    data_df = self.read_original_data(file_path)
                    new_df = self.gen_new_data(data_df)

                    if not os.path.exists("./res"):
                        os.makedirs("./res")

                    new_file_name = file.replace(".xlsx", "_unique.xlsx")
                    text_df = new_df.drop_duplicates(subset=["text"], keep='first', inplace=False)  # 按照句子文件内去重
                    # sum_text_df = sum_text_df.append(text_df.copy(), ignore_index=True)

                    text_style_df = new_df.drop_duplicates(subset=["text_style"], keep='first', inplace=False)  # 句式去重
                    text_style_df.to_excel("./res/{}".format(new_file_name), index=False)
                    # sum_df = sum_df.append(text_style_df.copy(), ignore_index=True)

            # sum_df.to_excel("{}_org_text_style.xlsx".format(folder_name), index=False)
            # sum_df.drop_duplicates(subset=["text_style"], keep='first', inplace=True)
            # sum_df.to_excel("{}_uni_text_style.xlsx".format(folder_name), index=False)
            #
            # sum_text_df.drop_duplicates(subset=["text"], keep='first', inplace=True)
            # sum_text_df.to_excel("{}_uni_text.xlsx".format(folder_name), index=False)

    def gen_new_data(self, df):
        """
        处理df 中text 文本生成新的df
        :param df:
        :return:
        """
        new_df = pd.DataFrame()

        def tran_time(time_int):
            delta = datetime.timedelta(time_int - 43640)
            base_date = datetime.date(2020, 6, 24)
            real_date = base_date + delta
            str_date = "{}月{}日".format(real_date.month, real_date.day)
            return str_date

        for index, row in df.iterrows():
            text = row.get("text")
            if text is not np.nan and text:
                single_info = pd.Series()
                single_info = single_info.append(row)
                text_content = copy.deepcopy(text)
                try:
                    repl_field = row["intention":"国家"][1:-1]
                except Exception as e:
                    repl_field = row["text":"国家"][1:-1]
                finally:
                    for key, value in repl_field.items():
                        if key == "time":
                            if type(value) is int:
                                value = tran_time(value)
                            if type(value) is float:
                                value = str(value)
                        elif key in ["phoneNumber", 'number', 'albumName', 'songName', 'extremeValue']:
                            value = str(value)
                        elif key == "percent" or key == "precent":
                            value = "{}%".format(value * 100)

                        if value is not np.nan and value:
                            text_content = text_content.replace(value, "{" + "{}".format(key) + "}")
                    single_info["text_style"] = text_content
                new_df = new_df.append(single_info, ignore_index=True)
        return new_df

    def read_original_data(self, file_path):
        """
        读取原始数据
        :return:
        """
        original_df = pd.read_excel(file_path, header=None)
        new_head = original_df.iloc[:3, :].copy().fillna(method='ffill')
        new_df = original_df.iloc[3:, :].copy()
        new_df.columns = new_head.iloc[2]
        new_df.dropna(axis=1, how="all", inplace=True)
        new_df.dropna(axis=0, how="all", inplace=True)
        try:
            df = new_df.loc[:, :"国家"].copy()
        except KeyError as e:
            print(file_path)
            raise e
        else:
            return df


if __name__ == '__main__':
    ss = StandardSentence()
    ss.run()



