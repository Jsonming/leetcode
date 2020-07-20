#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/2 10:17
# @Author  : yangmingming
# @Site    : 
# @File    : baidu_zhidao.py
# @Software: PyCharm
import pymssql
import pandas

import pyodbc


class BaiduZhiDao(object):
    def __init__(self):
        pass

    def new_con(self):

        def get_sms_operator(sectorNumber='0'):
            cnxn = pyodbc.connect("DRIVER={SQL SERVER};SERVER=10.10.11.35;DATABASE=ddddd;UID=sa;PWD=liuxd")
            cur = cnxn.cursor()
            select = """SELECT ID
              , BigClass
              , SmallClass
              , Solved
              , QuestionDetail
              , QuestionSupplement
              , BestAnswer
              , OtherAnswers
              , FromUrl
              , SolveTime
              , SubmitTime
              , Score
FROM ddddd.dbo.Baidu_Zhidao2 where ID = 4001663;"""
            cur.execute(select)
            # rows=cur.fetchall()
            row = cur.fetchone()
            if row:
                return row
            else:
                raise Exception("There seems no operator on sector:" + str(sectorNumber))
            cnxn.close()

        for row in get_sms_operator(0):
            print(row)

    def run(self):
        """
        主逻辑
        :return:
        """
        self.new_con()


if __name__ == '__main__':
    bd = BaiduZhiDao()
    bd.run()

