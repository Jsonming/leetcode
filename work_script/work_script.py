#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/9 14:23
# @Author  : yangmingming
# @Site    : 
# @File    : work_script.py
# @Software: PyCharm
import collections
import json
import os

import MeCab
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
                    sql = "update English_word_phonetic set frequency={} where id={}".format(int(frequency),
                                                                                             int(word_id))
                    con.db_cur.execute(sql)
                i += 1
                if i % 5000 == 0:
                    con.db_conn.commit()

        con.close()

    def process_metadate(self, work_path):
        """
        处理data文件
        :param work_path:
        :return:
        """
        new_content = ""
        for root, dirs, files in os.walk(work_path):
            for file in files:
                if file.endswith("metadata"):
                    file_name = os.path.join(root, file)
                    with open(file_name, 'r+', encoding='utf8') as f:
                        for line in f:
                            pass

                    # os.remove(file_name)
                    # with open(file_name, 'w', encoding='utf8') as f:
                    #     f.write(new_content)

    def folder_rename(self, folder):
        """
        闽南语文件夹重名
        :param folder:
        :return:
        """
        i = 0
        for parent_folder in os.listdir(folder):
            parent_folder_path = os.path.join(folder, parent_folder)
            for sub_folder in os.listdir(parent_folder_path):
                i += 1
                new_name = "G" + str(i).zfill(4)
                os.rename(os.path.join(parent_folder_path, sub_folder),
                          os.path.join(parent_folder_path, new_name))  # 子文件夹重命名
                print(sub_folder, "has been renamed successfully! New name is: ", new_name)  # 输出提示

    def file_rename(self, parent_path):
        """
        修改文件名，根据生成的文件批次修改文件
        :param parent_path:
        :return:
        """
        for sub_folder in os.listdir(parent_path):
            inner_path = os.path.join(sub_folder, parent_path)
            for p_name in os.listdir(inner_path):
                p_path = os.path.join(inner_path, p_name)
                for session in os.listdir(p_path):
                    session_path = os.path.join(p_path, session)
                    for file in os.listdir(session_path):
                        if file.startswith("T"):
                            new_name = p_name + file[10:]
                            os.rename(os.path.join(session_path, file), os.path.join(session_path, new_name))
                            print(new_name)

    def read_metadata(self, file) -> dict:
        """
        解析metadata数据
        :param file: metadata 文件
        :return: metadata 的字典
        """
        infos = collections.OrderedDict()
        with open(file, 'r', encoding='utf8')as f:
            for line in f:
                info = line.strip().split('\t')
                if len(info) != 2:
                    info = line.strip().split(' ')
                if len(info) == 2:
                    k, v = info
                    infos.update({k: v})
        return infos

    def write_meta(self, meta: dict, meta_file: str):
        """
        写入metadata文件
        :param meta:
        :param meta_file:
        :return:
        """
        lines = [k + "\t" + v for k, v in meta.items()]
        with open(meta_file, 'w', encoding='utf8') as f:
            f.write("\n".join(lines))

    def fixed_metadata(self, folder):
        """
        修改metadata 替换统一批次
        :param folder:
        :return:
        """
        # for p_name in os.listdir(folder):
        #     p_path = os.path.join(folder, p_name)
        #
        #     for root, dirs, files in os.walk(p_path):
        #         for file in files:
        #             if file.endswith("metadata"):
        #                 file_path = os.path.join(root, file)
        #                 p_num = file_path.split("\\")[-3]
        #                 print(p_num)
        #
        #                 lines = []
        #                 with open(file_path, 'r', encoding='utf8') as r_f:
        #                     for line in r_f:
        #                         if "SES" in line or "SCD" in line:
        #                             t_name = line.split()[0]
        #                             new_line = t_name + "\t" + p_num
        #                         elif "DIR" in line:
        #                             t_name = line.split()[0]
        #                             new_line = t_name + "\t" + "\\".join(file_path.split("\\")[-5:])
        #                         elif "SRC" in line:
        #                             t_name = line.split()[0]
        #                             new_line = t_name + "\t" + ".".join(file_path.split("\\")[-2:])
        #                         else:
        #                             new_line = line.strip()
        #                         lines.append(new_line)
        #
        #                 with open(file_path, 'w', encoding='utf8') as w_f:
        #                     w_f.write("\n".join(lines))

        # 修改性别和年龄信息，由于传入的文件夹比较层次比较深，
        print(folder)
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith("metadata"):
                    file_path = os.path.join(root, file)
                    lines = []
                    with open(file_path, 'r', encoding='utf8') as r_f:
                        for line in r_f:
                            if "SES" in line:
                                t_name = line.split()[0]

    def temp_one(self, path):
        """
        临时处理文件
        :param file:
        :return:
        """
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith("metadata"):
                    file_path = os.path.join(root, file)
                    # print(file_path)

                    content = ''
                    with open(file_path, 'r', encoding='utf8')as f:
                        for line in f:
                            if "BIR" in line:
                                type_name = line.strip().split("\t")
                                if len(type_name) == 2:
                                    content += line
                                elif len(type_name) == 1:
                                    content += type_name[0] + "\t" + "Zhang Zhou City" + "\n"
                            else:
                                content += line

                    with open(file_path, 'w', encoding='utf8') as r_f:
                        r_f.write("".join(content).strip())

    def gen_participle(self, src, dst):
        """
        生成分词后结果
        :param src: 原文件
        :param dst: 目的文件夹
        :return:
        """
        # 在目的文件夹创建文件夹
        new_dst = os.path.join(dst, "data")
        if not os.path.exists(new_dst):
            for root, dirs, files in os.walk(src):
                for dir in dirs:
                    src_s = os.path.join(root, dir)
                    dst_s = src_s.replace(src, new_dst)
                    if not os.path.exists(dst_s):
                        os.makedirs(dst_s)

        # 读取源文件分词写入新文件

        mecab = MeCab.Tagger("-Owakati")
        for root, dirs, files in os.walk(src):
            for file in files:
                if file.endswith("txt"):
                    file_path = os.path.join(root, file)
                    new_file_path = file_path.replace(src, new_dst)

                    sign = self.is_bom_sig(file_path)
                    if sign:
                        with open(file_path, 'r', encoding='utf-8-sig')as s_f, open(new_file_path, 'w',
                                                                                    encoding='utf8')as d_f:
                            line = s_f.read()
                            participle = mecab.parse(line.strip())
                            d_f.write(line.strip() + "\n")
                            d_f.write(participle)
                    else:
                        with open(file_path, 'r', encoding='utf8')as s_f, open(new_file_path, 'w',
                                                                               encoding='utf8')as d_f:
                            line = s_f.read()
                            participle = mecab.parse(line.strip())
                            d_f.write(line.strip() + "\n")
                            d_f.write(participle)

    def over_write_file(self, src, dest):
        """
        覆盖文件
        :param src: 源文件
        :param dest: 目的文件
        :return:
        """
        for root, dirs, files in os.walk(src):
            for file in files:
                src_file = os.path.join(root, file)
                dest_file = src_file.replace(src, dest)
                with open(src_file, 'r', encoding='utf8') as s_f, open(dest_file, 'w', encoding='utf8') as d_f:
                    content = s_f.read()
                    d_f.write(content)
                print("*" * 300)
                print(src_file)
                print(dest_file)

    def word_diff_dict(self, text_folder, dict_file):
        """
        单词提取，单词与发音词典对比
        :param text_folder: 单词提取路径
        :param dict_file: 发音词典文件
        :return:
        """
        # 读取发音词典文件
        word_set = set()
        with open(dict_file, 'r', encoding='utf8') as f:
            for line in f:
                word = line.strip().split("\t")[0]
                word_set.add(word)

        # 循环出文件里面的所有单词判断是否都在发音词典里面
        with open("error.txt", "a", encoding='utf8')as e_f:
            for root, dirs, files in os.walk(text_folder):
                for file in files:
                    file_name = os.path.join(root, file)
                    with open(file_name, 'r', encoding='utf8') as t_f:
                        words = t_f.readlines()[1].strip().split()
                        for word in words:
                            if word not in word_set:
                                print(word)
                                print(file_name)
                                e_f.write("\t".join([word, file_name]) + "\n")

    def is_bom_sig(self, file):
        """
        判断是否有签名
        :param file:
        :return:
        """
        with open(file, mode='rb+') as f:
            content = f.read()
            if len(content) >= 3 and content[0] == 0xef and content[1] == 0xbb and content[2] == 0xbf:
                return True
            else:
                return False

    def file_sig_tran(self, folder):
        """
        文件签名转换
        :param folder: 文件夹
        :return:
        """
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_name = os.path.join(root, file)
                if file_name.endswith("txt"):
                    with open(file_name, mode='rb+') as f:
                        content = f.read()
                        if len(content) >= 3 and content[0] == 0xef and content[1] == 0xbb and content[2] == 0xbf:
                            f.seek(0)
                            f.truncate()
                            f.write(content[3:])

    def output_data(self, table_name=None, file_name=None, test=True):
        """
        导出数据, 不同于那两个方法，输出不同
        :param table_name:
        :param file_name:
        :return:
        """
        if not test:
            sql = """select * from spiderframe.{};""".format(table_name)
        else:
            sql = """select * from spiderframe.{} limit 10;""".format(table_name)

        my = MysqlCon()
        i = 1
        for batch in my.get_many_json(sql):
            for item in batch:
                content_str = item.get("content")
                if content_str:
                    with open(file_name + "_{}.txt".format(i), 'a', encoding='utf8')as f:
                        f.write(content_str + "\n")
                    i += 1

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
        # dict_file = r"wordfreq.txt"
        # word_file = r"English_word.tsv"
        # self.count_word_freq(dict_file, word_file)

        # 替换matedata文件
        # path = r"\\10.10.30.14\apy161101045_797人低幼儿童麦克风手机采集语音数据\完整数据包_processed\data"
        # path = r"\\10.10.30.14\apy161101025_739人中国儿童麦克风采集语音数据\完整数据包_processed\data"
        # self.process_metadate(path)

        # 修改文件夹名
        # files_path = r"\\10.10.30.14\李昺3\数据整理\已完毕\语音类\基础识别\apy161101018_r_1044小时闽南语手机采集语音数据_朗读\完整数据包_加密后数据\data"
        # self.folder_rename(files_path)

        # parent_path = r"\\10.10.30.14\李昺3\数据整理\已完毕\语音类\基础识别\apy161101018_r_1044小时闽南语手机采集语音数据_朗读\完整数据包_加密后数据\data\category1"
        # parent_path = r"\\10.10.30.14\李昺3\数据整理\已完毕\语音类\基础识别\apy161101018_r_1044小时闽南语手机采集语音数据_朗读\完整数据包_加密后数据\data\category2"
        # parent_path = r"\\10.10.30.14\李昺3\数据整理\已完毕\语音类\基础识别\apy161101018_r_1044小时闽南语手机采集语音数据_朗读\完整数据包_加密后数据\data\category3"
        # parent_path = r"\\10.10.30.14\李昺3\数据整理\已完毕\语音类\基础识别\apy161101018_r_1044小时闽南语手机采集语音数据_朗读\完整数据包_加密后数据\data\category4"
        # parent_path = r"\\10.10.30.14\李昺3\数据整理\已完毕\语音类\基础识别\apy161101018_r_1044小时闽南语手机采集语音数据_朗读\完整数据包_加密后数据\data\category5"

        # self.file_rename(parent_path)
        # parent_path = r"\\10.10.30.14\李昺3\数据整理\已完毕\语音类\基础识别\apy161101018_r_1044小时闽南语手机采集语音数据_朗读\完整数据包_加密后数据\data\category"
        #
        # self.fixed_metadata(parent_path)

        # 临时性一次性分隔内容

        # file = r"\\10.10.30.14\李昺3\数据整理\已完毕\语音类\基础识别\apy161101018_r_1044小时闽南语手机采集语音数据_朗读\错误文件"
        # self.temp_one(file)

        # with open('last_info', 'r', encoding='utf8') as f:
        #     for line in f.readlines():
        #         line_content = line.strip()
        #         self.fixed_metadata(line_content)

        # src = r"\\10.10.30.14\格式整理_ming\APY161101033_R_bad_txt\data"
        # dest = r"\\IT-20190729TRCT\数据备份_liuxd\apy161101033_r_232小时法语手机采集语音数据\完整数据包_processed\data"
        # self.over_write_file(src, dest)

        # folder = r"\\10.10.30.14\apy181231008_514小时日语手机采集语音数据\完整数据包\data"
        # folder = r"C:\Users\Administrator\Desktop\日语"
        # dst_folder = r"\\10.10.30.14\杨明明\514小时日语文本"
        # dst_folder = r"C:\Users\Administrator\Desktop\data"
        # self.gen_participle(src=folder, dst=dst_folder)

        # text_folder = r"\\10.10.30.14\杨明明\514小时日语文本"
        # dict_file = r"C:\Users\Administrator\Desktop\发音词典"
        # self.word_diff_dict(text_folder, dict_file)

        # folder = r"\\10.10.30.14\apy181231008_514小时日语手机采集语音数据\完整数据包\data"
        # self.file_sig_tran(folder)

        self.output_data(table_name="hebrew_walla_content", file_name="hebrew")


if __name__ == '__main__':
    work = WorkScript()
    work.run()
