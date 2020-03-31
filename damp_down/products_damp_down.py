#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/30 17:07
# @Author  : yangmingming
# @Site    : 
# @File    : products_damp_down.py
# @Software: PyCharm
import os
import json
import requests
from urllib import parse


class ProductsDampDown(object):
    def __init__(self):
        pass

    def create_folder(self, folder_name):
        """
        创建一个products 文件夹，作为主文件夹，各个产品说明书在它的子文件夹
        :return:
        """
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        else:
            pass

    def crawl_product_info(self, page_num):
        """
        抓取damp信息
        :return:
        """
        url = "http://damp.datatang.com/fullSearch/searchProduct"
        headers = {
            'cache-control': "no-cache",
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
            "Cookie": "Hm_lvt_c11a8399d964da0bb1f13ee5438d021d=1574392765,1574418656; account=liuxiaodong; password=1306934; JSESSIONID=C277601A24AB0F0D68DA484BAD1C0FAE",
        }
        data = {
            "onlineFlag": 1,
            "currentPage": page_num,
            "pageSize": 20
        }
        response = requests.request("POST", url, data=data, headers=headers)
        return response.text

    def crawl_enclosure(self, path, base_url):
        """
        抓取附件的内容
        :return:
        """
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
        }
        e_response = requests.get(url=base_url)
        e_name = parse.unquote(e_response.url).split("?")[0].split('/')[-1]
        e_content = e_response.content
        self.create_folder(path)
        file_name = os.path.join(path, e_name)
        with open(file_name, 'wb', )as f:
            f.write(e_content)
        return e_name

    def save_product_info(self, info: list):
        """
        保存产品信息
        :param info:
        :return:
        """
        new_info = [item if item else " " for item in info]
        with open("product.txt", 'a', encoding='utf8') as f:
            f.write("\t".join(new_info) + "\n")

    def run(self):
        """
        主逻辑控制
        :param products_file: 产品execl 表格
        :return:bj_data
        """
        # 创建文件夹
        folder_name = os.path.join(os.getcwd(), "products")
        self.create_folder(folder_name)

        # 抓取信息
        for i in range(1, 17):
            product_info = self.crawl_product_info(page_num=i)
            product_dict = json.loads(product_info)
            info_rows = product_dict.get("rows")
            for row in info_rows:
                class_name = row.get("classname1", '')  # 类别
                enossreturnurl = row.get("enossreturnurl", '')  # 英文说明书
                productname = row.get("productname", '')  # 产品名称
                samplestoreloc = row.get("samplestoreloc", '')  # 样例
                demourl = row.get("demourl", '')  # demo
                ossreturnurl = row.get("ossreturnurl", '')  # 中文说明书

                # 保存产品名称，说明书（中英文），样例，demo链接到文件中
                self.save_product_info(info=[productname, ossreturnurl, enossreturnurl, samplestoreloc, demourl])

                # down图像视频产品
                if class_name == "图像视频":
                    file_path = os.path.join(folder_name, productname)
                    for file_url in [samplestoreloc, demourl, ossreturnurl, enossreturnurl]:
                        if file_url:
                            self.crawl_enclosure(file_path, file_url)


if __name__ == '__main__':
    pdd = ProductsDampDown()
    pdd.run()
