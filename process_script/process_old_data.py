#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/1 16:43
# @Author  : yangmingming
# @Site    : 
# @File    : process_old_data.py
# @Software: PyCharm
import re
import os
import json
import shutil
from workspace.work.dingding import dingding_decorator
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

    def sub_special_symbol(self, file):
        """
        替换特殊字符，替换的是 "[{" 和 "}]"
        :param file: 需替换的的文件
        :return:
        """
        with open(file, "r+", encoding='utf8') as input_f, \
                open("special_log.log", 'a', encoding='utf8') as log_f:
            content = input_f.read()
            new_content = content.replace("[{", "").replace("}]", "")
            input_f.seek(0)
            input_f.truncate()
            input_f.write(new_content)
            log_f.write("\t".join([file, content, new_content]) + "\n")

    def process_noise(self, file):
        """
        处理噪音符号格式问题
        :param file:
        :return:
        """
        with open(file, "r+", encoding='utf8')as f:
            content = f.read()
            content = re.sub(r"[\[]+[\]]*lipsmack[\[]*[\]]+", "[[lipsmack]]", content)
            content = re.sub(r"[\[]+[\]]*cough[\[]*[\]]+", "[[cough]]", content)
            content = re.sub(r"[\[]+[\]]*sneeze[\[]*[\]]+", "[[sneeze]]", content)
            content = re.sub(r"[\[]+[\]]*breath[\[]*[\]]+", "[[breath]]", content)
            content = re.sub(r"[\[]+[\]]*background[\[]*[\]]+", "[[background]]", content)
            content = re.sub(r"[\[]+[\]]*laugh[\[]*[\]]+", "[[laugh]]", content)
            content = re.sub(r"[\[]+[\]]*breath[\[]*[\]]+", "[[breath]]", content)
            # f.seek(0)
            # f.truncate()
            # f.write(content)

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
        local_file = folder.split("\\")[4] + ".txt"
        with open(local_file, 'a', encoding='utf') as f:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.endswith("txt"):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r', encoding='utf8')as r_f:
                            content = r_f.read()
                            f.write(file_path + "\t" + content.strip() + "\n")

    def fix_foreign_word(self, file):
        """
        修改外来词
        :param file:
        :param content:
        :return:
        """
        with open(file, 'r+', encoding="utf8") as f:
            content = f.read()
            word = re.findall("/(.*?)/", content)
            new_content = re.sub("/.*?/", "[/" + word[0] + "/]", content)

    def mod_unclear_word(self, file, content):
        blurry_word = re.findall(r"\((.*?)\)", content)

    def get_symbol(self, file):
        """
        提取文件中的特殊符号
        :param file: 特殊符号日志文件
        :return: 特殊符号集合
        """

        symbol_char = set()
        with open(file, 'r', encoding='utf8')as f:
            for line in f:
                file, error, content = line.strip().split("\t")
                symbol = error.replace("in contain symbol ", "").replace("out contain symbol ", "")
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

    def replace_parenthes(self, content):
        """
        替换 (()) 的情况 ,排处[(())]的情况，把(()) 替换成[()]
        :param content:
        :return:
        """
        one_content = re.sub("[[]*\(\(", "[((", content)
        return re.sub("\)\)[]]*", "))]", one_content)

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

    def process_japanese_pre(self, file):
        """
        处理日语txt 文件，日语txt 文件报含 wav文件名 删除wav文件名
        :param file: 文件路径
        :return:
        """
        with open(file, 'r+', encoding="utf8") as f:
            content = f.read()
            wav_file_name, txt_content = content.strip().split("\t")
            f.seek(0)
            f.truncate()
            f.write(txt_content.strip())

    def count_jepanese_charactor(self, log_file):
        """
        根据日志文件查找日语种噪音符号的标注
        :param log_file: 日志文件
        :return:
        """

        noise = set()
        with open(log_file, 'r', encoding='utf8')as f:
            for line in f:
                try:
                    file_path, error_message, content = line.strip().split("\t")
                except Exception as e:
                    pass
                else:
                    noise_content = re.findall("\[.*?\]", content)
                    for item in noise_content:
                        noise.add(item)
        print(noise)

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
            content = re.sub(r"[\[]+[a|B]+[\]]*", '[a]', content)
            content = re.sub(r"[\[]+[m|M]+[\]]*", '[m]', content)
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
                        # content = f.read().replace("下午", "")
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

    def sub_noise(self, file):
        """
        标准化噪音符号
        :param file:
        :return:
        """
        with open(file, "r+", encoding='utf8')as f:
            content = f.read()
            content = re.sub(r"[\[]+lipsmack[\]]+", "[[lipsmack]]", content)
            content = re.sub(r"[\[]+cough[\]]+", "[[cough]]", content)
            content = re.sub(r"[\[]+sneeze[\]]+", "[[sneeze]]", content)
            content = re.sub(r"[\[]+breath[\]]+", "[[breath]]", content)
            content = re.sub(r"[\[]+[background|Background|BACKGROUND]+[\]]+", "[[background]]", content)
            content = re.sub(r"[\[]+laugh[\]]+", "[[laugh]]", content)
            content = re.sub(r"[\[]+breath[\]]+", "[[breath]]", content)

            content = re.sub(r"[\[]+[lipmack|Lipmack|LIPMACK|lipmake|lipsmacl]+[\]]+", "[[lipsmack]]", content)

            content = re.sub(r"[\[]*\(\(", "[((", content)  # 处理外来词缺失中括号的情况
            content = re.sub(r"\)\)[\]]*", "))]", content)

            f.seek(0)
            f.truncate()
            f.write(content)

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
                error_files.add(file_path)

        for error_file in error_files:
            print(error_file)
            with open(error_file, 'r+', encoding='utf8')as f:
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

    def find_error_person(self, log_file):
        """
        查找出所有有问题的人路径
        :param log_file: 日志文件
        :return:
        """
        all_error = list()

        re_extr = re.compile(r".*data\\G\d+")
        with open(log_file, 'r', encoding='utf8')as f:
            for line in f:
                error_file, *_ = line.strip().split()
                data_path = re.search(re_extr, error_file).group()
                all_error.append(data_path)
        return list(set(all_error))

    def run(self):
        """
        主控制逻辑
        :return:
        """

        # 提取日志的特殊符号
        # symbol_chars = set()
        # symbol_logs = [
        #     r"error_out_contain_symbol.txt",
        # r"error_out_contain_symbol.txt"
        # ]
        # for file in symbol_logs:
        #     symbol_char = self.get_symbol(file)
        #     symbol_chars = symbol_chars | symbol_char
        # print(symbol_chars)

        # 分隔日志
        # log_file = r"D:\Workspace\Logs\11-log.log"
        # out_file_prefix = r"error_"
        # self.split_log(log_file, out_file_prefix)

        # 删除数据
        # with open('error_contains_numbers_is.txt', 'r', encoding='utf8') as f:
        #     for line in f:
        #         file = line.strip().split("\t")[0]
        #         self.err_file_remove(file)

        # 删除错误文件
        # with open('error_contains_numbers_is.txt', 'r', encoding='utf8') as f:
        #     for line in f:
        #         file = line.strip().split("\t")[0]
        #         os.remove(file)

        # 有疑问的,需要人工的数据导出数据导出
        # out_folder = r"D:\老数据人工修改部分\347小时意大利语手机采集语音数据"
        # error_file = r'error_contain_other_noisy.txt'
        # error_folder = os.path.join(out_folder, os.path.splitext(error_file)[0])
        # self.create_folder(error_folder)
        # with open(error_file, 'r', encoding='utf8') as f:
        #     for line in f:
        #         txt_file = line.strip().split("\t")[0]  # txt文件
        #         dest_txt = os.path.split(txt_file)[-1]
        #         wav_file = txt_file.replace("txt", 'wav')
        #         dest_wav = os.path.split(wav_file)[-1]
        #         shutil.copyfile(txt_file, os.path.join(error_folder, dest_txt))
        #         shutil.copyfile(wav_file, os.path.join(error_folder, dest_wav))

        # 可替换的字符替换
        # symbol_replace_map = {"<": ' ', ">": " ", ":": " ", "_": " ", "•": " ", '"': " ", "…": " ", ";": " ",
        #                       "\xad": "-", '—': "-", '“': " ", '”': " "}
        # seconde_symbol_replace = {'“': " ", '◎': " ", '・': " ", '．': " ", '（': " ", '。': " ", '：': " ", '☆': " ",
        #                           '”': " ", '…': " ", '）': " ", '《': " ", '『': " ", '』': " ", '"': " ", '？': " ",
        #                           ':': " ", '「': " ", '，': " ", '》': " ", '≒': " ", '【': " ", '」': " ", '】': " ",
        #                           }
        # symbol_replace_map.update(seconde_symbol_replace)
        #
        # error_file = r'error_out_contain_symbol.txt'
        # with open(error_file, 'r', encoding='utf8') as f:
        #     for line in f:
        #         file, error_message, content = line.strip().split("\t")
        #         error_symbol_list = eval(error_message.replace("in contain symbol ", "").replace("out contain symbol ", ""))
        #         for error_symbol in error_symbol_list:
        #             if error_symbol in symbol_replace_map:
        #                 with open(file, 'r+', encoding='utf8')as inner_f:
        #                     cont = inner_f.read()
        #                     new_content = re.sub(r"[\s]*{}[\s]*".format(error_symbol), symbol_replace_map[error_symbol],
        #                                          cont).strip()
        #                     new_content = new_content.replace("*", '')
        #                     inner_f.seek(0)
        #                     inner_f.truncate()
        #                     inner_f.write(new_content)

        # 模糊音格式错误修改
        # symbol_replace_map = {"<": ' ', ">": " ", ":": " ", "_": " ", "•": " ", '"': " ", "…": " ", ";": " ",
        #                       "\xad": "-", '—': "-"}
        # legal_character = {'-', '¿', '¡'}
        # error_file = r'error_in_contain_symbol.txt'
        # with open(error_file, 'r', encoding='utf8') as f:
        #     for line in f:
        #         file, error_message, content = line.strip().split("\t")
        #         error_symbol_list = eval(error_message.replace("in contain symbol ", "").replace("out contain symbol ", ""))
        #         error_symbol_set = set(error_symbol_list) - legal_character - set(symbol_replace_map.keys())
        #
        #         if error_symbol_set:
        #             with open(file, 'r+', encoding='utf8')as inner_f:
        #                 inner_content = inner_f.read()
        #                 flag = re.findall("\(\(.*?\)\)", inner_content)   # 处理(())情况
        #                 if flag:
        #                     new_content = self.replace_parenthes(inner_content)
        #                     inner_f.seek(0)
        #                     inner_f.truncate()
        #                     inner_f.write(new_content)

        # 人工处理部分
        # out_folder = r"D:\老数据人工修改部分\347小时意大利语手机采集语音数据"
        # error_folder = os.path.join(out_folder, "special_symbol")
        # self.create_folder(error_folder)
        # symbol_replace_map = {"<": ' ', ">": " ", ":": " ", "_": " ", "•": " ", '"': " ", "…": " ", ";": " ",
        #                       "\xad": "-", '—': "-"}
        # legal_character = {'-', '¿', '¡'}
        # error_file = r'error_out_contain_symbol.txt'
        # with open(error_file, 'r', encoding='utf8') as f:
        #     for line in f:
        #         file, error_message, content = line.strip().split("\t")
        #         error_symbol_list = eval(
        #             error_message.replace("in contain symbol ", "").replace("out contain symbol ", ""))
        #         error_symbol_set = set(error_symbol_list) - legal_character - set(symbol_replace_map.keys())
        #         if error_symbol_set:
        #             txt_file = line.strip().split("\t")[0]  # txt文件
        #             dest_txt = os.path.split(txt_file)[-1]
        #             wav_file = txt_file.replace("txt", 'wav')
        #             dest_wav = os.path.split(wav_file)[-1]
        #             shutil.copyfile(txt_file, os.path.join(error_folder, dest_txt))
        #             shutil.copyfile(wav_file, os.path.join(error_folder, dest_wav))

        # 统计所有的字符
        # project_folder = r"\\10.10.30.14\格式整理_ming\apy161101022_r_235小时日语手机采集语音数据_朗读\完整数据包_加密后数据\data"
        # chars = self.count_all_charactirs(project_folder)

        # 修改日语文本中有wav文件名的情况
        # project_folder = r"\\10.10.30.14\格式整理_ming\apy161101022_r_235小时日语手机采集语音数据_朗读\完整数据包_加密后数据\data"
        # for root, dirs, files in os.walk(project_folder):
        #     for file in files:
        #         if file.endswith("txt"):
        #             file_path = os.path.join(root, file)
        #             self.process_japanese_pre(file_path)

        # 获取日语中的噪音符号
        # log_file = r"D:\Workspace\Logs\10-log.log"
        # self.count_jepanese_charactor(log_file)

        # 补全日语中噪音符号
        # symbol_logs = [
        #     r"error_out_contain_symbol.txt"
        # ]
        # for file in symbol_logs:
        #     with open(file, 'r', encoding='utf8')as f:
        #         for line in f:
        #             file, error_message, cont = line.strip().split("\t")
        #             symbol = error_message.replace("in contain symbol ", "").replace("out contain symbol ", "")
        #             try:
        #                 chars = eval(symbol)
        #             except Exception as e:
        #                 print(symbol)
        #
        #             if "]" in chars or "[" in chars:
        #                 self.modify_noise_symbol(file)

        # 全角转半角
        # error_file = r'error_Has_double_str(quan.txt'
        # with open(error_file, 'r', encoding='utf8') as f:
        #     for line in f:
        #         file, error_message, content = line.strip().split("\t")
        #         print(file)
        #         with open(file, 'r+', encoding='utf8') as route_f:
        #             route_content = route_f.read()
        #             new_content = strQ2B(route_content)
        #             route_f.seek(0)
        #             route_f.truncate()
        #             route_f.write(new_content)

        # 补全字段缺失
        # folders = set()  # 统计缺失字段的录音人
        # miss_field_log = r"error_ACT_key_is.txt"
        # with open(miss_field_log, 'r', encoding='utf8')as log_f:
        #     for line in log_f:
        #         file, error_mg = line.strip().split("\t")
        #         group_folder = re.sub("\w+.metadata", '', file)
        #         folder = group_folder.rstrip('\\')
        #         folders.add(folder)

        # person_folder = r"\\10.10.30.14\格式整理_ming\APY161101029_r_292小时泰语手机采集语音数据_朗读\完整数据包_加密后数据\data\G1192"
        # self.filled_field(person_folder, {"SCC":"Quiet", "BIR": "Thailand", "ACT": "Thai"})

        # 统一噪音符号
        noise_error_log = r"error_out_contain_symbol.txt"
        with open(noise_error_log, 'r', encoding='utf8')as log_f:
            for line in log_f:
                file, error_mg, content = line.strip().split("\t")
                self.sub_noise(file)


        # 查看泰语中的数字是否是泰语数字
        # numbers = set()
        # error_message_log = r'error_contains_numbers_is.txt'
        # with open(error_message_log, 'r', encoding='utf8')as log_f:
        #     for line in log_f:
        #         file, error_mg, content = line.strip().split("\t")
        #         number = eval(error_mg.replace("contains numbers is ", ""))
        #         for n in number:
        #             numbers.add(n)
        # print(numbers)

        # 修改日志文件中，将男女转为英文
        # error_message_log = r'error_value_format_is.txt'
        # self.modify_gender_field(error_message_log)

        # 查找有问题的人的数据
        # log_file = r"error_content_contains_chinese.txt"
        # error_person = self.find_error_person(log_file)

        # 日语特殊字符筛选
        # special_symoble = {'―', '+', '=', '×', '/', '○', '&', 'Ⅴ', '─'}
        # file = r"error_out_contain_symbol.txt"
        # with open(file, 'r', encoding='utf8') as f:
        #     for line in f:
        #         file, error, content = line.strip().split("\t")
        #         symbol = error.replace("in contain symbol ", "").replace("out contain symbol ", "")
        #         symbol_set = set(eval(symbol)) & special_symoble
        #         if symbol_set:
        #             with open('san.txt', 'a', encoding='utf8')as f:
        #                 f.write(line)
        #         else:
        #             print(line)


if __name__ == '__main__':
    pd = ProcessData()
    pd.run()
