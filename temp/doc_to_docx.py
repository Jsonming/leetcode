#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/23 15:45
# @Author  : yangmingming
# @Site    : 
# @File    : doc_to_docx.py
# @Software: PyCharm


from win32com import client as wc

w = wc.Dispatch('Word.Application')
# 或者使用下面的方法，使用启动独立的进程：
# w = wc.DispatchEx('Word.Application')

file_path = r"D:\Workspace\workscript\temp\8a820143709f85660170cced2a14282c_智芯（物资）-第二十二批成交结果公告.doc"
doc = w.Documents.Open(file_path)

doc.SaveAs(r"D:\Workspace\workscript\temp\8a820143709f85660170cced2a14282c_智芯（物资）-第二十二批成交结果公告.docx", FileFormat=16)
doc.Close()
