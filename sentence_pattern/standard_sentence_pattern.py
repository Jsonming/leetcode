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


class StandardSentence(object):
    def __init__(self):
        pass

    def run(self):
        """
        逻辑控制函数
        :return:
        """
        original_folders = [
            "D:\Workspace\workscript\sentence_pattern\Weather-31500",
            'D:\Workspace\workscript\sentence_pattern\天气Weather-31500'
        ]
        sum_s = pd.Series()
        for original_folder in original_folders:
            for root, dirs, files in os.walk(original_folder):
                for file in files:
                    if "modified" not in file and "unique" not in "file":
                        file_path = os.path.join(root, file)
                        data_df = self.read_original_data(file_path)
                        new_df = self.gen_new_data(data_df)
                        # new_file_name = file_path.replace(".xlsx", "_modified.xlsx")
                        # new_df.to_excel(new_file_name, index=False)

                        # new_file_name = file_path.replace(".xlsx", "_unique.xlsx")
                        # new_df.drop_duplicates(subset=["text_style"], keep='first', inplace=False)
                        # new_df.to_excel(new_file_name, index=False)
                        text_style = new_df["text_style"].drop_duplicates()
                        # text_style.to_excel(new_file_name, index=False)
                        sum_s = sum_s.append(text_style)
        t_s = sum_s.drop_duplicates()
        t_s.to_excel("text_style.xlsx", index=False)

    def gen_new_data(self, df):
        """
        处理df 中text 文本生成新的df
        :param df:
        :return:
        """
        new_text = []

        for index, row in df.iterrows():
            text = row.get("text")
            if not text:
                text = row.get("Text")
            if text is np.nan:
                text = ""

            try:
                time = row.get("time")
                if time is not np.nan and time:
                    text = text.replace(time, "{time}")
            except Exception as e:
                delta = datetime.timedelta(time - 43640)
                base_date = datetime.date(2020, 6, 24)
                real_date = base_date + delta
                str_date = "{}月{}日".format(real_date.month, real_date.day)
                text = text.replace(str_date, "{time}")

            festival = row.get("festival")
            if festival is not np.nan and festival:
                text = text.replace(festival, "{festival}")

            province = row.get("province")
            if province is not np.nan and province:
                text = text.replace(province, "{province}")

            state = row.get("state")
            if state is not np.nan and state:
                text = text.replace(state, "{state}")

            city = row.get("city")
            if city is not np.nan and city:
                text = text.replace(city, "{city}")

            country = row.get("country")
            if country is not np.nan and country:
                text = text.replace(country, "{country}")

            county = row.get("county")
            if county is not np.nan and county:
                text = text.replace(county, "{county}")

            temperatureUnit = row.get("temperatureUnit")
            if temperatureUnit is not np.nan and temperatureUnit:
                text = text.replace(temperatureUnit, "{temperatureUnit}")

            new_text.append(text)
        new_df = df.copy()
        new_df["text_style"] = new_text
        return new_df

    def read_original_data(self, file_path):
        """
        读取原始数据
        :return:
        """
        original_df = pd.read_excel(file_path, header=None)
        new_head = original_df.iloc[:3, :].fillna(method='ffill')
        new_df = original_df.iloc[3:, :]
        new_df.columns = new_head.iloc[2]

        return new_df


if __name__ == '__main__':
    ss = StandardSentence()
    ss.run()
