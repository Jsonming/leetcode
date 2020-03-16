#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/16 17:59
# @Author  : yangmingming
# @Site    : 
# @File    : redis_my.py
# @Software: PyCharm
import hashlib
import redis

def gen_md5(data):
    """
        生成md5
    :param data: 字符串数据
    :return:
    """
    md5 = hashlib.md5()
    md5.update(data.encode('utf-8'))
    return md5.hexdigest()

md5 = gen_md5


class MyRedis(object):
    def __init__(self):
        pool = redis.ConnectionPool(host='123.56.11.156', port=6379, db=0, password='')
        self.r = redis.Redis(connection_pool=pool)

    def generate_md5(self, str):
        md5 = hashlib.md5()
        data = str
        md5.update(data.encode('utf-8'))
        return md5.hexdigest()

    def hash_(self, name="fingerprint", string=None):
        return self.r.hset(name=name, key=string, value=1)

    def hash_exist(self, name='fingerprint', string=None):
        return self.r.hexists(name=name, key=string)

    def insert_(self, key, value):
        self.r.lpush(key, value)

    def get_finger(self):
        a = self.r.hkeys("fingerprint")
        print(a)


class SSDBCon(object):
    def __init__(self):
        """
        初始化连接SSDB数据库,
        链接SSDB数据库没有使用SSDB客户端，使用的是Redis客户端有两个原因
            1.可以无缝对接
            2.框架配合scrapy_redis使用
            3.这里的函数，没有删除数据函数，如果要执行删除操作 到数据库删除  SSDB数据库命令参考
             http://ssdb.io/docs/zh_cn/commands/index.html

        """
        db_host = '123.56.11.156'
        db_port = 8888
        self.conn = redis.StrictRedis(host=db_host, port=db_port)

    def connection(self):
        """
        返回数据库连接
        :return:
        """
        return self.conn

    def insert_to_list(self, name, value):
        """
        向列表中插入单个的值
        :param name: 列表名称
        :param value: 要插入的值
        :return:
        """
        if isinstance(value, str):
            self.conn.lpush(name, value)
        elif isinstance(value, list) or isinstance(value, tuple):
            self.conn.lpush(name, *value)

    def get_list(self, name, start=0, end=-1):
        """
        获取列表的内容
        :param name:
        :param start: 开始索引
        :param end: 结束索引
        :return:
        """
        return self.conn.lrange(name=name, start=start, end=end)

    def insert_to_hashmap(self, name, key, value=1):
        """
        插入到集合中,由于SSDB 没有set数据类型， 这里的集合采用排序集合sorted set
        :return:
        """
        if isinstance(key, str):
            self.conn.hset(name=name, key=key, value=value)
        else:
            raise TypeError("expected string got %s".format(value))

    def insert_finger(self, name, value):
        """
        将字符串md5插入集合
        :param name:
        :param value:
        :return:
        """
        self.insert_to_hashmap(name, md5(value))

    def exist_finger(self, name, value):
        """
        判断指纹是否存在
        :param name: 指纹库
        :param value: 需要验证的值
        :return:
        """
        return self.exist_in_hashmap(name, md5(value))

    def get_set(self, name, start=0, end=-1):
        """
        获取集合中的元素
        :param name:集合的键
        :return:
        """
        return self.conn.zrange(name=name, start=start, end=end)

    def exist_in_hashmap(self, name, key):
        """
        判断值是否在集合中
        :param name: 集合名称
        :param value: 值
        :return:
        """
        return self.conn.hexists(name=name, key=key)

    def close(self):
        """
        关闭数据库连接
        :return:
        """
        self.conn.connection_pool.disconnect()


if __name__ == '__main__':
    ssdb = SSDBCon()
    file = r"summary_phonetic.txt"
    with open(file, 'r', encoding="utf8")as f:
        for line in f:
            word = line.strip().split()[0]
            ssdb.insert_to_list("bing_word_urls", 'https://dict.cn/search?q={}'.format(word))
