#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/24 16:25
# @Author  : yangmingming
# @Site    : 
# @File    : process_image.py
# @Software: PyCharm
import json
import os
import shutil
from collections import defaultdict
import re
import math
from PIL import Image
from workscript.process_img.img_md5_remove import get_md5_value


class ProcessImage(object):
    def __init__(self):
        pass

    def fixed_json(self):
        """
        修改json文件添加适当格式
        :param pro:
        :return:
        """
        project_path = r"\\10.10.30.14\apy190531001_50023张人体服饰分割数据\完整数据包\data - 副本"
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r+', encoding='utf8') as f:
                        content = json.loads(f.read())
                        new_content = json.dumps(content, ensure_ascii=False, indent=4)
                        f.seek(0)
                        f.truncate()
                        f.write(new_content)

    def temp_fixed_data(self):
        """
        非功能性修改文件，单次临时修改，修改文件名称
        :return:
        """
        with open("e_etext_num.txt", "a", encoding='utf8')as e_f, open("include.txt", "a", encoding='utf8')as i_f:
            project_path = r"\\10.10.30.14\图像数据2\图像数据2017\APY170301415_1_53万张街景图片_2.6万张道路线精细标注数据\完整数据包_加密后数据 - 新\data\category\G0001"
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    if file.endswith(".json"):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r+', encoding='utf8') as f:
                            content = json.loads(f.read())
                            datalist = content.get("datalist")
                            for item in datalist:
                                e_text = item.get("e_etext_num")
                                include = item.get("include")
                                e_f.write("{}\t{}\n".format(file_path, e_text))
                                i_f.write("{}\t{}\n".format(file_path, include))

    def rebuild_data(self):
        """
        重构json 数据
        :return:
        """
        tag_type = {"1": "Road indication signs", "2": "Speed limit signs", "3": "Roadways"}
        sub_type = {
            "1_1": "Driving straight", "1_2": "Turning right", "1_3": "Turning left", "1_4": "U-turn",
            "1_5": "Driving straight or turning right", "1_6": "Driving straight or turning left",
            "1_7": "U-turn & going straight", "1_8": "Others",
            "2_1": "Speed limit signs",
            "3_1": "Solid roadways lines", "3_2": "Dotted roadways lines", "3_3": "Pedestrian crossing lines",
            "3_4": "Parking lines", "3_5": "Others",
        }

        project_path = r"\\10.10.30.14\图像数据2\图像数据2017\APY170301415_1_53万张街景图片_2.6万张道路线精细标注数据\完整数据包_加密后数据 - 新\data\category\G0001"
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r+', encoding='utf8') as f:
                        content = json.loads(f.read())
                        datalist = content.get("datalist")
                        for item in datalist:
                            item["object_type"] = item.get("object_type").replace("Roadways", "road lines")
                            item["category"] = item.get("category").replace("U-turn & going straight",
                                                                            "U-turn or going straight")
                        f.seek(0)
                        f.truncate()
                        f.write(json.dumps(content, ensure_ascii=False, indent=4))

    def count_data(self):
        """
        统计数据量
        :return:
        """
        object_res = defaultdict(int)
        year_res = defaultdict(int)
        category_res = defaultdict(int)
        speed_limit_res = defaultdict(int)
        project_path = r"\\10.10.30.14\图像数据2\图像数据2017\APY170301415_1_53万张街景图片_2.6万张道路线精细标注数据\完整数据包_加密后数据 - 新\data\category\G0001"
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith(".json"):
                    # year = re.findall(r"201[34567]", file)[0]
                    # year_res[year] += 1
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r+', encoding='utf8') as f:
                        content = json.loads(f.read())
                        data_list = content.get("datalist")
                        for item in data_list:
                            object_type = item.get("object_type")
                            object_res[object_type] += 1

                            if object_type == "Road indication signs":
                                category = item.get("category")
                                category_res[category] += 1
                            elif object_type == "Roadways":
                                category = item.get("category")
                                if category == "Others":
                                    category_res["Others_"] += 1
                                else:
                                    category_res[category] += 1
                            else:
                                speed_limit = item.get("speed_limit_number")
                                speed_limit_res[speed_limit] += 1
        print(object_res)
        print(year_res)
        print(category_res)
        print(speed_limit_res)

    def fixed_format(self):
        """
        修改数据格式
        :return:
        """

        def sub_field(field):
            field = field.replace("Fear", "Scared")
            field = field.replace("Surprise", "Surprised")
            field = field.replace("Others", "Other")

            field = field.replace("Depression", "Depressed")
            field = field.replace("Envy", "Envies")
            field = field.replace("Dishonesty", "Dishonest")
            field = field.replace("Cowardice", "Coward")
            field = field.replace("Acceptance", "Approved")
            field = field.replace("Blame", "Blamed")
            return field

        project_path = r"\\10.10.30.14\apy190218001_1003人情感视频数据\完整数据包\data"
        with open('em.txt', 'a', encoding='utf8')as e_f:
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    if file.endswith("json"):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r+', encoding='utf8') as f:
                            content = json.load(f)
                            for item in content:
                                inner_emotion = item.get("inner emotion")
                                inner_emotion = [sub_field(i_e) for i_e in inner_emotion]
                                item["inner emotion"] = inner_emotion
                                facial_emotion = item.get("facial emotion")
                                facial_emotion = [sub_field(f_e) for f_e in facial_emotion]
                                item["facial emotion"] = facial_emotion
                            f.seek(0)
                            f.truncate()
                            f.write(json.dumps(content, ensure_ascii=False, indent=4))

    def fixed_data(self):
        """修改数据"""

        project_path = r"\\10.10.30.14\图像数据2\图像数据2017\APY170301450_7万张英文场景文字标注数据\完整数据包\data\category\G0001\session01"
        with open("info.txt", 'a', encoding='utf8')as info_f:
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file.endswith("json"):
                        with open(file_path, 'r+', encoding='utf8')as f:
                            content = json.loads(f.read())
                            info_f.write("{}\t{}\n".format(file_path, json.dumps(content, ensure_ascii=False)))

    def extract_img(self):
        """
        提取交通图片
        :return:
        """
        project_path = r"\\10.10.30.14\图像数据2\图像数据2017\APY170301415_0_53万张街景图片_53万张标框数据\完整数据包\data"

        with open('detail.txt', 'a', encoding='utf8')as d_f:
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    if file.endswith("jpg") or file.endswith("png"):
                        file_name, suffix = os.path.splitext(file)
                        img_path = os.path.join(root, file)
                        img = Image.open(img_path)
                        json_path = os.path.join(root, file_name + ".json")

                        with open(json_path, 'r', encoding='utf8')as f:
                            content = json.load(f)
                            indication = content.get("Workload", {}).get("Indication signs")
                            prohibitory = content.get("Workload", {}).get("Prohibitory signs")
                            if indication or prohibitory:
                                for box in content.get("boxs"):
                                    object_type = box.get("Object_type")
                                    category = box.get("Category")
                                    if object_type == "Indication signs" or object_type == "Prohibitory signs":
                                        base_path = r"\\10.10.30.14\图像数据2\图像数据2017\APY170301415_0_53万张街景图片_53万张标框数据\新抽取"
                                        dir_path = os.path.join(os.path.join(base_path, object_type), category)
                                        if not os.path.exists(dir_path):
                                            os.makedirs(dir_path)
                                        x, y, w, h = box["x"], box["y"], box["w"], box["h"]
                                        box_id = box["id"]
                                        base_img_name = img_path.replace(
                                            r"\\10.10.30.14\图像数据2\图像数据2017\APY170301415_0_53万张街景图片_53万张标框数据\完整数据包",
                                            "").lstrip("\\").replace("\\", "_")
                                        name, suf = os.path.splitext(base_img_name)
                                        img_name = "{}_{}".format(name, box_id) + suf
                                        new_img_path = os.path.join(dir_path, img_name)
                                        print(new_img_path)
                                        region = img.crop((x, y, x + w, y + h))
                                        region.save(new_img_path)
                                        d_f.write("{}\t{}\n".format(new_img_path, img_path))

    def check_data(self):
        """
        检查数据
        :return:
        """
        project_paths = [
            r"\\10.10.30.14\图像数据2\图像数据2017\APY170301450_7万张英文场景文字标注数据\完整数据包\data\category\G0001\session01",
        ]

        md5_set, person_id_set = dict(), dict()
        for root, dirs, files in os.walk(project_paths[0]):
            for file in files:
                if file.endswith("jpg"):
                    camera_sample_path = os.path.join(root, file)
                    md5_value = get_md5_value(camera_sample_path)
                    if md5_value not in md5_set:
                        md5_set[md5_value] = camera_sample_path
                    else:
                        print(camera_sample_path)
                        # new_img_path = camera_sample_path.replace("session01", "重复")
                        # shutil.move(camera_sample_path, new_img_path)
                        #
                        # json_path = camera_sample_path.replace(".jpg", ".json")
                        # new_json_path = camera_sample_path.replace("session01", "重复").replace(".jpg", ".json")
                        # shutil.move(json_path, new_json_path)
                        #
                        # meta_path = camera_sample_path.replace(".jpg", ".metadata")
                        # new_meta_path = camera_sample_path.replace("session01", "重复").replace(".jpg", ".metadata")
                        # shutil.move(meta_path, new_meta_path)

    def recover(self):
        """
        数据找回主要为了找回年龄字段
        :return:
        """
        name_map = dict()
        project_path = r"\\10.10.30.14\apy191016001_423人34748张3d人体实例分割及人体22关键点&2d手势识别采集标注数据\完整数据包\data\Human-body-instance-segmentation&22-points-landmark"
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith("color.json"):
                    file_path = os.path.join(root, file)
                    name_map[file] = file_path

        project_path = r"\\10.10.30.14\apy191016001_423人34748张3d人体实例分割及人体22关键点&2d手势识别采集标注数据\完整数据包 - 副本\data"
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith("color.json"):
                    file_path = os.path.join(root, file)
                    o_file_path = name_map[file]
                    age_info = o_file_path.split("\\")[-5].split("-")[-1]
                    with open(file_path, 'r+', encoding='utf8')as f:
                        content = json.load(f)
                        data_list = content.get("DataList")
                        for item in data_list:
                            item["age"] = age_info
                        f.seek(0)
                        f.truncate()
                        f.write(json.dumps(content, ensure_ascii=False, indent=4))

    def rects_polygons(self, marks):
        """
        统计marks里边的矩形和多变形的
        :param marks:
        :return:
        """

        rect_num, polygon_num = 0, 0
        for mark in marks:
            coordinates = mark.get("coordinates")
            rect_flag = is_rect(coordinates)
            if rect_flag:
                rect_num += 1
            else:
                polygon_num += 1
        return rect_num, polygon_num

    def distiguish_word(self, mark_list):
        """
        区分不同的字
        :param ws:
        :return:
        """
        pass

    def run(self):
        def text_mark_map(marks):
            t_m_map = defaultdict(list)
            for mark in marks:
                t_m_map[mark["text"]].append(mark)
            return t_m_map

        with open('6_info.txt', 'r', encoding='utf8')as f, open('7_info.txt', 'a', encoding='utf8')as n_f:
            for line in f:
                file_path, content = line.strip().split("\t")
                content = json.loads(content)
                mark_res = content.get("markResult")
                text_mark_res = text_mark_map(mark_res)

                for mark in mark_res:
                    text = mark.get("text")
                    text_type = mark.get("text type")
                    if len(text) == 1:
                        mark_list = text_mark_res[text]
                        if len(mark_list) == 1:
                            if text_type != "char":
                                mark["text type"] = "char"
                        else:
                            words = defaultdict(list)
                            for mark_info in mark_list:
                                coordinates = mark_info.get("coordinates")
                                center = comput_center(coordinates)
                                words[center].append(mark_info)

                            for word, mark_i in words.items():
                                if len(mark_i) == 1:
                                    if mark_i[0]["text type"] != "char":
                                        mark_i[0]["text type"] = "char"
                n_f.write("{}\t{}\n".format(file_path, json.dumps(content, ensure_ascii=False)))

    def temp(self):
        """
        将处理的结果回写到文件
        :return:
        """
        with open('7_info.txt', 'r', encoding='utf8')as f:
            for line in f:
                file_path, content = line.strip().split("\t")
                content = json.loads(content)
                with open(file_path, 'w', encoding='utf8')as r_f:
                    r_f.write(json.dumps(content, ensure_ascii=False, indent=4))


def comput_center(coor):
    """
    计算字的中心
    :param coor:
    :return:
    """
    x = (coor[0][0] + coor[2][0]) / 2
    y = (coor[0][1] + coor[2][1]) / 2
    return (x, y)


def is_rect(coor):
    """
    判断是否是矩形
    :param mark:
    :return:
    """
    flag = True
    if coor[0][0] != coor[1][0]:
        flag = False
    elif coor[1][1] != coor[2][1]:
        flag = False
    elif coor[2][0] != coor[3][0]:
        flag = False
    elif coor[3][1] != coor[0][1]:
        flag = False
    return flag


if __name__ == '__main__':
    psi = ProcessImage()
    # psi.temp_fixed_data()
    # psi.rebuild_data()
    # psi.count_data()
    # psi.fixed_format()
    # psi.fixed_data()
    # psi.extract_img()
    # psi.check_data()
    # psi.recover()
    # psi.run()
    psi.temp()
