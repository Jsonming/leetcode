#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/1 16:43
# @Author  : yangmingming
# @Site    : 
# @File    : process_old_data.py
# @Software: PyCharm
import json
import os
import re
import pypinyin
import time
from collections import defaultdict
from CommenScript.update_data.update_txt import strQ2B


def check_noise_annotation_old_norm(txt_path, input_str):
    # 获取配置文件的噪音标注列表
    noise_right_list = []
    # 匹配句子中的噪音标注
    noise_find_list = re.findall('\\[\\[.*?\\]\\]', input_str)
    for word in noise_find_list:
        if word not in noise_right_list:
            print("{}\t has wrong noise_annotation".format(txt_path))

    # 去除所有正确标注后，检测多余中括号
    new_str = re.sub("\\[\\(\\(.*?\\)\\)\\]", " ", input_str)
    new_str = re.sub("\\[/.*?/\\]", " ", new_str)
    new_str = re.sub("\\[\\[.*?\\]\\]", " ", new_str)

    if '[' in new_str:
        print('{}\t Noise label format error contain ['.format(txt_path))
    elif ']' in new_str:
        print('{}\t Noise label format error contain ]'.format(txt_path))
    elif "(" in new_str or ")" in new_str:
        print('{}\t Noise label format error contain ( or )'.format(txt_path))
    elif "/" in new_str:
        f_str = re.findall("/", new_str)
        if len(f_str) == 1:
            print('{}\t Noise label format error contain /'.format(txt_path))


class ProcessData(object):
    def __init__(self):
        pass

    def split_log(self, log_file, out_file_pre):
        """
        分解日志文件，修改分别输出日志，根据不同的错误类型输出日志
        :param log_file:日志文件
        :param out_file_pre: 输出文件前缀
        :return:
        """
        with open(log_file, 'r', encoding='utf8') as log_f:
            for line in log_f:
                content = line.strip()
                error_desc = content.split("\t")
                file = error_desc[0]
                error_class = "\t".join(error_desc[1:]).strip()  # 因为是根据"\t" 分隔的，这里用"\t" 拼接到一起，还原错误
                error_class_name = "_".join(error_class.split()[:3])  # "["中括号不能作为文件名，选前三位作为文件名
                if error_class_name:
                    # 将错误分别写入到各自文件夹中
                    with open(out_file_pre + error_class_name + ".txt", 'a', encoding='utf8')as error_f:
                        error_f.write(file + "\t" + error_class + "\n")

    def err_file_remove(self, file):
        """
        删除无法处理的文件
        :param file:
        :return:
        """
        if file.endswith("txt"):
            txt_file = file
            wav_file = file.replace("txt", "wav")
            meta_file = file.replace("txt", "metadata")
        elif file.endswith("wav"):
            txt_file = file.replace("wav", "txt")
            wav_file = file
            meta_file = file.replace("wav", "metadata")
        elif file.endswith("metadata"):
            txt_file = file.replace("metadata", "txt")
            wav_file = file.replace("metadata", "wav")
            meta_file = file

        try:
            os.remove(wav_file)
            os.remove(txt_file)
            os.remove(meta_file)
        except Exception as e:
            raise e

    def copy_txt(self, folder):
        """
        将文件夹下面所有文txt 文件copy 到本地便于查找问题
        :param folder:
        :return:
        """
        file_name = re.findall(r"\\(\w+语音数据.*?)\\", folder)[0]
        # file_name = folder.split("\\")[-2]
        if file_name:
            local_file = file_name + ".txt"
        else:
            raise FileNotFoundError("路径中没有匹配到项目名称")

        with open(local_file, 'a', encoding='utf') as f:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.endswith("txt"):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r', encoding='utf8')as r_f:
                            content = r_f.read().strip()
                            # f.write(file_path + "\t" + content.strip() + "\n")
                            f.write(content.strip() + "\n")

    def get_symbol(self, file):
        """
        提取文件中的特殊符号
        :param file: 特殊符号日志文件
        :return: 特殊符号集合
        """

        symbol_char = set()
        with open(file, 'r', encoding='utf8')as f:
            for line in f:
                file, error, *_, content = line.strip().split("\t")
                symbol = error.replace("in contain symbol ", "").replace("out contain symbol ", "").replace(
                    "Has double str(quan jiao) is ", "")
                try:
                    chars = eval(symbol)
                except Exception as e:
                    print(symbol)
                for char in chars:
                    symbol_char.add(char)
        return symbol_char

    def create_folder(self, folder):
        """
        创建文件夹
        :param folder:
        :return:
        """
        if not os.path.exists(folder):
            os.makedirs(folder)

    def count_all_charactirs(self, pro_folder):
        """
        统计一套数据所有的字符
        :return:
        """
        charactors = set()  # 字符集合
        for root, dirs, files in os.walk(pro_folder):
            for file in files:
                if file.endswith("txt"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf8') as f:
                        for line in f:
                            for char in line.strip():
                                charactors.add(char)
        return charactors

    def modify_noise_symbol(self, file):
        """
        日语修改噪音符号，日语噪音符号是[n]  格式，不存在各种嵌套，根据n]  匹配左括号，根据[n 匹配右括号
        :param file:
        :return:
        """
        with open(file, 'r+', encoding='utf8')as f:
            content = f.read()
            content = re.sub(r"[\[]*[p|P]+[\]]+", '[p]', content)
            content = re.sub(r"[\[]*[n|N]+[\]]+", '[n]', content)
            content = re.sub(r"[\[]*[r|R]+[\]]+", '[r]', content)
            content = re.sub(r"[\[]*[b|B]+[\]]+", '[b]', content)
            content = re.sub(r"[\[]*[a|A]+[\]]+", '[a]', content)
            content = re.sub(r"[\[]*[m|M]+[\]]+", '[m]', content)
            content = re.sub(r"[\[]+[p|P]+[\]]*", '[p]', content)
            content = re.sub(r"[\[]+[n|N]+[\]]*", '[n]', content)
            content = re.sub(r"[\[]+[r|R]+[\]]*", '[r]', content)
            content = re.sub(r"[\[]+[b|B]+[\]]*", '[b]', content)
            content = re.sub(r"[\[]+[a|A]+[\]]*", '[a]', content)
            content = re.sub(r"[\[]+[m|M]+[\]]*", '[m]', content)

            # 中文数据
            # content = re.sub(r"[\[]*[z|Z]+[\]]+", '[z]', content)
            # content = re.sub(r"[\[]*[h|H]+[\]]+", '[h]', content)
            # content = re.sub(r"[\[]*[n|N]+[\]]+", '[n]', content)
            # content = re.sub(r"[\[]+[p|P]+[\]]*", '[p]', content)
            # content = re.sub(r"[\[]+[k|K]+[\]]*", '[k]', content)

            f.seek(0)
            f.truncate()
            f.write(content)

    def filled_field(self, folder, field: dict):
        """
        修改metadata 填充字段
        :param folder:
        :param field:
        :return:
        """
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith("metadata"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r+', encoding='utf8')as f:
                        content = ""
                        for line in f:
                            field_name = line.strip().split("\t")[0]
                            if field_name in field:
                                new_line = "\t".join([field_name, field[field_name]]) + "\n"
                            else:
                                new_line = line
                            content += new_line
                        f.seek(0)
                        f.truncate()
                        f.write(content)

    def sub_noise(self, error_file):
        """
        标准化噪音符号
        :param file:
        :return:
        """

        with open(error_file, 'r', encoding='utf8') as error_f:
            for line in error_f:
                file, error, content = line.strip().split("\t")

                with open(file, "r+", encoding='utf8')as f:
                    content = f.read()
                    print(content)
                    # content = content.replace("[(([background]))]", "[[background]]")

                    content = re.sub(r"[\[]+lipsmack[\]]+", "[[lipsmack]]", content)
                    content = re.sub(r"[\[]+cough[\]]+", "[[cough]]", content)
                    content = re.sub(r"[\[]+sneeze[\]]+", "[[sneeze]]", content)
                    content = re.sub(r"[\[]+breath[\]]+", "[[breath]]", content)
                    content = re.sub(r"[\[]+[background|Background|BACKGROUND|bakcground]+[\]]+", "[[background]]",
                                     content)
                    content = re.sub(r"[\[]+laugh[\]]+", "[[laugh]]", content)
                    content = re.sub(r"[\[]+breath[\]]+", "[[breath]]", content)
                    content = re.sub(
                        r"[\[]+[lipmack|Lipmack|LIPMACK|lipmake|lipsmacl|lipsmark|ipsmackl|liosmack]+[\]]+",
                        "[[lipsmack]]", content)

                    # 处理模糊音缺失中括号的情况
                    content = re.sub(r"[\[]*\(\(", "[((", content)
                    content = re.sub(r"\)\)[\]]*", "))]", content)
                    content = content.replace("()", '')
                    print(content)
                    f.seek(0)
                    f.truncate()
                    f.write(content)

    def replace_special_characters(self, error_file, special_characters):
        """
        替换特殊字符
        :param error_file:
        :return:
        """
        with open(error_file, 'r', encoding='utf8') as f:
            for line in f:
                file, error, *_, content = line.strip().split("\t")
                try:
                    with open(file, 'r+', encoding="utf8") as route_f:
                        route_content = route_f.read()
                        new_content = re.sub('[{}]+'.format("|".join(special_characters)), " ", route_content).strip()
                        new_content = re.sub('\s+', " ", new_content).strip()
                        print(route_content)
                        print(new_content)
                        route_f.seek(0)
                        route_f.truncate()
                        route_f.write(new_content)
                except FileNotFoundError as e:
                    print("文件删除")

    def remove_special_characters(self, error_file, special_characters):
        """
        替换特殊字符
        :param error_file:
        :return:
        """
        with open(error_file, 'r', encoding='utf8') as f:
            for line in f:
                file, error, *_, content = line.strip().split("\t")
                try:
                    with open(file, 'r+', encoding="utf8") as route_f:
                        route_content = route_f.read()
                        new_content = re.sub('[{}]+'.format("|".join(special_characters)), "", route_content).strip()
                        new_content = re.sub('\s+', " ", new_content).strip()
                        print(route_content)
                        print(new_content)
                        route_f.seek(0)
                        route_f.truncate()
                        route_f.write(new_content)
                except FileNotFoundError as e:
                    print("文件删除")

    def modify_gender_field(self, log_file):
        """
        修改SEX 字段
        :param log_file:
        :return:
        """

        error_files = set()
        with open(log_file, 'r', encoding='utf8')as log_f:
            for line in log_f:
                file_path = line.strip().replace("	value format is err", "")
                if file_path not in error_files:
                    error_files.add(file_path)
                    with open(file_path, 'r+', encoding='utf8')as f:
                        content = ""
                        for line in f:
                            if "SEX" in line:
                                new_line = line.replace("男", "Male").replace("女", "Female")
                            else:
                                new_line = line
                            content += new_line
                        # f.seek(0)
                        # f.truncate()
                        # f.write(content)

    def project_process_gender(self, project_path):
        """
        处理项目中所有的性别处理
        :param project_path:
        :return:
        """
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith("metadata"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r+', encoding='utf8')as f:
                        content = ""
                        for line in f:
                            if "SEX" in line:
                                new_line = line.replace("男", "Male").replace("女", "Female")
                            else:
                                new_line = line
                            content += new_line
                        f.seek(0)
                        f.truncate()
                        f.write(content)

    def process_tran_line(self, project_path):
        """
        处理项目中多行问题
        :param project_path:
        :return:
        """
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith("txt"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r+', encoding='utf8')as f:
                        content = f.read().strip()
                        f.seek(0)
                        f.truncate()
                        f.write(content)

    def process_quanjioa(self, log_file):
        """
        处理全角符号，全角转半角
        :param log_file:
        :return:
        """
        with open(log_file, 'r', encoding='utf8') as f:
            try:
                for line in f:
                    file, error_message, *_, content = line.strip().split("\t")
                    with open(file, 'r+', encoding='utf8') as route_f:
                        route_content = route_f.read()
                        new_content = strQ2B(route_content)
                        # print(route_content)
                        # print(new_content)
                        route_f.seek(0)
                        route_f.truncate()
                        route_f.write(new_content)
            except FileNotFoundError as e:
                print("文件被删除")

    def remove_symbol_square_brackets(self, content):
        """
        删除与噪音符号相似的中括号
        :param content:
        :return:
        """
        noise_set = set(list("zhnpkrpnrbamPNRBAM"))
        all_case = re.findall("\[(.*?)\]", content)
        for item in all_case:
            if item not in noise_set:
                content = content.replace("[" + item + "]", item)
        return content

    def tran_new_mate(self, project_path):
        """
        处理成新metadata
        :param work_dir:
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

        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith("metadata"):
                    file_path = os.path.join(root, file)
                    meta = dict()
                    with open(file_path, 'r+', encoding='utf8')as f:
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

                        sra = meta.get("SRA")
                        if not sra:
                            meta["SRA"] = ""
                        EMO = meta.get("EMO")
                        if not EMO:
                            meta["EMO"] = ""
                        ORS = meta.get("ORS")
                        if not ORS:
                            meta["ORS"] = ""

                        new_content = sample_temp.format(**meta)
                        print(new_content)
                        f.seek(0)
                        f.truncate()
                        f.write(new_content)

    def count_noise(self, project_path):
        """
        统计噪音符号情况
        :param project_path:项目文件夹
        :return:
        """
        re_regr_one = re.compile(
            "\[\[lipsmack]]+|\[\[cough]]+|\[\[sneeze]]+|\[\[breath]]+|\[\[background]]+|\[\[laugh]]"
            "+|\[p]+|\[n]+|\[z]+|\[h]+|\[k]+|\[r]+|\[b]+|\[a]+|\[m]+|\[s]+|\[t]+|[@~%]+")
        count_n = defaultdict(int)

        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith("txt"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r+', encoding='utf8')as f:
                        content = f.read()

                        match_result = re.findall(re_regr_one, content)
                        for item in match_result:
                            print(item)
                            count_n[item] += 1

                        loanword_one = re.findall("\[/.*?/]", content)
                        count_n["[//]表示外来词"] += len(loanword_one)
                        fuzzy_one = re.findall("\[\(\(.*?\)\)]", content)
                        count_n["[(())]表示外来词"] += len(fuzzy_one)

        return count_n

    def process_tem_file(self, error_file):
        """
        手动修改部分，这部分情况比较复杂大多一次性修改不足以抽出来封装函数
        :param error_file:
        :return:
        """

        with open(error_file, 'r+', encoding='utf8') as f:
            for line in f:
                file, *_, content_ = line.strip().split("\t")
                with open(file, 'r+', encoding='utf8')as route_f:
                    new_content = ""
                    for line in route_f:
                        if "SCC" in line:
                            field, content = line.strip().split("\t")
                            lenth = content.split(",")
                            if len(lenth) != 4:
                                try:
                                    surround, car_type, expr = content.split(",")
                                except Exception as e:
                                    print(content)
                                    raise e
                                sub_expr = expr.split()
                                if len(sub_expr) == 2:
                                    scc = ", ".join([surround, car_type, *sub_expr])
                                elif len(sub_expr) == 5:
                                    scc = ", ".join([surround, car_type, " ".join(sub_expr[:-3]), " ".join(sub_expr[-3:])])
                                else:
                                    scc = "Inside the car, German car, Audi A4L, low speed road"
                            new_line = "SCC" + "\t" + scc + "\n"
                        else:
                            new_line = line
                        new_content += new_line

                    route_f.seek(0)
                    route_f.truncate()
                    route_f.write(new_content)

    def process_all_data(self, folder):
        """
        处理整个项目的所有文件（临时性）
        :param folder:
        :return:
        """
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith("metadata"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r+', encoding='utf8')as f, open("SCC.txt", 'a', encoding='utf8')as i_f:
                        content = f.readlines()
                        for line in content:
                            if "SCC" in line:
                                i_f.write("\t".join([file_path, line]))

                        # f.seek(0)
                        # f.truncate()
                        # f.write(new_content)

    def run(self):
        """
        主控制逻辑
        :return:
        """

        # 分隔日志
        # log_file = r"D:\Workspace\Logs\2-log.log"
        # out_file_prefix = r"error_"
        # self.split_log(log_file, out_file_prefix)

        # 删除数据
        # error_file = r"error_contains_numbers_is.txt"
        # with open(error_file, 'r', encoding='utf8') as f:
        #     for line in f:
        #         file = line.strip().split("\t")[0]
        #         self.err_file_remove(file)

        # 删除错误文件
        # with open('error_file_type_error.txt', 'r', encoding='utf8') as f:
        #     for line in f:
        #         file = line.strip().split("\t")[0]
        #         if os.path.exists(file):
        #             os.remove(file)

        # 全角转半角
        # error_file = r'error_Has_double_str(quan.txt'
        # self.process_quanjioa(error_file)

        # 规范噪音符号
        # error_file = r"error_out_contain_symbol.txt"
        # self.sub_noise(error_file)

        # 统计所有的特殊符号
        # error_file = r"error_out_contain_symbol.txt"
        # print(self.get_symbol(error_file))

        # 删除特殊字符
        # error_file = r"error_out_contain_symbol.txt"
        # special_char = ['「', "」", '『', "』", ')', '(', '>', '<', '《', '》', '{', '}', ':', '“', '∶', '’', '”', '—', ';']
        # self.remove_special_characters(error_file, special_char)

        # 替换特殊字符
        # error_file = r"error_out_contain_symbol.txt"
        # special_char = ['_', ':']
        # self.replace_special_characters(error_file, special_char)

        # 填充字段
        # person_folder = r"\\10.10.30.14\apy180901052_287小时日语手机采集语音数据\完整数据包_processed\data\category\G0942\session01"
        # self.filled_field(person_folder, {"ACT": "East"})

        # 修改日志文件中，将男女转为英文
        # error_message_log = r'error_value_format_is.txt'
        # self.modify_gender_field(error_message_log)

        # 修改项目中所有的性别中文英文转换
        # project_path = r"\\10.10.30.14\apy161101014_r_662小时中文重口音手机采集语音数据\完整数据包_processed\data"
        # self.project_process_gender(project_path)

        # 修改项目中多个换行
        # project_path = r"\\10.10.30.14\apy161101013_1505小时普通话手机采集语音数据\完整数据包_加密后数据\data"
        # self.process_tran_line(project_path)

        # 提取所有TXT文件
        # project_path = r"\\10.10.30.14\apy161101018_r_1044小时闽南语手机采集语音数据_朗读\完整数据包_加密后数据\data"
        # self.copy_txt(project_path)

        # 转换成新的metadata
        # project_path = r"\\10.10.30.14\apy161101005_245小时车载环境普通话手机采集语音数据\完整数据包_加密后数据\data"
        # self.tran_new_mate(project_path)

        # 统计所有的噪音符号
        # project_path = r"\\10.10.30.14\apy161101005_245小时车载环境普通话手机采集语音数据\完整数据包_加密后数据\data"
        # project_path = r"\\10.10.30.14\apy161101014_r_662小时中文重口音手机采集语音数据\完整数据包_processed\data"
        # project_path = r"\\10.10.30.14\apy161101014_g_132小时中文重口音手机采集语音数据\完整数据包_processed\data"
        project_path = r"\\10.10.30.14\apy180901052_287小时日语手机采集语音数据\完整数据包_processed\data"
        print(project_path)
        print(self.count_noise(project_path))

        # 根据错误日志手动修改部分
        # error_file = 'sscc.txt'
        # self.process_tem_file(error_file)

        # 临时性处理所有数据 刷一遍数据
        # project_path = r"\\10.10.30.14\apy161101005_245小时车载环境普通话手机采集语音数据\完整数据包_加密后数据\data"
        # self.process_all_data(project_path)


if __name__ == '__main__':
    pd = ProcessData()
    pd.run()
