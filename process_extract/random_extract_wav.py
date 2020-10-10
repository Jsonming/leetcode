#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import random
import shutil
import zipfile
import requests
from requests import Session
from lxml import etree


class RandomExtractWav(object):
    """
    从damp  download样例 在样例中抽取数据放到服务器抽取文件上
    """

    def __init__(self):
        self.EXTRACT_NUM = 260

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

    def extract_data(self, sample_folder, dest_dir):
        """
        随机抽取数据
        :return:
        """
        all_list = []
        for root, dirs, files in os.walk(sample_folder):
            for file in files:
                if file.endswith('wav'):
                    wav_path = os.path.join(root, file)
                    all_list.append(wav_path)
        if len(all_list) < self.EXTRACT_NUM:
            need = all_list
        else:
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

    def run_3(self, sample_folder, dest_dir):
        print("开始提取文件")
        self.extract_data(sample_folder, dest_dir)
        print("提取完成")


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

    sample_folder = r"\\10.10.30.14\d\语音\语音数据_2016\APY161101013_1505小时普通话手机采集语音数据\完整数据包_加密后数据\data\category1"
    dest_dir = r"\\10.10.8.123\刘晓东\liuxd_share\实验数据\200个课外\80、普通话朗读语音标注\data"
    rew.run_3(sample_folder, dest_dir)