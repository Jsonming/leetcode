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
        txt_file = file.replace("txt", "wav")
        meta_file = file.replace("txt", "metadata")
        try:
            os.remove(file)
        except Exception as e:
            print(e)
        os.remove(txt_file)
        os.remove(meta_file)

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

    def run(self):
        """
        主控制逻辑
        :return:
        """

        # 提取日志的特殊符号
        # symbol_chars = set()
        # symbol_logs = [
        #     r"error_in_contain_symbol.txt",
        #     r"error_out_contain_symbol.txt"
        # ]
        # for file in symbol_logs:
        #     symbol_char = self.get_symbol(file)
        #     symbol_chars = symbol_chars | symbol_char
        # print(symbol_chars)

        # 分隔日志
        # log_file = r"D:\Workspace\workscript\Logs\log.log"
        # out_file_prefix = r"error_"
        # self.split_log(log_file, out_file_prefix)

        # 删除数据
        # with open('error_file_type_error.txt', 'r', encoding='utf8') as f:
        #     for line in f:
        #         file = line.strip().split("\t")[0]
        #         self.err_file_remove(file)

        # 删除错误文件
        # with open('error_file_type_error.txt', 'r', encoding='utf8') as f:
        #     for line in f:
        #         file = line.strip().split("\t")[0]
        #         os.remove(file)

        # 有疑问的,需要人工的数据导出数据导出
        # error_file = r'error_contain_other_noisy.txt'
        # out_folder = r"G:\老数据修改人工部分"
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
        #                       "\xad": "-", '—': "-"}
        # error_file = r'error_in_contain_symbol.txt'
        # with open(error_file, 'r', encoding='utf8') as f:
        #     for line in f:
        #         file, error_message, content = line.strip().split("\t")
        #         error_symbol_list = eval(error_message.replace("in contain symbol ", "").replace("out contain symbol ", ""))
        #         for error_symbol in error_symbol_list:
        #             if error_symbol in symbol_replace_map:
        #                 with open(file, 'r+', encoding='utf8')as inner_f:
        #                     cont = inner_f.read()
        #                     new_content = re.sub(r"[\s]*{}[\s]*".format(error_symbol), symbol_replace_map[error_symbol], cont).strip()
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
        # out_folder = r"G:\老数据修改人工部分"
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
        # project_folder = r"\\10.10.30.14\杨明明\修改测试demo\data"
        # chars = self.count_all_charactirs(project_folder)


if __name__ == '__main__':
    pd = ProcessData()
    pd.run()
