#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/28 11:42
# @Author  : yangmingming
# @Site    : 
# @File    : tool.py
# @Software: PyCharm

import hashlib


def get_md5_value(src):
    """
        调用获取md5值的函数，返回文件的十六进制结果，并返回Md5结果
    :param src:
    :return:
    """
    try:
        with open(src, "rb") as fobj:
            code = fobj.read()

            myMd5 = hashlib.md5()  # 调用hashlib里的md5()生成一个md5 hash对象
            myMd5.update(code)  # 生成hash对象后，就可以用update方法对字符串进行md5加密的更新处理
            myMd5_Digest = myMd5.hexdigest()  # 加密后的十六进制结果

            return myMd5_Digest  # 返回十六进制结果
    except Exception as e:
        raise e
