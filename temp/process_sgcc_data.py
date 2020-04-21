#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/25 19:51
# @Author  : yangmingming
# @Site    : 
# @File    : process_sgcc_data.py
# @Software: PyCharm
import os
import json
import tabula
import pandas as pd


class ProcessSGCC(object):
    def __init__(self):
        pass

    def process_result(self, src, dest):
        """
        修改文件文件json 格式修改为tsv 格式，并去重
        :param src: 源文件
        :param dest: 目的文件
        :return:
        """
        flags, projects = set(), []
        with open(src, 'r', encoding='utf8') as s_f:
            for line in s_f:
                item = json.loads(line.strip().strip(","))
                values = []
                for k, v in item.items():
                    values.append(v)
                flag = "\t".join(values[:3])
                if flag not in flags:
                    flags.add(flag)
                    projects.append(item)
        return projects

    def process_txt(self, file):
        """
        处理txt 文件中的数据
        :param file:
        :return:
        """
        with open(file, 'r', encoding="utf8") as f:
            data = f.readlines()
            header_line = data[0].strip().split("\t")
            content = [item.strip().split("\t") for item in data[1:]]
            try:
                df = pd.DataFrame(content, columns=header_line)
                return df
            except Exception as e:
                return None

    def process_pdf(self, file):
        """
        处理pdf文件
        :param file:
        :return:
        """
        return tabula.read_pdf(file, pages="all")

    def run(self):
        """
        处理抓取的数据
        :return:
        """
        # result 文件
        src = "result.txt"
        dest = "result.txt"
        projects = self.process_result(src=src, dest=dest)

        # 循环项目
        df = pd.DataFrame(columns=["temp"])
        for project in projects:
            files = project.get("files")
            for file in files:
                file = os.path.join(os.getcwd() + "\\sgcc", file)
                url = r"http://ecp.sgcc.com.cn/html/news/{}/{}.html".format(*project.get("detail_id"))
                project_df = pd.DataFrame({
                    "company_name": project.get("company_name"),
                    "project_name": project.get("name"),
                    "time": project.get("time"),
                    "page_url": url
                }, pd.Index(range(1)))

                if file.endswith("txt"):
                    pass
                    # data = self.process_txt(file)
                    # if data is None:
                    #     pass
                    # else:
                    #     try:
                    #         df = pd.concat([df, data])
                    #     except Exception as e:
                    #         pass
                elif file.endswith("pdf"):
                    data = self.process_pdf(file)
                    if data is not None:
                        try:
                            data_df = pd.concat([project_df, data[0]])
                            df = pd.concat([df, data_df])
                        except Exception as e:
                            pass
                elif file.endswith("docx"):
                    pass
                elif file.endswith("doc"):
                    pass
        df.to_excel("temp.xlsx", index=None)


if __name__ == '__main__':
    psgcc = ProcessSGCC()
    psgcc.run()
