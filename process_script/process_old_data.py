#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/1 16:43
# @Author  : yangmingming
# @Site    : 
# @File    : process_old_data.py
# @Software: PyCharm


class ProcessData(object):
    def __init__(self):
        pass

    def split_log(self, log_file, out_file, error_type):
        """
        分解日志文件，
        :param log_file:日志文件
        :param out_file: 输出文件
        :param error_type: 文件错误类型
        :return:
        """
        with open(log_file, 'r', encoding='utf8') as log_f, open(out_file, 'a', encoding='utf8') as out_f:
            for line in log_f:
                content = line.strip()
                error_desc = content.split("\t")
                file = error_desc[0]
                error_class = "\t".join(error_desc[1:]).strip()
                if error_class == error_type:
                    out_f.write(file + "\n")

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

    def run(self):
        log_file = r"log.log"
        errot_type = r"Noise label format error"
        out_file = r"special_symbol_one.txt"
        self.split_log(log_file, out_file, errot_type)


if __name__ == '__main__':
    pd = ProcessData()
    pd.run()
