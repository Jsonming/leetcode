#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/1 16:43
# @Author  : yangmingming
# @Site    : 
# @File    : process_old_data.py
# @Software: PyCharm
import re
import os
import shutil
from process_script.check_noise_annotation import get_noise_list


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
                if "[" in error_class:
                    error_class_name = "_".join(error_class.split()[:3])  # "["中括号不能作为文件名，选前三位作为文件名
                else:
                    error_class_name = "_".join(error_class.split())
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

    def run(self):
        # 分隔日志
        # log_file = r"D:\Workspace\workscript\Logs\log.log"
        # out_file_prefix = r"err_"
        # self.split_log(log_file, out_file_prefix)

        # 删除数据
        # with open('err_contains_special_symbol.txt', 'r', encoding='utf8') as f:
        #     for line in f:
        #         file = line.strip().split("\t")[0]
        #         self.err_file_remove(file)

        # 将文件拉倒本地
        # src_path = r'\\IT-20190729TRCT\数据备份_liuxd\apy170901049_347小时意大利语手机采集语音数据\完整数据包_加密后数据\data'
        # self.copy_txt(src_path)

        # 检查 txt问题
        # src_path = r"apy170901049_347小时意大利语手机采集语音数据.txt"
        # with open(src_path, 'r', encoding="utf8") as f:
        #     for line in f:
        #         line = line.strip()
        #         file, content = line.split("\t")
        #         check_noise_annotation_old_norm(file, content)

        # 修改/
        src_file = r"tem.txt"
        dest_foler = r"\\10.10.30.14\刘晓东\oracle_交付\人工修改\apy170901049_347小时意大利语手机采集语音数据"
        with open(src_file, 'r', encoding='utf8')as f:
            for line in f:
                file = line.strip()
                folder_path, file_name = os.path.split(file)
                meta_file = file_name.replace("txt", "metadata")
                wav_file = file_name.replace("txt", "wav")
                for item in [file_name, meta_file, wav_file]:
                    old_file_name = os.path.join(folder_path, item)
                    new_file_name = os.path.join(dest_foler, item)
                    shutil.copyfile(old_file_name, new_file_name)


def check_noise_annotation_old_norm(txt_path, input_str):
    # 获取配置文件的噪音标注列表
    noise_right_list = get_noise_list()
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


if __name__ == '__main__':
    pd = ProcessData()
    pd.run()
