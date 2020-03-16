#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/12 9:07
# @Author  : yangmingming
# @Site    : 
# @File    : mysql_in.py
# @Software: PyCharm
import pymysql


class MysqlCon(object):
    def __init__(self):
        """
        初始化连接mysql数据库
        """
        self.db_conn = pymysql.connect(
            host='123.56.11.156',
            user='sjtUser',
            passwd='sjtUser!1234',
            port=3306,
            db='spiderframe',
            charset='utf8',
            use_unicode=True)
        self.db_cur = self.db_conn.cursor()

    def insert_data(self, table_name, item):
        """
        插入数据到数据中
        :param table_name:
        :param item:
        :return:
        """
        keys, values = [], []
        for key, value in item.items():
            keys.append(key)
            values.append(value)

        para = ["%s"] * len(keys)
        sql = 'INSERT INTO {db_name}({keys}) VALUES({para})'.format(db_name=table_name, keys=",".join(keys),
                                                                    para=",".join(para))
        self.db_cur.execute(sql, values)
        self.db_conn.commit()

    def create_table(self, table_name):
        """
        创建数据库
        :param table_name:
        :return:
        """
        sql = """create table {} (
              `id` int(11) NOT NULL AUTO_INCREMENT,
              `spider_name` varchar(32),
              `fingerprint` varchar(32),
              `category` varchar(32),

              `url` varchar(480),
              `title` varchar(480),
              `content` longtext,
              PRIMARY KEY (`id`)
            )ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;""".format(table_name)
        self.db_cur.execute(sql)
        self.db_conn.commit()

    def exist_table(self, table_name):
        """
        判断表是否存在， 查询表是否存在
        :param table_name:
        :return:
        """
        self.db_cur.execute(
            "select count(1) from information_schema.tables where table_name ='{table_name}';".format(**locals()))
        return self.db_cur.fetchone()[0]

    def close(self):
        self.db_conn.commit()
        self.db_conn.close()


if __name__ == '__main__':
    con = MysqlCon()
    file = r"summary_phonetic.txt"
    with open(file, 'r', encoding="utf8")as f:
        for line in f.readlines()[5:]:
            word = line.strip().split()[0]
            try:
                con.insert_data(table_name="English_word_phonetic", item={"word": word})
            except Exception as e:
                print(e)
