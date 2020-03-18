#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/18 10:36
# @Author  : yangmingming
# @Site    : 
# @File    : douyin_get.py
# @Software: PyCharm

import hashlib
import json
import random
import re
import urllib.parse

import pymongo
import requests

# outer_reids_server = '39.98.232.174'
# intranet_redis_server = '172.26.26.133'
# outer_mongo_server = '47.92.174.37'
# intranet_mongo_server = '172.26.26.132'

useragent_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
]
useragent = random.choice(useragent_list)
item1 = {}


class Start(object):
    def __init__(self):
        # 用户id配置
        self.user_id = '102220954116'
        # id
        self.dou_yin_id = '1212930875'
        # sign配置
        self._signature = 'o5dpuRAd.nZm8jE0qwb.laOXaa'
        # headers头
        self.headers = {
            'user-agent': useragent,
        }
        # MonGo连接
        # MonGo_cli = pymongo.MongoClient(host='127.0.0.1',port=27017)['web_page']['douyin_detail']
        # MonGo_cli = pymongo.MongoClient("mongodb://xhql:" + urllib.parse.quote_plus(
        #     "xhql_190228_snv738J72*fjVNv8220aiVK9V820@_") + "@47.92.174.37:20388/webpage")["webpage"]["douyin_details"]

        # redis链接
        # r = redis.StrictRedis(host='127.0.0.1', port=6379, db=8)
        # r = redis.StrictRedis(host='39.98.232.174', port=8990, db=6,
        #                       password='28JCi*289V92ofj2owoBkv8282928SKVISmv8920565LjhMcs')

    def get_page(self, max_cursor):
        url = "https://www.iesdouyin.com/share/user/{}".format(self.user_id)
        source = requests.get(url, headers=self.headers)
        source.encoding = 'utf-8'
        # dytk
        dytk = re.search("dytk: '(.*?)'", source.text).group(1)
        # 抖音名
        nickname = re.search('<p class="nickname">(.*?)</p>', source.text).group(1)
        try:
            type = re.search('<span class="info">(.*?)</span>', source.text).group(1).replace(' ', '')
        except:
            type = ''

        url_detail = 'https://www.iesdouyin.com/web/api/v2/aweme/post/?'
        params = {
            'user_id': self.user_id,
            'count': '21',
            'max_cursor': max_cursor,
            'aid': '1128',
            '_signature': self._signature,  # 目前需要手动更换
            'dytk': dytk
        }
        response = requests.get(url=url_detail, params=params, headers=self.headers)
        list = json.loads(response.text)['aweme_list']
        print(response.text)
        has_more = json.loads(response.text)['has_more']

        for item in list:
            user_id = self.user_id  # 用户id
            title = item['desc']  # 读取视频名称
            video = item['video']['play_addr']['uri']  # 读取视频uri
            video_url = "https://aweme.snssdk.com/aweme/v1/playwm/?video_id={}".format(video)  # 拼接视频地址

            # id
            id_md5 = hashlib.md5(video_url.encode("utf-8"))
            id = id_md5.hexdigest()

            print(nickname, user_id, title, type, video_url, id)
            # mongo_save(nickname, user_id, title, type, video_url, id)
            # redis_config(video_url)

        if has_more != False:
            max_cursor = json.loads(response.text)['max_cursor']
            print(max_cursor)
            # get_page(max_cursor)
        else:
            return

    def mongo_save(self, nickname, user_id, title, type, video_url, id):
        item1['id'] = id
        item1['dou_yin_id'] = self.dou_yin_id
        item1['nickname'] = nickname
        item1['user_id'] = user_id
        item1['title'] = title
        item1['type'] = type
        item1['video_url'] = video_url
        print(item1)

        # if MonGo_cli.update({'id': item1['id']}, item1, True):
        #     print(
        #         '------------------------------------------Save_MonGo_Success------------------------------------------')

    def redis_config(self, video_url):
        print(video_url)
        # md5_data = md5_(video_url)
        # sta = hash_exist(md5_data)
        # if sta == False:
        #     print("入库待抓url:%s" % (video_url))
        #     hash_(md5_data)
        #     # r.lpush('douyin_seeds',video_url)
        # else:
        #     pass

    def md5_(self, str):
        md5 = hashlib.md5()
        data = str
        md5.update(data.encode('utf-8'))
        return md5.hexdigest()

    # def hash_(,str):
    #     return r.hset(name="douyin_fingerprint", key=str, value=1)
    #
    # def hash_exist(,str):
    #     print(r.hlen('douyin_fingerprint'))
    #     return r.hexists(name='douyin_fingerprint',key=str)


if __name__ == '__main__':
    Spider = Start()
    Spider.get_page('')
