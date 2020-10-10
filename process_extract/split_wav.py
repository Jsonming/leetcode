import os
import shutil

import wave
import numpy as np
import pylab as plt

import contextlib
import numpy as np
import matplotlib.pyplot as plt

from scipy.io import wavfile
from pydub import AudioSegment
import random

def get_ms_part_wav(main_wav_path, start_time, end_time, part_wav_path):
    '''
    音频切片，获取部分音频 单位是毫秒级别
    :param main_wav_path: 原音频文件路径
    :param start_time:  截取的开始时间
    :param end_time:  截取的结束时间
    :param part_wav_path:  截取后的音频路径
    :return:
    '''
    start_time = int(start_time)
    end_time = int(end_time)

    sound = AudioSegment.from_mp3(main_wav_path)
    word = sound[start_time:end_time]

    word.export(part_wav_path, format="wav")


def get_sex(meta_path):
    sex_dict={}
    id_dict = {}
    i = 1
    with open(meta_path,'r',encoding='utf-8') as f:
        s_list =  f.readlines()[18].strip().split('\t')[1].split(',')
        for each in s_list:
            p = each.split('_')[0]
            sex = each.split('_')[1][0]
            sex_dict[p]=sex
            id_dict[p] = i
            i+=1
    return sex_dict,id_dict
    # print(sex_dict)

def wav_process(wav_path,num):
    global dest_dir
    
    # meta_path = wav_path.replace('wav','metadata')
    # 获取性别，放到字典里
    # sex_dict,id_dict = get_sex(meta_path)
    # 新建一个字典存放 speaker id
    
    txt_path = wav_path.replace('wav','txt')

    name = wav_path.split('\\')[-1].split('.')[0]
    word_num = 0
    with open(txt_path,'r',encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            line_list = line.split('\t')
            if len(line_list) == 4:
                word_num+=1
                start = int(float(line_list[0])*1000)
                end = int(float(line_list[1])*1000)
                who = line_list[2]
                content = line_list[3].lower()
                # new_name = 'PTO'+sex_dict[who]+str(num)+str(id_dict[who])+'_'+str(word_num).zfill(4)+'.wav'
                new_name = name+'_'+str(word_num).zfill(4)
                wav_save = dest_dir+'\\'+str(num)+'_'+new_name+'.wav'
                get_ms_part_wav(wav_path,start,end,wav_save)
                # txt_save = dest_dir+'\\'+new_name+'.txt'
                txt_save = dest_dir+'\\'+new_name+'.txt'


                # with open(txt_save,'w+',encoding='utf-8') as fw:
                #     fw.write(content)


def explore(work_dir,dest_dir):

    # for file in os.listdir(work_dir):
    num = 0
    wav_lst = []
    for root,dirs,files in os.walk(work_dir):
        for file in files:
            if file.endswith('phone.wav'):
                wav_path = os.path.join(root,file)
                wav_lst.append(wav_path)

    import random
    need = random.sample(wav_lst,400)

    # print(len(wav_lst))
    for wav_path in need:

        num +=1
        print(num)
        try:

            wav_process(wav_path,num)
        except:
            print(wav_path)



if __name__ == '__main__':
    work_dir = r'\\10.10.8.123\500小时粤语自然对话语音采集\607.8小时结果数据\结果数据\data\category'
    dest_dir = r'D:\data\自然对话有效语音截取\粤语'
    explore(work_dir,dest_dir)

    work_dir = r'\\10.10.8.123\700小时四川方言自然对话标注\整体入库数据2\data\category'
    dest_dir = r'D:\data\自然对话有效语音截取\四川方言自然对话'
    num = 0
    wav_lst = []
    for root,dirs,files in os.walk(work_dir):
        for file in files:
            if file.endswith('.wav'):
                wav_path = os.path.join(root,file)
                wav_lst.append(wav_path)

    
    need = random.sample(wav_lst,600)

    print(len(wav_lst))

    for wav_path in need:
        try:

            wav_process(wav_path,num)
        except:
            print(wav_path)

