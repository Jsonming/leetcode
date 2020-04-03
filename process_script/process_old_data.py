#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/1 16:43
# @Author  : yangmingming
# @Site    : 
# @File    : process_old_data.py
# @Software: PyCharm
import re
import os

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
            content = re.sub(r"[\[]+lipsmack[\]]+", "[[lipsmack]]", content)
            content = re.sub(r"[\[]+cough[\]]+", "[[cough]]", content)
            content = re.sub(r"[\[]+sneeze[\]]+", "[[sneeze]]", content)
            content = re.sub(r"[\[]+breath[\]]+", "[[breath]]", content)
            content = re.sub(r"[\[]+background[\]]+", "[[background]]", content)
            content = re.sub(r"[\[]+laugh[\]]+", "[[laugh]]", content)
            content = re.sub(r"[\[]+breath[\]]+", "[[breath]]", content)
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

    def run(self):
        # log_file = r"D:\Workspace\workscript\Logs\log.log"
        # out_file_prefix = r"err_"
        # self.split_log(log_file, out_file_prefix)

        with open('err_contains_special_symbol.txt', 'r', encoding='utf8') as f:
            for line in f:
                file = line.strip().split("\t")[0]
                self.err_file_remove(file)


if __name__ == '__main__':
    pd = ProcessData()
    pd.run()
