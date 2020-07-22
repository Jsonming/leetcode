#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/1 16:43
# @Author  : yangmingming
# @Site    : 
# @File    : process_old_data.py
# @Software: PyCharm
import os
import re
import shutil
import json
from collections import defaultdict
from multiprocessing import Pool
from collections import defaultdict
import pypinyin

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


def move_data(file):
    """
    移动拷贝数据
    :param file:
    :return:
    """
    # 老数据文件
    src_txt_file = file
    src_wav_file = file.replace("txt", "wav")
    src_meta_file = file.replace("txt", "metadata")

    path, file_name = os.path.split(file)
    new_path = path.replace("data", "包含数字")  # 新路径
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    # 新文件
    txt_file = os.path.join(new_path, file_name)
    wav_file = txt_file.replace("txt", "wav")
    meta_file = txt_file.replace("txt", "metadata")

    shutil.copyfile(src_txt_file, txt_file)
    shutil.copyfile(src_wav_file, wav_file)
    shutil.copyfile(src_meta_file, meta_file)


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

        if os.path.exists(wav_file):
            os.remove(wav_file)
        else:
            print("{}\t do not exits".format(wav_file))
        if os.path.exists(txt_file):
            os.remove(txt_file)
        else:
            print("{}\t do not exits".format(txt_file))
        if os.path.exists(meta_file):
            os.remove(meta_file)
        else:
            print("{}\t do not exits".format(meta_file))

    def copy_txt(self, folder):
        """
        将文件夹下面所有文txt 文件copy 到本地便于查找问题
        :param folder:
        :return:
        """
        file_name = re.findall(r"\\(\w+音数据.*?)\\", folder)[0]
        # file_name = folder.split("\\")[-2]
        if file_name:
            local_file = file_name + ".txt"
        else:
            raise FileNotFoundError("路径中没有匹配到项目名称")

        with open(local_file, 'a', encoding='utf8') as f:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.endswith("txt") and file != "index.txt":
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r', encoding='utf8')as r_f:
                            content = r_f.read()
                            f.write(file_path + "\t" + content.strip() + "\n")
                            # f.write(content.strip() + "\n")

    def get_symbol(self, file):
        """
        提取文件中的特殊符号
        :param file: 特殊符号日志文件
        :return: 特殊符号集合
        """

        symbol_char = defaultdict(int)
        with open(file, 'r', encoding='utf8')as f:
            for line in f:
                file, error, *_ = line.strip().split("\t")
                symbol = error.replace("in contain symbol ", "").replace("out contain symbol ", "").replace(
                    "Has double str(quan jiao) is ", "")
                try:
                    chars = eval(symbol.strip())
                except Exception as e:
                    print(symbol)
                for char in chars:
                    symbol_char[char] += 1
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

    def modify_noise_symbol(self, error_file):
        """
        日语修改噪音符号，日语噪音符号是[n]  格式，不存在各种嵌套，根据n]  匹配左括号，根据[n 匹配右括号
        :param file:
        :return:
        """
        with open(error_file, 'r', encoding='utf8') as f:
            for line in f:
                file, error = line.strip().split("\t")
                if os.path.exists(file):
                    with open(file, 'r+', encoding='utf8')as route_f:
                        content = route_f.read()
                        print(content)

                        content = re.sub(r"[\[]*[p|P]+[\]]+", '[p]', content)
                        content = re.sub(r"[\[]*[n|N]+[\]]+", '[n]', content)
                        content = re.sub(r"[\[]*[r|R]+[\]]+", '[r]', content)
                        content = re.sub(r"[\[]*[b|B]+[\]]+", '[b]', content)
                        content = re.sub(r"[\[]*[a|A]+[\]]+", '[a]', content)
                        content = re.sub(r"[\[]*[s|S]+[\]]+", '[s]', content)
                        content = re.sub(r"[\[]*[t|T]+[\]]+", '[t]', content)
                        content = re.sub(r"[\[]*[M]+[\]]+", '[m]', content)

                        content = re.sub(r"[\[]+[p|P]+[\]]*", '[p]', content)
                        content = re.sub(r"[\[]+[n|N]+[\]]*", '[n]', content)
                        content = re.sub(r"[\[]+[r|R]+[\]]*", '[r]', content)
                        content = re.sub(r"[\[]+[b|B]+[\]]*", '[b]', content)
                        content = re.sub(r"[\[]+[a|A]+[\]]*", '[a]', content)
                        content = re.sub(r"[\[]+[s|S]+[\]]*", '[s]', content)
                        content = re.sub(r"[\[]+[t|T]+[\]]*", '[t]', content)
                        content = re.sub(r"[\[]+[M]+[\]]*", '[m]', content)

                        content = re.sub(r"[\[]*[z|Z]+[\]]+", '[z]', content)
                        content = re.sub(r"[\[]+[z|Z]+[\]]*", '[z]', content)
                        content = re.sub(r"[\[]*[h|H]+[\]]+", '[h]', content)
                        content = re.sub(r"[\[]+[h|H]+[\]]*", '[h]', content)
                        content = re.sub(r"[\[]*[k|K]+[\]]+", '[k]', content)
                        content = re.sub(r"[\[]+[k|K]+[\]]*", '[k]', content)
                        content = re.sub(r"[\[]*[o|O]+[\]]+", '[o]', content)
                        content = re.sub(r"[\[]+[o|O]+[\]]*", '[o]', content)
                        content = re.sub(r"\[]", '', content)
                        # content = re.sub(r"[\[]*[n|N]+[\]]+", '[N]', content)
                        # content = re.sub(r"[\[]+[n|N]+[\]]*", '[N]', content)
                        # content = re.sub(r"[\[]*[p|P]+[\]]+", '[P]', content)
                        # content = re.sub(r"[\[]+[p|P]+[\]]*", '[P]', content)
                        # content = re.sub(r"[\[]*[s|S]+[\]]+", '[S]', content)
                        # content = re.sub(r"[\[]+[s|S]+[\]]*", '[S]', content)
                        # content = re.sub(r"[\[]*[t|T]+[\]]+", '[T]', content)
                        # content = re.sub(r"[\[]+[t|T]+[\]]*", '[T]', content)
                        print(content.replace(""))
                        # route_f.seek(0)
                        # route_f.truncate()
                        # route_f.write(content)

    def count_person_field(self, error_field):
        """
        统计字段缺失的人
        :param error_field:
        :return:
        """
        path_set = set()
        with open(error_field, 'r', encoding='utf8')as f:
            for line in f:
                file, error_type = line.strip().split("\t")
                path, file_name = os.path.split(file)
                path_set.add(path)
        print(error_type)
        for item in path_set:
            print(item)
        return list(path_set)

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
                    self.modify_metadata(file_path, field)

    def modify_metadata(self, file_path, field):
        """

        :param file_path:
        :param field:
        :return:
        """
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
                file, error, *_ = line.strip().split("\t")
                try:
                    with open(file, 'r+', encoding="utf8") as route_f:
                        route_content = route_f.read()
                        new_content = re.sub('[{}]+'.format("|".join(special_characters)), " ", route_content).strip()
                        # new_content = re.sub(' ', "\n", new_content).strip()
                        # print(route_content)
                        print(new_content)
                        route_f.seek(0)
                        route_f.truncate()
                        route_f.write(new_content)
                except FileNotFoundError as e:
                    print("文件删除")

    def remove_special_characters(self, error_file, special_characters):
        """
        删除特殊字符
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

    def remove_line(self, file, line_content):
        """
        删除文本中某一行
        :param file:
        :param line_number:
        :return:
        """
        with open(file, 'r+', encoding='utf8')as f:
            content = ''
            for line in f:
                if line.strip().split("\t")[-1] != line_content.strip():
                    content += line
            f.seek(0)
            f.truncate()
            f.write(content)

    def delete_contain_symbol(self, error_file, special_characters):
        """
        删除包含特殊字符的数据
        :param error_file:
        :param special_characters:
        :return:
        """
        with open(error_file, 'r', encoding='utf8') as f:
            for line in f:
                file, error, *_ = line.strip().split("\t")
                flag = eval(error.replace("out contain symbol ", '').replace("in contain symbol ", ''))
                special_char_flag = [True if char in flag else False for char in special_characters]
                if any(special_char_flag):
                    if os.path.exists(file):
                        self.err_file_remove(file)

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
            for line in f:
                file, error_message, *_ = line.strip().split("\t")
                try:
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

    def tran_new_mate(self, project_path=None):
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
                            meta["LBR"] = lbr.split()[-1]
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
                        DBN = meta.get("DBN")
                        # if not DBN:
                        #     meta["DBN"] = "ZY2016091911"

                        try:
                            new_content = sample_temp.format(**meta)
                        except KeyError as ke:
                            print(file_path)
                            raise ke
                        else:
                            # print(new_content)
                            f.seek(0)
                            f.truncate()
                            f.write(new_content)

    def count_noise(self, project_path):
        """
        统计噪音符号情况
        :param project_path:项目文件夹
        :return:
        """
        print(project_path)
        re_regr_one = re.compile("[\[]+.*?[]]+|[@~%]+|<.*?>")
        count_n = defaultdict(int)
        with open("noise_file.txt", 'a', encoding='utf8')as n_f:
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    if file.endswith("txt"):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r+', encoding='utf8')as f:
                            content = f.read()
                            match_result = re.findall(re_regr_one, content)
                            if match_result:
                                n_f.write(file_path + "\t" + str(match_result) + "\n")  # 将噪音符号文件记录和
                                for item in match_result:
                                    print(item)
                                    count_n[item] += 1
                            loanword_one = re.findall("\[/.*?/]", content)
                            count_n["[//]表示外来词"] += len(loanword_one)
                            fuzzy_one = re.findall("\[\(\(.*?\)\)]", content)
                            count_n["[(())]表示外来词"] += len(fuzzy_one)
        with open('count_noise.txt', 'a', encoding='utf8')as c_f:
            c_f.write(json.dumps(count_n))
        return count_n

    def output_noise(self, project_path):
        """
        统计噪音符号
        :param legal_noise:
        :return:
        """
        print(project_path)
        re_regr_one = re.compile(
            "\[\[lipsmack]]|\[\[cough]]|\[\[sneeze]]|\[\[breath]]|\[\[background]]|\[\[laugh]]|[@~%]+|<SPK>|<NON>|<STA>|<NPS>|"
            "\[[NTSP]]|\[[ntsp]]")
        count_n = defaultdict(int)
        with open("noise_file.txt", 'a', encoding='utf8')as n_f:
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    if file.endswith("txt"):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r+', encoding='utf8')as f:
                            content = f.read()
                            match_result = re.findall(re_regr_one, content)
                            if match_result:
                                n_f.write(file_path + "\t" + str(match_result) + "\n")  # 将噪音符号文件记录和
                                for item in match_result:
                                    print(item)
                                    count_n[item] += 1
                            loanword_one = re.findall("\[/.*?/]", content)
                            count_n["[//]表示外来词"] += len(loanword_one)
                            fuzzy_one = re.findall("\[\(\(.*?\)\)]", content)
                            count_n["[(())]表示模糊不清"] += len(fuzzy_one)
        with open('count_noise.txt', 'a', encoding='utf8')as c_f:
            c_f.write(json.dumps(count_n))
        return count_n

    def chinese_place_english(self, location_name):
        """
        地点名称转换
        :param location_name:
        :return:
        """
        if "省" in location_name:
            provice_name_zh = location_name.split("省")[0]
            if "山西" in provice_name_zh:
                provice_name_en = "shan1xi province"
            elif "陕西" in provice_name_zh:
                provice_name_en = "shan3xi province"
            else:
                provice_name_en = "{} provice".format("".join(pypinyin.lazy_pinyin(provice_name_zh)))
            city_name_zh = location_name.split("省")[1]
            city_name_en = "{} city".format("".join(pypinyin.lazy_pinyin(city_name_zh.split("市")[0])))
            local_name = "{}, {}".format(provice_name_en, city_name_en)
        elif "市" in location_name:
            city_name_en = "{} city".format("".join(pypinyin.lazy_pinyin(location_name.split("市")[0])))
            local_name = city_name_en
        else:
            local_name = location_name.replace("黑龙江哈尔滨", "heilongjiang province, haerbin, city")
            local_name = local_name.replace("河南信阳", "henan province, xinyang, city")
            local_name = local_name.replace("河北保定", "hebei province, baoding, city")
            local_name = local_name.replace("内蒙古兴安盟", "".join(pypinyin.lazy_pinyin("内蒙古兴安盟")))
            local_name = local_name.replace("内蒙古自治区兴安盟", "".join(pypinyin.lazy_pinyin("内蒙古自治区兴安盟")))

        return local_name

    def async_executive(self, func, args):
        """
        多进程执行函数有效提高效率
        :param func: 函数
        :param args: 参数
        :return:
        """
        pool = Pool(processes=4)
        pool.map(func, args)
        pool.close()
        pool.join()

    def process_tem_file(self, error_file):
        """
        手动修改部分，这部分情况比较复杂大多一次性修改不足以抽出来封装函数
        :param error_file:
        :return:
        """
        p = set()
        with open(error_file, 'r', encoding='utf8')as e_f:
            for line in e_f:
                file_path = line.strip().split("\t")[0]
                p.add(re.findall(r".*?G\d+", file_path)[0])
        for item in p:
            print(item)

    def process_all_data(self, project_path):
        """
        处理整个项目的所有文件（临时性）
        :param folder:
        :return:
        """
        city_map = {
            '台湾': 'Taiwan',
            '广东省梅州市': 'Meizhou City, Guangdong Province',
            '云南省红河哈尼族彝族自治州': 'Honghe Hani and Yi Autonomous Prefecture of Yunnan Province',
        }
        act_map = {
            "其它方言": 'Other',
            "閩語（福建方言）": "Min dialect(FuJian)",
            "闽话(福建方言)": "Min dialect(FuJian)",
            "闽语（福建方言）": "Min dialect(FuJian)",
            "标淮普通话(无方言)": "Standard Mandarin",
            "标准普通话（无方言）": "Standard Mandarin",
            "標準普通話（無方言）": "Standard Mandarin",
            "官話（北方方言）": "Standard Mandarin",
            "客家话": "Hakka dialect",
            "客家话(客家方言)": "Hakka dialect",
        }
        bir_map = {"台中及周邊(包含台中、彰化)": "Taichung and surrounding(Changhua)",
                   "台北及周邊（包含台北、桃園、基隆）": "Taipei and surrounding(Taoyuan、Keelung)",
                   "高雄及周邊(包含高雄、屏東)": "Kaohsiung and surrounding(Pingtung)",
                   "台南及周邊(包含台南、嘉義)": "Tainan and surrounding(Chiayi)"
                   }

        city = {'杭州': 'Hangzhou',
                '北京': 'Beijing',
                '南京': 'Nanjing',
                '绵阳': 'Mianyang',
                '暂无': '',
                '厦门': 'Xiamen',
                '贵阳': 'Guiyang',
                '德阳': 'Deyang',
                '崇州': 'Chongzhou',
                '天津': 'Tianjin',
                '河北': 'Hebei',
                '成都': 'Chengdu',
                '四川': 'Sichuan',
                '福州': 'Fuzhou', }
        birs = {'美国': 'United States',
                '厦门': 'Xiamen',
                '泉州': 'Quanzhou',
                '简阳': 'Jianyang',
                '成都': 'Chengdu',
                '日本': 'Japan',
                '漳州': 'Zhangzhou',
                '福州': 'Fuzhou',
                '吉林': 'Jilin',
                '北京': 'Beijing',
                '湖北': 'Hubei',
                '贵州': 'Guizhou',
                'n南京': 'Nanjing',
                '德阳': 'Deyang',
                '杭州': 'Hangzhou',
                '乐山': 'Leshan',
                '江西': 'Jiangxi',
                '浙江': 'Zhejiang',
                '泸州': 'Luzhou',
                '大连': 'Dalian',
                '上海': 'Shanghai',
                '河北': 'Hebei',
                '达州': 'Dazhou',
                '长春': 'Changchun',
                '绵阳': 'Mianyang',
                '南京': 'Nanjing',
                '唐山': 'Tangshan',
                '暂无': '',
                '香港': 'Hong Kong',
                '南充': 'Nanchong',
                '湖南': 'Hunan',
                '四川': 'Sichuan',
                '福建': 'Fujian',
                '天津': 'Tianjin',
                '云南': 'Yunnan',
                '眉山': 'Meishan',
                '河南': 'Henan',
                '安徽': 'Anhui',
                '江苏': 'Jiangsu',
                ' 北京': 'Beijing',
                '崇州': 'Chongzhou',
                '陕西': 'Shaanxi'}

        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith("metadata"):
                    file_path = os.path.join(root, file)
                    new_content = ""
                    with open(file_path, 'r+', encoding='utf8')as f:
                        for line in f:
                            if "REP" in line:
                                new_content += "REP\tindoor\n"
                            elif "ACC" in line and "TACC-19" not in line:
                                line = line.strip().strip("﻿")
                                try:
                                    acc, con = line.split("\t")
                                except Exception as e:
                                    new_content += "ACC\t\n"
                                else:
                                    if con:
                                        new_content += "ACC\t{}\n".format(city_map[con])
                                    else:
                                        new_content += "ACC\t\n"

                            elif "ACT" in line:
                                try:
                                    act, ccon = line.strip().split("\t")
                                except Exception as e:
                                    new_content += "ACT\t\n"
                                else:
                                    new_content += "ACT\t{}\n".format(act_map[ccon])
                            elif "BIR" in line:
                                try:
                                    bir, cccon = line.strip().split("\t")
                                except Exception as e:
                                    new_content += "BIR\t\n"
                                else:
                                    new_content += "BIR\t{}\n".format(bir_map[cccon])
                            elif "SRA" in line:
                                new_content += "SRA\t\n"
                            elif "EMO" in line:
                                new_content += "EMO\t\n"
                            else:
                                new_content += line
                        # print(new_content)
                        f.seek(0)
                        f.truncate()
                        f.write(new_content)

    def count_all_data(self, project_path):
        """
        统计项目中的各种情况
        :param project_path:
        :return:
        """
        rest = set()
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith("metadata"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r+', encoding='utf8')as f:
                        for line in f:
                            if "MIT" in line:
                                try:
                                    sra, con = line.strip().split("\t")
                                except Exception as e:
                                    print(file_path)
                                else:
                                    rest.add(con)
        print(rest)

    def temp(self, project_path):
        """

        :param project_path:
        :return:
        """
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith("txt"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r+', encoding='utf8')as f:
                        content = f.read().strip()
                        if 'wav' in content:
                            try:
                                wav_name, new_content = content.split("\t")
                            except Exception as e:
                                print(file_path, content)
                            else:
                                f.seek(0)
                                f.truncate()
                                f.write(new_content)

    def run(self):
        """
        主控制逻辑
        :return:
        """

        # 分隔日志
        # log_file = r"D:\Workspace\Logs\4-log.log"
        # out_file_prefix = r"error_"
        # self.split_log(log_file, out_file_prefix)

        # 删除数据
        # error_file = r"error_contains_the_number.txt"
        # with open(error_file, 'r', encoding='utf8') as f:
        #     for line in f:
        #         file = line.strip().split("\t")[0]
        #         self.err_file_remove(file)
        #
        # 删除错误文件
        # with open('error_file_type_error.txt', 'r', encoding='utf8') as f:
        #     for line in f:
        #         file = line.strip().split("\t")[0]
        #         if os.path.exists(file):
        #             os.remove(file)

        # 删除文本中某一行
        # with open('error_contains_the_number.txt', 'r', encoding='utf8') as f:
        #     for line in f:
        #         file = line.strip().split("\t")[0]
        #         line_content = line.strip().split("\t")[-2]
        #         self.remove_line(file, line_content)

        # 全角转半角
        # error_file = r'error_Has_double_str(quan.txt'
        # self.process_quanjioa(error_file)

        # 规范噪音符号
        # error_file = r"error_out_contain_symbol.txt"
        # self.sub_noise(error_file)

        # 老标注规范噪音符号
        # error_file = r"error_out_contain_symbol.txt"
        # self.modify_noise_symbol(error_file)

        # 统计所有的特殊符号
        # error_file = r"error_out_contain_symbol.txt"
        # print(self.get_symbol(error_file))

        # 删除特殊字符
        # error_file = r"error_out_contain_symbol.txt"
        # special_char = ['"']
        # self.remove_special_characters(error_file, special_char)

        # 替换特殊字符
        # error_file = r"error_out_contain_symbol.txt"
        # special_char = ['’', '(', ')', ';', '{', '}', '“', '”', '"']
        # self.replace_special_characters(error_file, special_char)

        # 删除含有特殊符号的数据
        # error_file = r"error_out_contain_symbol.txt"
        # special_char = ['}', '{', ']', '[', '=']
        # self.delete_contain_symbol(error_file, special_char)

        # 修改单个metadata 字段
        # error_file = r"error_BIR_value_is.txt"
        # with open(error_file, 'r', encoding='utf8') as f:
        #     for line in f:
        #         file = line.strip().split("\t")[0]
        #         self.modify_metadata(file, {"BIR": 'Northern China'})

        # 统计缺失人和字段
        # error_file = r"error_BIR_key_is.txt"
        # path_list = self.count_person_field(error_file)

        # 填充字段
        # person_folder = r"\\10.10.30.14\语音数据_2016\apy161101008_370人杭州方言手机采集语音数据\完整数据包_加密后数据\data\category\G0626"
        # self.filled_field(person_folder, {"AGE": "23"})

        # 修改日志文件中，将男女转为英文
        # error_message_log = r'error_value_format_is.txt'
        # self.modify_gender_field(error_message_log)

        # 修改项目中所有的性别中文英文转换
        # project_path = r"\\10.10.30.14\语音数据_2016\APY161101043_R_204人台湾普通话手机采集数据\完整数据包\data\category"
        # self.project_process_gender(project_path)

        # 修改项目中多个换行
        # project_path = r"\\10.10.30.14\apy161101013_1505小时普通话手机采集语音数据\完整数据包_加密后数据\data"
        # self.process_tran_line(project_path)

        # 提取所有TXT文件
        # project_path = r"\\10.10.30.14\apy170501037_1297小时录音笔采集场景噪音数据\完整数据包_processed\data"
        # self.copy_txt(project_path)

        # 转换成新的metadata
        # project_path = r"\\10.10.30.14\语音数据_2016\apy161101007_250人苏州方言手机采集语音数据\完整数据包_加密后数据\data\category"
        # self.tran_new_mate(project_path)

        # 预统计所有的噪音符号
        # project_path = r"\\10.10.30.14\语音数据_2016\apy161101016_463人河南方言手机采集语音数据\完整数据包_加密后数据\data\category"
        # project_path = r"\\10.10.30.14\语音数据_2016\apy161101008_370人杭州方言手机采集语音数据\完整数据包_加密后数据\data\category"
        # project_path = r"\\10.10.30.14\语音数据_2016\apy161101007_250人苏州方言手机采集语音数据\完整数据包_加密后数据\data\category"
        # print(self.count_noise(project_path))

        # 噪音符号统计
        # project_path = r"\\10.10.30.14\语音数据_2016\apy161101045_797人低幼儿童麦克风手机采集语音数据\完整数据包_processed\data"
        # project_path = r"\\10.10.30.14\语音数据_2016\apy161101008_370人杭州方言手机采集语音数据\完整数据包_加密后数据\data\category"
        # print(self.output_noise(project_path))

        # 根据错误日志手动修改部分
        # error_file = r"error_ACC_value_is.txt"
        # self.process_tem_file(error_file)

        # 统计项目中的情况
        # project_path = r"\\10.10.30.14\语音数据_2016\apy161101016_463人河南方言手机采集语音数据\完整数据包_加密后数据\data\category"
        # self.count_all_data(project_path)

        # 临时性处理所有数据 刷一遍数据
        # project_path = r"\\10.10.30.14\语音数据_2016\APY161101043_R_204人台湾普通话手机采集数据\完整数据包\data\category"
        # self.process_all_data(project_path)

        # project_path = r"\\10.10.30.14\语音数据_2016\APY161101043_R_204人台湾普通话手机采集数据\完整数据包\data\category"
        # self.temp(project_path)


if __name__ == '__main__':
    pd = ProcessData()
    pd.run()
