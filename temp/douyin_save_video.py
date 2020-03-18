#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/18 10:37
# @Author  : yangmingming
# @Site    : 
# @File    : douyin_save_video.py
# @Software: PyCharm

import hashlib
import redis
import requests


class Start():
    def __init__():
        r = redis.StrictRedis(host='127.0.0.1', port=6379, db=9)
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Mobile Safari/537.36'
        }

    def get_video_url():
        num = r.llen('douyin_seeds')
        for i in range(num):
            i = i + 1
            print('总条数:', num, '现在第{}条'.format(i))
            # lpop出一个视频的链接
            go_out = r.lpop('douyin_seeds')
            video_url = str(go_out).lstrip('b').replace("'", '')
            print(video_url)
            if 'playwm' in video_url:
                replac = video_url.replace('playwm', 'play')
                video_add = replac
                download_video(video_url, video_add)
            else:
                quit()

    def download_video(, video_url, video_add):
        # 写入视频
        mp4 = requests.get(video_add, headers=headers, stream=True, verify=False).content
        id_md5 = hashlib.md5(video_url.encode("utf-8"))
        id = id_md5.hexdigest()
        try:
            open('D:/douyin_video/' + id + '.mp4', 'wb').write(mp4)
            print("下载完成")
        except Exception as e:
            print(e)
            pass


if __name__ == '__main__':
    Spider = Start()
    Spider.get_video_url()
