import os, shutil, re
import re


def strQ2B(txt_path):
    global noise
    """全角转半角"""
    with open(txt_path, 'r', encoding='utf-8') as fr:
        ustring = fr.read()

    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化

            inside_code -= 65248
        rstring += chr(inside_code)
    rstring = rstring.replace('。', '.').replace('【', '[').replace('】', ']').replace('〜', '~')
    noise_find = re.findall('\\[\\[.*?\\]\\]', rstring)
    with open('1.txt', 'a+', encoding='utf-8') as fff:
        for each in noise_find:
            if not each in noise:
                fff.write(txt_path + '\n')
                print('noise_err:\t' + txt_path)
    label = re.sub("\\[\(\(.*?\)\)\\]", " ", rstring)
    label = re.sub("\\[/.*?/\\]", " ", label)
    label = re.sub("\\[\\[.*?\\]\\]", " ", label)
    return label


def to_start(work_dir):
    for root, dirs, files in os.walk(work_dir):
        for file in files:
            if file.endswith('txt'):
                txt_path = os.path.join(root, file)
                check_string = strQ2B(txt_path)
                if '[' in check_string or ']' in check_string:
                    print(txt_path)
                    print(check_string)
                    # with open('1.txt', 'a+', encoding='utf-8') as fff:
                    #     print(check_string)
                    #     print(txt_path)
                    #     fff.write(txt_path+'\n')
                    with open(txt_path, 'r', encoding='utf-8') as fr:
                        s = fr.read()

                    # with open(txt_path,'w',encoding='utf-8') as fw:
                    #     # s = s.replace('[lipsmack]','[[lipsmack]]').replace('[background]','[[background]]').replace('[[[','[[').replace(']]]',']]')
                    #     # s = re.sub("[^\\[]*\\[lipsmack\\][^\\[]*","",s)
                    #     s = s.replace('[{','').replace('}]','')
                    #     fw.write(s)


def check_tap(work_dir):
    for root, dirs, files in os.walk(work_dir):
        for file in files:
            if file.endswith('txt'):
                txt_path = os.path.join(root, file)
                with open(txt_path, 'r', encoding='utf-8') as f:
                    fr = f.read()
                fr_list = fr.split('\t')
                if len(fr_list) > 1:
                    new_fr = fr_list[-1]
                    print(txt_path)
                    # with open(txt_path,'w',encoding='utf-8') as fw:
                    #     fw.write(new_fr)


if __name__ == '__main__':
    noise = []
    noise.append('[[lipsmack]]')
    noise.append('[[laugh]]')
    noise.append('[[cough]]')
    noise.append('[[sneeze]]')
    noise.append('[[breath]]')
    noise.append('[[background]]')
    noise = set(noise)

    work_dir = r'E:\数据备份\apy161101033_g_405人法语手机采集语音数据\完整数据包_processed\data\category'
    print(work_dir)
    to_start(work_dir)
    # check_tap(work_dir)
