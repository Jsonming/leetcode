#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import random
import re
import shutil
import zipfile
import json
import requests
from lxml import etree
from requests import Session
import csv

from workscript.dingding.dingding_decorator import dingding_monitor


class RandomExtractWav(object):
    """
    从damp  download样例 在样例中抽取数据放到服务器抽取文件上
    """

    def __init__(self):
        self.EXTRACT_NUM = 50

    def download_sample_one(self, project_temp_folder, url):
        """
        根据项目下载项目的样例
        :param url: 项目链接
        :return:
        """
        session = Session()
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Connection": "keep-alive",
            "Cookie": "Hm_lvt_c11a8399d964da0bb1f13ee5438d021d=1574392765,1574418656; JSESSIONID=CC49527B4BD246BA657339CD9FE2FF24",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        }
        response = session.get(url, headers=headers)
        html = etree.HTML(response.text)
        oss_url_list = html.xpath('//*[@id="cc1"]/div[1]/div[26]/div[2]/a/@href')
        if not oss_url_list:
            raise Exception("项目国内链接为空")
        else:
            oss_url = oss_url_list[0]
            sample_name = oss_url.split("?")[0].split("/")[-1]
            sample_name = os.path.join(project_temp_folder, sample_name)
            oss_content = requests.get(oss_url).content
            with open(sample_name, 'wb')as f:
                f.write(oss_content)
            return sample_name

    def download_sample(self, project_temp_folder, url):
        """
        根据项目下载项目的样例
        :param url: 项目链接
        :return:
        """
        # session = Session()
        # headers = {
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        #     "Connection": "keep-alive",
        #     "Cookie": "Hm_lvt_c11a8399d964da0bb1f13ee5438d021d=1574392765,1574418656; JSESSIONID=20976AD6AC4743D12A6BA1513427FA18",
        #     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        # }
        # response = session.get(url, headers=headers)
        # html = etree.HTML(response.text)
        # oss_url_list = html.xpath('//*[@id="cc1"]/div[1]/div[26]/div[2]/a/@href')
        # if not oss_url_list:
        #     raise Exception("项目国内链接为空")
        # else:
        #     oss_url = oss_url_list[0]
        #     sample_name = oss_url.split("?")[0].split("/")[-1]
        #     sample_name = os.path.join(project_temp_folder, sample_name)
        #     oss_content = requests.get(oss_url).content
        #     with open(sample_name, 'wb')as f:
        #         f.write(oss_content)
        #     return sample_name

        sample_name = url.split("?")[0].split("/")[-1]
        sample_name = os.path.join(project_temp_folder, sample_name)
        oss_content = requests.get(url).content
        with open(sample_name, 'wb')as f:
            f.write(oss_content)
        return sample_name

    def unzip_sample(self, sample_file):
        """
        解压样例返回文件夹
        :return:
        """
        if not os.path.exists(sample_file):
            raise Exception("文件不存在")
        sample_folder = os.path.splitext(sample_file)[0]
        with zipfile.ZipFile(sample_file) as zip_file:
            for f in zip_file.namelist():
                zip_file.extract(f, sample_folder)
        if not os.listdir(sample_folder):
            raise Exception("解压出来文件夹为空")
        else:
            return sample_folder

    def extract_data_rename(self, sample_folder, dest_dir):
        """
        同样抽取数据，但是这个是重命名抽取数据
        :param sample_folder:
        :param dest_dir:
        :return:
        """
        all_list = []
        for root, dirs, files in os.walk(sample_folder):
            for file in files:
                if file.endswith('wav'):
                    wav_path = os.path.join(root, file)
                    all_list.append(wav_path)
        i = 1
        need = random.sample(all_list, self.EXTRACT_NUM)
        for wav_path in need:
            txt_path = wav_path.replace('.wav', '.txt')
            meta_path = wav_path.replace('.wav', '.metadata')

            wav_dest = dest_dir + '\\' + str(i).zfill(5) + ".wav"
            txt_dest = wav_dest.replace('.wav', '.txt')
            meta_dest = wav_dest.replace('.wav', '.metadata')

            shutil.copy(wav_path, wav_dest)
            shutil.copy(txt_path, txt_dest)
            shutil.copy(meta_path, meta_dest)

            i += 1

    def extract_data(self, sample_folder, dest_dir):
        """
        随机抽取数据
        :return:
        """

        file_finger = set()
        for root, dirs, files in os.walk(dest_dir):
            for file in files:
                if file.endswith('wav'):
                    file_finger.add(file)

        all_list = []
        for root, dirs, files in os.walk(sample_folder):
            for file in files:
                if file.endswith('wav'):
                    if file not in file_finger:
                        wav_path = os.path.join(root, file)
                        all_list.append(wav_path)

        need = random.sample(all_list, self.EXTRACT_NUM)
        for wav_path in need:
            self.to_copy(wav_path, sample_folder, dest_dir)

    def to_copy(self, wav_path, work_dir, dest_dir):
        """
        拷贝文件
        :param wav_path:
        :param work_dir:
        :param dest_dir:
        :return:
        """
        name = wav_path.split('\\')[-1]
        wav_dest = dest_dir + '\\' + name

        txt_path = wav_path.replace('.wav', '.txt')
        meta_path = wav_path.replace('.wav', '.metadata')

        txt_dest = wav_dest.replace('.wav', '.txt')
        meta_dest = wav_dest.replace('.wav', '.metadata')

        shutil.copy(wav_path, wav_dest)
        shutil.copy(txt_path, txt_dest)
        shutil.copy(meta_path, meta_dest)

    def run(self, project_url, dest_dir):
        """
        主逻辑控制
        :return:
        """
        project_temp_folder = r"E:\提取"
        sample_file = self.download_sample(project_temp_folder, project_url)
        print("提取到样例文件:{}".format(sample_file))
        sample_folder = self.unzip_sample(sample_file)
        print("解压出文件夹:{}".format(sample_folder))

        print("开始提取文件")
        self.extract_data(sample_folder, dest_dir)
        print("提取完成")
        os.remove(sample_file)
        print("删除样例文件")
        shutil.rmtree(sample_folder)
        print("删除样例文件夹")

    def run_2(self, project_url, dest_dir):
        project_temp_folder = r"E:\提取"
        sample_file = self.download_sample_one(project_temp_folder, project_url)
        print("提取到样例文件:{}".format(sample_file))
        sample_folder = self.unzip_sample(sample_file)
        print("解压出文件夹:{}".format(sample_folder))

        print("开始提取文件")
        self.extract_data(sample_folder, dest_dir)
        print("提取完成")
        shutil.rmtree(sample_folder)
        print("删除样例文件夹")

    @dingding_monitor
    def run_3(self, sample_folder, dest_dir):
        print("开始提取文件")
        # self.extract_data(sample_folder, dest_dir)
        self.extract_data_rename(sample_folder, dest_dir)
        print("提取完成")

    @dingding_monitor
    def run_4(self, src_dir, dest_dir):
        """
        抽取图片
        :return:
        """
        all_list = []
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                if file.endswith("g"):
                    jpg_path = os.path.join(root, file)
                    if len(all_list) < 20000:
                        all_list.append(jpg_path)
                    else:
                        break

        need = random.sample(all_list, 200)
        for i, img_path in enumerate(need):
            order_id = re.findall("(\d+)、", dest_dir)[0]
            name, suf = os.path.splitext(img_path)
            dest_img_file = "KWTK-{}-{}{}".format(order_id, str(i + 1).zfill(3), suf)
            dest_img_path = os.path.join(dest_dir, dest_img_file)
            shutil.copy(img_path, dest_img_path)

    @dingding_monitor
    def run_5(self, src_dir, dest_dir):
        """

        :return:
        """
        all_list = []
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                if file.endswith(".MOV"):
                    jpg_path = os.path.join(root, file)
                    if len(all_list) < 5000:
                        all_list.append(jpg_path)
                    else:
                        break

        need = random.sample(all_list, 50)
        for i, img_path in enumerate(need):
            order_id = re.findall("(\d+)、", dest_dir)[0]
            dest_img_file = "KWTK-{}-{}.MOV".format(order_id, str(i + 1).zfill(3))
            dest_img_path = os.path.join(dest_dir, dest_img_file)
            shutil.copy(img_path, dest_img_path)

    @dingding_monitor
    def run_6(self, src_dir, dest_dir):
        """

        :param src_dir:
        :param dest_dir:
        :return:
        """
        all_list = []
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                if file.endswith("wav"):
                    jpg_path = os.path.join(root, file)
                    if len(all_list) < 20000:
                        all_list.append(jpg_path)
                    else:
                        break

        # for root, dirs, files in os.walk(src_dir):
        #     for file in files:
        #         if file.endswith("metadata"):
        #             meta_path = os.path.join(root, file)
        #             with open(meta_path, 'r', encoding='utf8')as f:
        #                 content = f.read()
        #                 age = re.findall(r"AGE\s+(\d+)", content)[0]
        #                 if int(age) < 18:
        #                     jpg_path = meta_path.replace(".metadata", ".wav")
        #                     if len(all_list) < 20000:
        #                         all_list.append(jpg_path)
        #                     else:
        #                         break

        need = random.sample(all_list, 500)
        for i, img_path in enumerate(need):
            order_id = re.findall("(\d+)、", dest_dir)[0]
            dest_img_file = "KWTK-{}-{}.wav".format(order_id, str(i + 1).zfill(3))
            dest_img_path = os.path.join(dest_dir, dest_img_file)
            shutil.copy(img_path, dest_img_path)

    def run_7(self, dest_dir):
        """
        提取标注数据
        :return:
        """
        contents = [["content"]]
        with open("tem.txt", 'r', encoding='utf8')as f:
            for line in f:
                content = json.loads(line.strip())
                text = content.get("短信")
                print(text)
                contents.append([text])

        order_id = re.findall("(\d+)、", dest_dir)[0]
        dest_img_file = "KWTK-{}-1.csv".format(order_id)
        dest_img_path = os.path.join(dest_dir, dest_img_file)
        with open(dest_img_path, 'w', encoding='gbk', newline="")as c_f:
            f_csv = csv.writer(c_f)
            f_csv.writerows(contents)

    def run_8(self):
        """

        :return:
        """
        docment = ""
        with open("tem.txt", 'r', encoding='utf8')as f:
            for line in f:
                line_content = line.strip()
                if line_content != "</Event>":
                    docment += line
                else:
                    text = re.findall("<Original>(.*?)</Original>", docment, re.S)[0]
                    with open('a.txt', 'a', encoding='utf8')as f:
                        f.write(text.replace("\n", "") + "\n")
                    docment = ""


if __name__ == '__main__':
    rew = RandomExtractWav()
    # with open('id_info.txt', 'r', encoding='utf8')as f:
    #     content = f.readlines()
    #     for item in content[:4]:
    #         order_id, folder_name, product_name, url, name = item.strip().split()
    #         print("_"*100)
    #         print(order_id, folder_name)
    #         dest_dir = r'\\10.10.8.123\刘晓东\liuxd_share\实验数据\200个课外\{}、{}\data'.format(order_id, folder_name)
    #         project_url = url
    #         rew.run(project_url, dest_dir)
    #
    # sample_url = r"http://damp.datatang.com/product/detail?productid=234"
    # dest_dir = r"\\10.10.8.123\刘晓东\liuxd_share\实验数据\200个课外\43、噪音环境下普通话语音标注\data"
    # rew.run_2(sample_url, dest_dir)

    # sample_folder = r"\\10.10.30.14\d\语音\语音数据_2016\APY161101006_754人外国人说汉语手机采集语音数据\完整数据包_加密后数据\data\category"
    # dest_dir = r"\\10.10.8.123\刘晓东\liuxd_share\实验数据\200个课外\84、外国人说汉语语音标注\data"
    # rew.run_3(sample_folder, dest_dir)

    # dest_dir = r"\\10.10.8.123\刘晓东\liuxd_share\实验数据\200个课外\198、中国儿童说英语语音标注\data"
    # src_dir = r"\\10.10.30.14\jxw\APY190422001_203小时中国儿童说英语手机采集语音数据\完整数据包\data\category"
    # rew.run_6(src_dir, dest_dir)

    # dest_dir = r"\\10.10.8.123\刘晓东\liuxd_share\实验数据\200个课外\199、有声读物文本拼音标注\data"
    # src_dir = r"\\10.10.30.14\l\自有数据\语音数据\已入库_5\APY170801047_35小时有声读物文本拼音标注语音数据\完整数据包\data\category"
    # rew.run_6(src_dir, dest_dir)