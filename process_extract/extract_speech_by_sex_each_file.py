#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@File    :   extract_speech_by_sex_each_file.py    
@Contact :   liuxd
2020/9/1 13:43  
'''

import os
import shutil

import re
import wave


def to_copy(wav_path, work_dir, dest_dir):
    wav_dest = wav_path.replace(work_dir, dest_dir)

    dirname = os.path.dirname(wav_dest)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    txt_path = wav_path.replace('.wav', '.txt')
    meta_path = wav_path.replace('.wav', '.metadata')

    txt_dest = wav_dest.replace('.wav', '.txt')
    meta_dest = wav_dest.replace('.wav', '.metadata')

    shutil.copy(wav_path, wav_dest)
    shutil.copy(txt_path, txt_dest)
    shutil.copy(meta_path, meta_dest)


def get_meta_dict(meta_path):
    metadata_dict = {}
    try:
        with open(meta_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                l_list = line.split('\t')
                if len(l_list) > 1:
                    metadata_dict[l_list[0].strip()] = l_list[1].strip()
                elif len(l_list) == 1:
                    metadata_dict[l_list[0].strip()] = ""
    except Exception as e:
        print('err：' + meta_path)
        raise e
    return metadata_dict


def get_wav_durtion(wav_path):
    try:
        file = wave.open(wav_path)
        # print('---------声音信息------------')

        a = file.getparams().nframes  # 帧总数
        f = file.getparams().framerate  # 采样频率
        time = a / f  # 声音信号的长度
    except Exception as e:
        print(e)
        print("errorrrrr")
        return 0
        raise Exception
    return time


def main(work_dir, dest_dir):
    need = {'female': 3600,
            'male': 3600}

    for root, dirs, files in os.walk(work_dir):
        for file in files:
            if file.endswith('wav'):
                wav_path = root + '\\' + file
                meta_path = wav_path.replace('.wav', '.metadata')

                txt_path = wav_path.replace('.wav', '.txt')
                with open(txt_path, 'r', encoding='utf8') as f:
                    fr = f.read()
                # res = re.search('[1234567890]',fr)
                # if res:
                #     continue

                t = get_wav_durtion(wav_path)
                sex = get_meta_dict(meta_path)['SEX'].lower()
                if need[sex] > 0:
                    need[sex] -= t
                    to_copy(wav_path, work_dir, dest_dir)
                # print(need)
            if need['female'] < 0 and need['male'] < 0:
                return


if __name__ == '__main__':
    work_dir = r'\\10.10.30.14\语音数据_2016\APY161101019_R_794小时四川方言手机采集语音数据_朗读\完整数据包_加密后数据\data\category'
    dest_dir = r'\\10.10.30.14\刘晓东\数据产品统计信息\语音\四川方言两小时样例\data\category'
    main(work_dir, dest_dir)
