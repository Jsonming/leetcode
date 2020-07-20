#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/2 14:27
# @Author  : yangmingming
# @Site    : 
# @File    : process_ppm.py
# @Software: PyCharm
import struct


class ProcessData(object):
    def __init__(self):
        pass

    def one(self):
        """
        主逻辑
        :return:
        """
        file_name = r"depth.ppm"
        with open(file_name, 'rb') as f, open("one.txt", 'a') as w_f:
            f.seek(17)
            flag = True
            while flag:
                high_bytes_read = f.read(1)
                lower_bytes_read = f.read(1)
                try:
                    high_val_arr, *_ = struct.unpack('B', high_bytes_read)
                    lower_val_arr, *_ = struct.unpack('B', lower_bytes_read)
                except Exception as e:
                    flag = False
                else:
                    e = int(high_val_arr) * 256 + int(lower_val_arr)
                    w_f.write(str(e) + "\n")

    def two(self):
        file_name = r"depth.ppm"
        with open(file_name, 'rb') as f, open("two_s.txt", 'a') as w_f:
            f.seek(17)
            high_bytes_read = f.read(1)
            lower_bytes_read = f.read(1)
            while high_bytes_read:
                e = ord(high_bytes_read) * 256 + ord(lower_bytes_read)
                high_bytes_read = f.read(1)
                lower_bytes_read = f.read(1)
                w_f.write(str(e) + "\n")


if __name__ == '__main__':
    pd = ProcessData()
    pd.two()
