#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/20 11:04
# @Author  : yangmingming
# @Site    : 
# @File    : new_process_data.py
# @Software: PyCharm
import asyncio
import os
import re
import time
import pypinyin
from multiprocessing import Pool
from collections import defaultdict


class NewProcessData(object):
    """
    新处理老数据脚本
    """

    def __init__(self):
        pass

    def check_chinese(self, file):
        """
        异步处理文件
        :param file:
        :return:
        """
        z = re.compile(u'[\u4e00-\u9fa5]')

        with open(file, 'r', encoding='utf8')as f, open("chinese.txt", 'a', encoding='utf8')as w_f:
            for line in f:
                if z.search(line):
                    w_f.write("\t".join([file, line]))

    def change_metadata(self, file):
        """
        修改metadata文件
        :param file:
        :return:
        """
        city_name = ['仙台', '新潟県', '広島', '宇都宮', '小金井市', '下野', '新潟市', '栃木市', '青森市', '四日市市', '東京都', '福岡', '埼玉', '冲绳', '东京',
                     '秋田', '宫城县', '甲府市', '岩手県', '埼玉県', '福岛', '北海道  札幌市', '岐阜県', '神奈川県', '愛知県', '枥木县', '鹿沼', '三重県', '广岛',
                     '静岡県', '大阪', '福岡県北九州市', '名古屋', '福冈', '神奈川', '東京', '埼玉县', '横滨']
        city_name_en = ["Sendai", "Niigata Prefecture", "Hiroshima ", "Utsunomiya ", "Koganei", "Shimono",
                        "Niigata City", "Tochigi City", "Aomori", "Yokkaichi", "Tokyo ", "Fukuoka ", "Saitama",
                        "Paperback", "Tokyo", "Akita ", "Miyagi Shiro", "Kofu City", "Iwate Prefecture ", "Saitama ",
                        "Fukushima", "Sapporo City, Hokkaido", "Gifu Prefecture ", "Kanagawa Prefecture ",
                        "Aichi prefecture", "Toshiro", "Kanuma", "Mie Prefecture ", "Island", "Shizuoka Prefecture ",
                        "Osaka", "Kitakyushu, Fukuoka Prefecture ", "Nagoya ", "Fukuoka", "Kanagawa", "Tokyo",
                        "Saitama", "Yokomari"]
        city_name_d = dict()
        for item in zip(city_name, city_name_en):
            city_name_d[item[0]] = item[1]

        with open(file, 'r+', encoding='utf8')as route_f:
            new_content = ""
            for line in route_f:
                if "ACC" in line:
                    file, content = line.strip().split("\t")
                    if content in city_name:
                        new_line = "ACC" + "\t" + city_name_d[content] + "\n"
                    else:
                        new_line = line
                elif "SCC" in line:
                    new_line = line.replace("日本", "Quiet")
                elif "CCD" in line:
                    new_line = line.replace("日语", "Japanese")
                elif "QNT" in line:
                    new_line = line.replace("无压缩", "")
                elif "BIR" in line:
                    new_line = line.replace("日本", "Japan")
                elif "NCH" in line:
                    new_line = line.replace("单声道", "1")
                elif "REP" in line:
                    new_line = line.replace("室内", "indoor")
                else:
                    new_line = line
                new_content += new_line
            route_f.seek(0)
            route_f.truncate()
            route_f.write(new_content)

    def tran_new_metadata(self, file):
        """
        转换metadata
        :param file:
        :return:
        """
        sample_temp = """LHD	Datatang - v1.2
DBN	{DBN}
SES	{SES}
CMT	*** Speech Label Information ***
FIP	{DIR}
CCD	{CCD}
REP	{REP}
RED	{RED}
RET	{RET}
CMT	*** Speech Data Coding ***
SAM	{SAM}
SNB	{SNB}
SBF	{SBF}
SSB	{SSB}
QNT	{QNT}
NCH	{NCH}
CMT	*** Speaker Information ***
SCD	{SCD}
SEX	{SEX}
AGE	{AGE}
ACC	{ACC}
ACT	{ACT}
BIR	{BIR}
CMT	*** Recording Conditions ***
SNQ	{SNQ}
MIP	{MIP}
MIT	{MIT}
SCC	{SCC}
CMT	*** Label File Body ***
LBD	{LBD}
LBR	{LBR}
LBO	{LBO}
CMT	*** Customized Label Body ***
SRA	{SRA}
EMO	{EMO}
ORS	{ORS}
"""
        meta = dict()
        with open(file, 'r+', encoding='utf8')as f:
            for line in f:
                line_content = line.strip()
                if line_content:
                    if len(line_content) == 3:
                        meta[line_content] = ''
                    else:
                        meta[line_content[:3]] = line_content[3:].strip()

            lbr = meta.get("LBR")
            if lbr:
                meta["LBR"] = lbr.split("\t")[-1]
            else:
                meta["LBR"] = ''
            dir = meta.get("DIR")
            if not dir:
                meta["DIR"] = meta.get("FIP")

            sex = meta.get("SEX")
            if sex:
                meta["SEX"] = sex.capitalize()

            sra = meta.get("SRA")
            if not sra:
                meta["SRA"] = ""
            EMO = meta.get("EMO")
            if not EMO:
                meta["EMO"] = ""
            ORS = meta.get("ORS")
            if not ORS:
                meta["ORS"] = ""
            meta["LBO"] = ""
            meta["ACC"] = "".join(pypinyin.lazy_pinyin(meta["ACC"])).capitalize()
            meta["ACT"] = "".join(pypinyin.lazy_pinyin(meta["ACT"].replace("地区", ""))).capitalize()
            meta["BIR"] = "".join(pypinyin.lazy_pinyin(meta["BIR"])).capitalize()
            new_content = sample_temp.format(**meta)
            f.seek(0)
            f.truncate()
            f.write(new_content)

    def async_executive(self, func, args):
        """
        多进程执行函数
        :param func: 函数
        :param args: 参数
        :return:
        """
        pool = Pool(processes=4)
        pool.map(func, args)
        pool.close()
        pool.join()

    def output_meta_contain_chinese(self, dest):
        """
        输出metadata中字段是中文
        :return:
        """
        file_set = set()
        if os.path.isfile(dest):
            with open(dest, 'r', encoding='utf8') as error_f:
                for line in error_f:
                    file = line.strip().split("\t")[0]
                    file_set.add(file)
        elif os.path.isdir(dest):
            for root, dirs, files in os.walk(dest):
                for file in files:
                    if file.endswith("metadata"):
                        file_path = os.path.join(root, file)
                        file_set.add(file_path)
        else:
            print("不知道参数是什么")

    def temp_process_file(self, file):
        """
        临时处理文件
        :param error_file:
        :return:
        """
        re_regr_one = re.compile("[\[]+.*?[]]+|[@~%]+|<.*?>")
        count_n = defaultdict(int)
        double_s = set()
        with open(file, 'r', encoding='utf8')as n_f:
            for line in n_f:
                file_name, content = line.strip().split("\t")
                # match_result = re.findall(re_regr_one, content)
                # if match_result:
                #     for item in match_result:
                #         print(item)
                #         count_n[item] += 1
                # new_content = re.sub("\[N]|\[T]|\[S]|\[P]", "", content)
                # if "]" in new_content or "[" in new_content:
                #     print(new_content)
                double_str = lambda x: ord(x) == 0x3000 or 0xFF01 <= ord(x) <= 0xFF5E
                for x in content:
                    if double_str(x):
                        double_s.add(x)

        print(double_s)

    def temp_process_project(self, project_path):
        """
        处理项目
        :return:
        """
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith("metadata"):
                    file_path = os.path.join(root, file)
                    self.tran_new_metadata(file_path)

    def run(self):
        """
        主要逻辑控制
        :return:
        """
        # error_file = "error_content_contains_chinese.txt"
        # self.output_meta_contain_chinese(error_file)

        error_file = r"C:\Users\Administrator\Desktop\中英混读三批所有数据\中英混读三批所有数据.txt"
        self.temp_process_file(error_file)

        # project_path = r"\\10.10.30.14\42HoursOfChineseChildrenSpeech"
        # self.temp_process_project(project_path)


if __name__ == '__main__':
    npd = NewProcessData()
    npd.run()
