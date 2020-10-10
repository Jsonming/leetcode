#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/21 18:12
# @Author  : yangmingming
# @Site    : 
# @File    : extract_data.py
# @Software: PyCharm
import csv
import os
import random
import re
import shutil
from collections import defaultdict
from multiprocessing import Pool
from pydub import AudioSegment
import json
from workscript.dingding.dingding_decorator import dingding_monitor
from workscript.common.tool import get_md5_value


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


class ExtractData(object):
    def __init__(self):
        pass

    def async_executive(self, func, args):
        """
        多进程执行函数
        :param func: 函数
        :param args: 参数
        :return:
        """
        pool = Pool(processes=4)
        pool.map(func, args)
        pool.close()
        pool.join()

    def one(self):
        yellow, green = [], []
        project_path = r"\\10.10.8.123\自采全国车牌数据\客户数据\format_all\data_0818_liuxd_result_result_shen_20200831\最终数据（无措）"
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith('.jpg'):
                    file_path = os.path.join(root, file)

                    if "yellow_double_card" in file_path:
                        yellow.append(file_path)
                    elif "green_card" in file_path:
                        green.append(file_path)
                    else:
                        pass

        result = []
        result.extend(random.sample(yellow, 6000))
        result.extend(random.sample(green, 2000))
        for file in result:
            new_file = file.replace(
                r"\\10.10.8.123\自采全国车牌数据\客户数据\format_all\data_0818_liuxd_result_result_shen_20200831\最终数据（无措）",
                r"\\10.10.30.14\刘晓东\数据提取\彭颖岚\8000张车牌数据\data")

            new_folder = os.path.split(new_file)[0]
            if not os.path.exists(new_folder):
                os.makedirs(new_folder)
            shutil.copyfile(file, new_file)

    def two(self):
        """
        统计一下亚洲人占比
        :return:
        """
        result = defaultdict(int)
        project_path = r"\\10.10.30.14\d\图像\APY180921001_70,846张人脸抠图数据\完整数据包_processed\data\category_1\session_04_photoshop"
        for root, dirs, files in os.walk(project_path):
            for file in files:
                file_path = os.path.join(root, file)
                # if file_path.endswith('.json'):
                # with open(file_path, 'r', encoding='utf8')as f:
                #     content = json.load(f)
                #     race = content.get("WorkLoad", {}).get("race")
                #     result[race] += 1
                # print(result)
                if file_path.endswith('.jpg'):
                    file_name = os.path.split(file_path)[-1]
                    race = file_name.split(".")[0].split("_")[-1]
                    result[race] += 1
        print(result)

    def three(self):
        """
        晓东提取数据
        :return:
        """
        file_list, gen_word = [], defaultdict(list)
        project_path = r"\\10.10.30.14\d\文本\APY190921001_汉语多音字语料库\完整数据包\data"
        for root, dirs, files in os.walk(project_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_list.append(file_path)

        with open('多音字文本属性.csv', 'a', encoding='gbk', newline="")as new_f:
            myWriter = csv.writer(new_f)
            myWriter.writerow(["content"])
            for item in file_list[10:20]:
                print(item)
                with open(item, 'r', encoding='utf8')as f:
                    content = f.readlines()
                    select_content = random.sample(content, 20)
                    for cont in select_content:
                        key_word = re.sub("(\w)(\[\w+])", r"<marker category=DYZ>\1</marker>", cont).strip()
                        myWriter.writerow([key_word])

    def extract_4(self):
        file = r"\\10.10.30.14\刘晓东\数据提取\aaaaa实验数据\50个实验\3\46、数字拼音标注\data\data.txt"
        with open(file, 'r', encoding='utf8')as f, open('数字文本属性.csv', 'a', encoding='gbk', newline="")as new_f:
            myWriter = csv.writer(new_f)
            myWriter.writerow(["content"])
            content = f.readlines()
            extract_res = random.sample(content, 200)
            for line in extract_res:
                line = line.strip()
                new_line = re.sub("\s*<.*>(\d+)<.*>\s*", r"<marker category=SZ>\1</marker>", line).strip()
                myWriter.writerow([new_line])
                # print(new_line)

    def extract_5(self):
        """提取替换阿里外语数据"""
        del_file = r"\\10.10.30.14\刘晓东\数据提取\彭颖岚\阿里外语\颖岚客户法语操作\法语待补充.txt"
        with open(del_file, 'r', encoding='utf8')as del_f:
            for line in del_f:
                file_p = line.strip().split("\t")
                src_txt_file = file_p[0]
                src_wav_file = src_txt_file.replace(".txt", ".wav")
                src_meta_file = src_txt_file.replace(".txt", ".metadata")
                dest_txt_file = src_txt_file.replace(r"\\10.10.8.123\十国自制项目\法语\整体入库",
                                                     r"\\10.10.30.14\刘晓东\数据提取\彭颖岚\阿里外语\100小时法语")
                dest_wav_file = dest_txt_file.replace(".txt", ".wav")
                dest_meta_file = dest_txt_file.replace(".txt", ".metadata")
                shutil.copyfile(src_txt_file, dest_txt_file)
                shutil.copyfile(src_wav_file, dest_wav_file)
                shutil.copyfile(src_meta_file, dest_meta_file)

    def extract_6(self):
        del_file = r"\\10.10.30.14\刘晓东\数据提取\彭颖岚\阿里外语\颖岚客户意大利语操作\意大利待补充数据.txt"
        with open(del_file, 'r', encoding='utf8')as del_f:
            for line in del_f:
                file_p = line.strip().split("\t")
                src_txt_file = file_p[0]
                src_wav_file = src_txt_file.replace(".txt", ".wav")
                src_meta_file = src_txt_file.replace(".txt", ".metadata")

                src_txt_info = src_txt_file.split("\\")
                dest_txt_file = r"\\10.10.30.14\刘晓东\数据提取\彭颖岚\阿里外语\200小时意大利语\data\category" + "\\" + src_txt_info[
                    -2] + "\\" + src_txt_info[-1]
                dest_wav_file = dest_txt_file.replace(".txt", ".wav")
                dest_meta_file = dest_txt_file.replace(".txt", ".metadata")
                shutil.copyfile(src_txt_file, dest_txt_file)
                shutil.copyfile(src_wav_file, dest_wav_file)
                shutil.copyfile(src_meta_file, dest_meta_file)

    def extract_7(self):
        del_file = r"\\10.10.30.14\刘晓东\数据提取\彭颖岚\阿里外语\颖岚客户德语操作\德语后补.txt"
        with open(del_file, 'r', encoding='utf8')as del_f:
            for line in del_f:
                file_p = line.strip().split("\t")
                src_txt_file = file_p[0]
                src_wav_file = src_txt_file.replace(".txt", ".wav")
                src_meta_file = src_txt_file.replace(".txt", ".metadata")

                src_txt_info = src_txt_file.split("\\")
                dest_txt_file = r"\\10.10.30.14\刘晓东\数据提取\彭颖岚\阿里外语\100小时德语\data\category" + "\\" + src_txt_info[
                    -2] + "\\" + src_txt_info[-1]
                dest_wav_file = dest_txt_file.replace(".txt", ".wav")
                dest_meta_file = dest_txt_file.replace(".txt", ".metadata")
                shutil.copyfile(src_txt_file, dest_txt_file)
                shutil.copyfile(src_wav_file, dest_wav_file)
                shutil.copyfile(src_meta_file, dest_meta_file)

    def extract_8(self):
        """
        提取日本王程晨数据

        :return:
        """

        def copy_person(path):
            """
            拷贝一个路径下面的七张图片
            :param path:
            :return:
            """
            cert_path = os.path.join(path, "C1.jpg")
            mask_down_path = os.path.join(path, "mask_down.jpg")
            mask_normal_path = os.path.join(path, "mask_normal.jpg")
            mask_up_path = os.path.join(path, "mask_up.jpg")
            nomask_down_path = os.path.join(path, "nomask_down.jpg")
            nomask_normal_path = os.path.join(path, "nomask_normal.jpg")
            nomask_up_path = os.path.join(path, "nomask_up.jpg")

            dest_cert_path = cert_path.replace(src_project_path, dest_project_path)
            dest_folder = os.path.split(dest_cert_path)[0]
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)
            shutil.copy(cert_path, dest_folder)
            shutil.copy(mask_down_path, dest_folder)
            shutil.copy(mask_normal_path, dest_folder)
            shutil.copy(mask_up_path, dest_folder)
            shutil.copy(nomask_down_path, dest_folder)
            shutil.copy(nomask_normal_path, dest_folder)
            shutil.copy(nomask_up_path, dest_folder)

        src_project_path = r"\\10.10.30.14\d\图像\APY200215001_1,058人面部遮挡多姿态人脸识别数据\完整数据包\data"
        dest_project_path = r"\\10.10.30.14\刘晓东\数据提取\王程晨\300人面部遮挡多姿态人脸识别数据\data"
        male_list, female_list = [], []
        for folder in os.listdir(src_project_path):
            person_folder = os.path.join(src_project_path, folder)
            number, sex, county, age = folder.split("_")
            if sex == "male":
                male_list.append(person_folder)
            else:
                female_list.append(person_folder)
        select_male = random.sample(male_list, 150)
        select_female = random.sample(female_list, 150)
        # for item in select_male:
        #     copy_person(item)
        # for item in select_female:
        #     copy_person(item)

    def extract_9(self):
        """
        检查周彦的数据
        :return:
        """
        old_folder = set()
        old_project = r"\\10.10.8.123\刘晓东2\提取数据\jueni\APY190318003\data"
        for root, dirs, files in os.walk(old_project):
            for dir in dirs:
                old_folder.add(dir)

        new_project = r"\\10.10.8.123\印尼语项目\0831入库\data"
        for root, dirs, files in os.walk(new_project):
            for dir in dirs:
                if dir not in old_folder:
                    folder_path = os.path.join(root, dir)
                    new_folder = folder_path.replace(r"\\10.10.8.123\印尼语项目\0831入库\data",
                                                     r"\\10.10.30.14\刘晓东\数据提取\Jue Ni\APY190318003\data")
                    shutil.copytree(folder_path, new_folder)

    def extract_10(self):
        """
        提取婴儿哭声
        :return:
        """
        project_folder = r"\\10.10.30.14\d\语音\APY190410001_201人婴幼儿啼哭语音数据\完整数据包_processed\data\category"
        src_folder = r"\\10.10.30.14\d\语音\APY190410001_201人婴幼儿啼哭语音数据\完整数据包_processed\data"
        dest_folder = r"\\10.10.30.14\刘晓东\数据提取\沈杰\201人婴幼儿啼哭语音数据\data"
        for person in os.listdir(project_folder):
            person_folder = os.path.join(project_folder, person)
            person_txt_list = [os.path.join(person_folder, file) for file in os.listdir(person_folder) if
                               file.endswith(".txt")]
            duration = 0
            for person_txt in person_txt_list:
                person_wav = person_txt.replace(".txt", ".wav")
                person_meta = person_txt.replace(".txt", ".metadata")

                with open(person_txt, 'r', encoding='utf8')as f:
                    for line in f:
                        start, end = line.strip().split()
                        duration = float(end) - float(start)
                        if duration > 30:
                            extract_person_wav = person_wav.replace(src_folder, dest_folder)
                            extract_folder = os.path.split(extract_person_wav)[0]
                            if not os.path.exists(extract_folder):
                                os.makedirs(extract_folder)
                            get_ms_part_wav(person_wav, float(start) * 1000, float(start) * 1000 + 30 * 1000,
                                            extract_person_wav)
                            shutil.copy(person_meta, extract_folder)
                            break
                if duration > 30:
                    break

    def extract_11(self):
        """
        检查补充 沈杰的数据
        :return:
        """
        project_folder = [
            r"\\10.10.30.14\d\语音\APY190410001_201人婴幼儿啼哭语音数据\完整数据包_processed\data\category\G0043",
            r"\\10.10.30.14\d\语音\APY190410001_201人婴幼儿啼哭语音数据\完整数据包_processed\data\category\G0096",
            r"\\10.10.30.14\d\语音\APY190410001_201人婴幼儿啼哭语音数据\完整数据包_processed\data\category\G0168",
            r"\\10.10.30.14\d\语音\APY190410001_201人婴幼儿啼哭语音数据\完整数据包_processed\data\category\G0170",
            r"\\10.10.30.14\d\语音\APY190410001_201人婴幼儿啼哭语音数据\完整数据包_processed\data\category\G0193",
        ]
        src_folder = r"\\10.10.30.14\d\语音\APY190410001_201人婴幼儿啼哭语音数据\完整数据包_processed\data"
        dest_folder = r"\\10.10.30.14\刘晓东\数据提取\沈杰\201人婴幼儿啼哭语音数据\data"
        for person in project_folder:
            person_txt_list = [os.path.join(person, file) for file in os.listdir(person) if file.endswith(".txt")]
            sum_duration = 0
            for person_txt in person_txt_list:
                person_wav = person_txt.replace(".txt", ".wav")
                person_meta = person_txt.replace(".txt", ".metadata")
                with open(person_txt, 'r', encoding='utf8')as f:
                    line = f.readline()
                    start, end = line.strip().split()
                    if sum_duration < 30:
                        duration = float(end) - float(start)
                        tem_duration = sum_duration + duration
                        extract_person_wav = person_wav.replace(src_folder, dest_folder)
                        extract_folder = os.path.split(extract_person_wav)[0]
                        if not os.path.exists(extract_folder):
                            os.makedirs(extract_folder)
                        if tem_duration < 30:
                            get_ms_part_wav(person_wav, float(start) * 1000, float(end) * 1000, extract_person_wav)
                            shutil.copy(person_meta, extract_folder)
                            sum_duration = tem_duration
                        else:
                            lack = 30 - sum_duration
                            get_ms_part_wav(person_wav, float(start) * 1000, float(start) * 1000 + lack * 1000,
                                            extract_person_wav)
                            shutil.copy(person_meta, extract_folder)
                            sum_duration = 30

    def extract_12(self):
        """
        提取手势关键点数据
        :return:
        """

        def to_copy(files, folder):
            """
            拷贝文件
            :param files:
            :return:
            """
            src_path = r"\\10.10.30.14\d\图像\APY181130001_314178张18种手势识别数据\完整数据包_processed\data"
            dest_path_sub = r"\\10.10.30.14\刘晓东\数据提取\彭颖岚\bilibili\30000张手势关键点（含标注）\data"
            new_folder = folder.replace(src_path, dest_path_sub)
            if not os.path.exists(new_folder):
                os.makedirs(new_folder)
            for file in files:
                shutil.copy(file, new_folder)
                shutil.copy(file.replace(".json", ".jpg"), new_folder)

        project_folders = [
            r"\\10.10.30.14\d\图像\APY181130001_314178张18种手势识别数据\完整数据包_processed\data\gesture01_Number-1",
            r"\\10.10.30.14\d\图像\APY181130001_314178张18种手势识别数据\完整数据包_processed\data\gesture02_Number-2",
            r"\\10.10.30.14\d\图像\APY181130001_314178张18种手势识别数据\完整数据包_processed\data\gesture05_Number-5",
            r"\\10.10.30.14\d\图像\APY181130001_314178张18种手势识别数据\完整数据包_processed\data\gesture06_Number-6",
            r"\\10.10.30.14\d\图像\APY181130001_314178张18种手势识别数据\完整数据包_processed\data\gesture08_Single-hand-heart",
            r"\\10.10.30.14\d\图像\APY181130001_314178张18种手势识别数据\完整数据包_processed\data\gesture09_OK",
            r"\\10.10.30.14\d\图像\APY181130001_314178张18种手势识别数据\完整数据包_processed\data\gesture10_Like",
            r"\\10.10.30.14\d\图像\APY181130001_314178张18种手势识别数据\完整数据包_processed\data\gesture12_Make-a-fist",
            r"\\10.10.30.14\d\图像\APY181130001_314178张18种手势识别数据\完整数据包_processed\data\gesture13_ROCK",
            r"\\10.10.30.14\d\图像\APY181130001_314178张18种手势识别数据\完整数据包_processed\data\gesture14_LOVE",
            r"\\10.10.30.14\d\图像\APY181130001_314178张18种手势识别数据\完整数据包_processed\data\gesture15_Two-hand-heart",
            r"\\10.10.30.14\d\图像\APY181130001_314178张18种手势识别数据\完整数据包_processed\data\gesture16_Put-palms-together",
            r"\\10.10.30.14\d\图像\APY181130001_314178张18种手势识别数据\完整数据包_processed\data\gesture17_Give-new-year's-greeting",
        ]

        for gesture in project_folders:
            res = defaultdict(list)
            for file in os.listdir(gesture):
                if file.endswith('.json'):
                    file_path = os.path.join(gesture, file)
                    with open(file_path, 'r', encoding='utf8')as f:
                        content = json.load(f)
                        sex = content.get("WorkLoad", {}).get("Sex")
                        res[sex].append(file_path)
            extact_num = 1154
            male_list, female_list = res["male"], res["female"]
            seample_male, seample_female = random.sample(male_list, extact_num), random.sample(female_list, extact_num)
            to_copy(seample_male, gesture)
            to_copy(seample_female, gesture)

    @dingding_monitor
    def extract_13(self):
        """
        提取刘达中移数据
        :return:
        """
        old_data = [
            r"\\10.10.30.14\刘晓东\数据提取\刘达\央研人脸数据挑选\100张人脸数据",
            r"\\10.10.30.14\刘晓东\数据提取\刘达\央研人脸数据挑选\900张人脸数据"
        ]
        face_data = r"\\10.10.30.14\刘晓东\数据提取\刘达\央研人脸数据挑选\data"

        finger_print = set()
        # 将老数据生成指纹库
        for old_folder in old_data:
            for old_img in os.listdir(old_folder):
                old_img_path = os.path.join(old_folder, old_img)
                finger = get_md5_value(old_img_path)
                finger_print.add(finger)

        age_limit = {
            "0": 440,
            "1": 524,
            "2": 686,
            "3": 646,
            "4": 691,
            "5": 480,
            "6": 300,
            "7": 234,
        }
        age_sum = defaultdict(int)
        dest_folder = r"\\10.10.30.14\刘晓东\数据提取\刘达\央研人脸数据挑选\人脸图像\data"
        for file in os.listdir(face_data):
            if file.endswith(".jpg"):
                file_path = os.path.join(face_data, file)
                file_finger = get_md5_value(file_path)
                if file_finger not in finger_print:
                    age = int(file.split(".")[0].split("_")[-1])
                    divisor = age // 10
                    if divisor < 8:
                        age_sum[str(divisor)] += 1
                        age_remin_num = age_limit[str(divisor)]
                        if age_remin_num > 0:
                            age_limit[str(divisor)] -= 1
                            shutil.copy(file_path, dest_folder)
        print(age_sum)
        print(age_limit)

    def extract_14(self):
        """
        数据重名
        :return:
        """
        age_sum = defaultdict(int)
        folder = r"\\10.10.30.14\刘晓东\数据提取\刘达\央研人脸数据挑选\人脸图像\data"
        for file in os.listdir(folder):
            if file.endswith('.jpg'):
                age = int(file.split(".")[0].split("-")[1])
                divisor = age // 10
                age_sum[str(divisor)] += 1
        print(age_sum)

    def extract_15(self):
        """

        :return:
        """
        i = 0
        folder = r"\\10.10.30.14\图像\APY180921001_70,846张人脸抠图数据\完整数据包_processed\data\category_1"
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith(".jpg"):
                    i += 1
        print(i)

    @dingding_monitor
    def extract_16(self):
        """

        :return:
        """
        folder = r"\\10.10.8.123\姜平2\5-口罩人脸采集\6-交付数据\Asian"
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file == "normal.jpg":
                    file_path = os.path.join(root, file)
                    size = os.path.getsize(file_path)
                    if size > 2000000:
                        print(file_path)

    def extract_17(self):
        """
        提取第二次数据
        :return:
        """
        total_data = r"\\10.10.30.14\刘晓东\数据提取\沈杰\201人婴幼儿啼哭语音数据\data"
        first_data = r"\\10.10.30.14\刘晓东\数据提取\沈杰\201人婴幼儿啼哭语音数据\data_first"
        dest_data = r"\\10.10.30.14\刘晓东\数据提取\沈杰\201人婴幼儿啼哭语音数据\data_second\category"
        fingerprint_set = set()

        for root, dirs, files in os.walk(first_data):
            for dir in dirs:
                fingerprint_set.add(dir)

        for root, dirs, files in os.walk(total_data):
            for dir in dirs:
                if dir not in fingerprint_set:
                    dir_path = os.path.join(root, dir)
                    dest_path = os.path.join(dest_data, dir)
                    shutil.copytree(dir_path, dest_path)

    def extract_18(self):
        """
        提取数据
        :return:
        """
        old_data = r"\\10.10.8.123\刘晓东2\提取数据\陈丽芳\106关键点黄种人\data"

        finger_print = set()
        # 将老数据生成指纹库
        for root, dirs, files in os.walk(old_data):
            for file in files:
                if file.endswith("jpg") or file.endswith("png"):
                    finger_print.add(file)

        new_data_paths = [
            r"\\10.10.30.14\d\图像\APY180930004_87,877张人脸106关键点标注数据（复杂场景）\完整数据包\data\session02",
            r"\\10.10.30.14\d\图像\APY180930004_87,877张人脸106关键点标注数据（复杂场景）\完整数据包\data\session04_yellow"
        ]
        for new_data_path in new_data_paths:
            with open("path.txt", 'a', encoding='utf8')as p_f:
                for root, dirs, files in os.walk(new_data_path):
                    for file in files:
                        if file.endswith("jpg") or file.endswith("png"):
                            img_path = os.path.join(root, file)
                            json_path = img_path.replace("jpg", "json").replace("png", "json")
                            with open(json_path, 'r', encoding='utf8')as f:
                                content = json.load(f)
                                race = content.get("WorkLoad").get("race")
                                if race == "Yellow":
                                    if file not in finger_print:
                                        print(img_path)
                                        p_f.write(img_path + "\n")

    def ticket_ocr(self):
        """
        抽取票据ocr图像
        :return:
        """
        ticket_list = [
            r"\\10.10.30.14\d\图像\APY190730002_4,601张22种票据OCR数据\完整数据包\data\VAT-invoice"
        ]
        for tickets in ticket_list:
            sum = 250
            src = r"\\10.10.30.14\d\图像\APY190730002_4,601张22种票据OCR数据\完整数据包\data"
            dest = r"\\10.10.30.14\刘晓东\数据提取\彭颖岚\云从——0928\四种票据ocr\data"
            dest_folder = tickets.replace(src, dest)
            for root, dirs, files in os.walk(tickets):
                for file in files:
                    if file.endswith('.json'):
                        json_path = os.path.join(root, file)
                        img_path = json_path.replace(".json", ".jpg")
                        demo_path = json_path.replace(".json", "_demo.jpg")
                        if sum > 0:
                            new_json_file = os.path.join(dest_folder, str(sum).zfill(5) + ".json")
                            new_img_path = new_json_file.replace(".json", ".jpg")
                            new_demo_path = new_json_file.replace(".json", "_demo.jpg")
                            shutil.copy(json_path, new_json_file)
                            shutil.copy(img_path, new_img_path)
                            shutil.copy(demo_path, new_demo_path)
                            sum -= 1

    @dingding_monitor
    def extract_19(self):
        """
        提取数字串
        :return:
        """
        file_path = r"\\10.10.30.14\刘晓东\数据提取\周彦\中国儿童普通话纯数字\中国儿童语音数字1.txt"

        src_folder_str = r"\\10.10.8.123\3000小时中国儿童语音项目\导出数据-肖旸\0428"
        dest_folder_str = r"\\10.10.30.14\刘晓东\数据提取\周彦\中国儿童普通话纯数字"
        with open(file_path, 'r', encoding='utf8')as index_f:
            for line in index_f:
                line_content = line.strip()
                ori_path = line_content.split()
                real_txt_file = ori_path[0].replace(r"U:\郎倩华", r"\\10.10.8.123")  # 索引文件

                real_txt_folder = re.sub(r"\\session.*", "", real_txt_file)  # 获取到所在的人
                sub_folders = [os.path.join(real_txt_folder, sub_f) for sub_f in os.listdir(real_txt_folder)]  # 人的不同设备

                # 获取索引文件名在不同设备中的文件
                txt_file_name = os.path.split(real_txt_file)[1].split("_")[-1]
                for sub_folder in sub_folders:
                    for file_name in os.listdir(sub_folder):
                        if txt_file_name in file_name:
                            src_path = os.path.join(sub_folder, file_name)
                            src_meta = src_path.replace(".txt", ".metadata")
                            src_wav = src_path.replace(".txt", ".wav")
                            dest_path = src_path.replace(src_folder_str, dest_folder_str)
                            dest_meta = dest_path.replace(".txt", ".metadata")
                            dest_wav = dest_path.replace(".txt", ".wav")

                            dest_folder = os.path.split(dest_path)[0]
                            if not os.path.exists(dest_folder):
                                os.makedirs(dest_folder)

                            shutil.copy(src_path, dest_path)
                            shutil.copy(src_meta, dest_meta)
                            shutil.copy(src_wav, dest_wav)


if __name__ == '__main__':
    ed = ExtractData()
    ed.extract_19()
