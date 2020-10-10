#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/20 11:04
# @Author  : yangmingming
# @Site    : 
# @File    : new_process_data.py
# @Software: PyCharm
import asyncio
import os
import re
import time
import pypinyin
import pandas as pd
from multiprocessing import Pool
from collections import defaultdict
from pybloom_live import ScalableBloomFilter, BloomFilter


class NewProcessData(object):
    """
    新处理老数据脚本
    """

    def __init__(self):
        pass

    def change_metadata(self, file):
        """
        修改metadata文件
        :param file:
        :return:
        """
        sra_map = {"快速": "Fast", "慢速": "Slow", "中速": "Medium"}
        mit_map = {"荣耀8": "honor 8",
                   "iso": "ios",
                   "安卓": "android",
                   }
        act_map = {
            "其它方言": 'Other',
            "閩語（福建方言）": "Min dialect(FuJian)",
            "闽话(福建方言)": "Min dialect(FuJian)",
            "闽语（福建方言）": "Min dialect(FuJian)",
            "标淮普通话(无方言)": "Standard Mandarin",
            "标准普通话（无方言）": "Standard Mandarin",
            "標準普通話（無方言）": "Standard Mandarin",
            "官話（北方方言）": "Standard Mandarin",
            "客家话": "Hakka dialect",
            "客家话(客家方言)": "Hakka dialect",
            "北方": "Northern dialect",
            "湘话(湖南方言)": "Hunan dialect",
            "湘语": "Hunan dialect",
            "官话(北方方言)": "Northern dialect",
            "粤语": "Cantonese (Cantonese dialect)",
            "粤话(广东方言)": "Cantonese (Cantonese dialect)",
            "西南方言": "Southwestern dialect",
            "吴语": "Wu dialect",
            "吴话(江浙方言)": "Wu dialect (Jiangsu and Zhejiang dialect)",
            "赣": "Gan Dialect",
            "赣话(江西方言)": "Gan Dialect (Jiangxi Dialect)",
            "西南": "Southwestern dialect",

            "华中地区": "Central China",
            "华南地区": "South China",
            "华东地区": "East China",
            "西南地区": "Southwest China",
            "西北地区": "Northwest China",
            "北京": "Beijing",
            "东北地区": "Northeast China",
            "华北地区": "North China",
            "天津河北": "Tianjin Hebei",
            "天津": "Tianjin"
        }
        acc_bir_map = {
            "暂无": "",
            '台湾': 'Taiwan',
            '广东省梅州市': 'Meizhou City, Guangdong Province',
            '云南省红河哈尼族彝族自治州': 'Honghe Hani and Yi Autonomous Prefecture of Yunnan Province',
            "台中及周邊(包含台中、彰化)": "Taichung and surrounding(Changhua)",
            "台北及周邊（包含台北、桃園、基隆）": "Taipei and surrounding(Taoyuan、Keelung)",
            "高雄及周邊(包含高雄、屏東)": "Kaohsiung and surrounding(Pingtung)",
            "台南及周邊(包含台南、嘉義)": "Tainan and surrounding(Chiayi)",
            "杭州": "Hangzhou",
            "北京": "Beijing",
            "南京": "Nanjing",
            "绵阳": "Mianyang",
            "厦门": "Xiamen",
            "贵阳": "Guiyang",
            "德阳": "Deyang",
            "崇州": "Chongzhou",
            "天津": "Tianjin",
            "河北": "Hebei",
            "成都": "Chengdu",
            "四川": "Sichuan",
            "福州": "Fuzhou",
            "美国": "United States",
            "泉州": "Quanzhou",
            "简阳": "Jianyang",
            "日本": "Japan",
            "漳州": "Zhangzhou",
            "吉林": "Jilin",
            "湖北": "Hubei",
            "贵州": "Guizhou",
            "乐山": "Leshan",
            "江西": "Jiangxi",
            "浙江": "Zhejiang",
            "泸州": "Luzhou",
            "大连": "Dalian",
            "上海": "Shanghai",
            "达州": "Dazhou",
            "长春": "Changchun",
            "唐山": "Tangshan",
            "香港": "Hong Kong",
            "南充": "Nanchong",
            "湖南": "Hunan",
            "福建": "Fujian",
            "云南": "Yunnan",
            "眉山": "Meishan",
            "河南": "Henan",
            "安徽": "Anhui",
            "江苏": "Jiangsu",
            "陕西": "Shaanxi",
            "广东": "Guangdong",
            "黑龙江": "Heilongjiang",
            "海南": "Hainan",
            "渭南": "Weinan",
            "商洛": "Shangluo",
            "儋州": "Danzhou",
            "徐州": "Xuzhou",
            "哈尔滨": "Harbin",
            "詹州": "Zhanzhou",
            "惠州": "Huizhou",
            "自贡": "Zigong",
            "咸阳": "Xianyang",
            "鹤壁": "Hebi",
            "宝鸡": "Baoji",
            "信阳": "Xinyang",
            "常德": "Changde",
            "中山": "Zhongshan",
            "郑州": "Zhengzhou",
            "西安": "Xi'an",
            "陇南": "Longnan",
            "延安": "Yan'an",
            "广州": "Guangzhou",
            "汉中": "Hanzhong",
            "江西上饶": "Shangrao City Jiangxi Province",
            "四川宜宾": "Yibin City Sichuan Province",
            "陕西省咸阳市": "Xianyang City Shaanxi Province",
            "天津市": "Tianjin City",
            "浙江温州": "Wenzhou City Zhejiang Province",
            "宁夏固原市": "Guyuan City Ningxia",
            "上海市": "Shanghai City",
            "山西省吕梁市": "Luliang City Shanxi Province",
            "山东省烟台市": "Yantai City Shandong Province",
            "广东省揭阳市": "Jieyang City Guangdong Province",
            "河北省衡水市": "Hengshui City Hebei Province",
            "湖南省郴州市": "Chenzhou City Hunan Province",
            "山东省青岛市": "Qingdao Shandong",
            "河南省郑州市": "Zhengzhou City Henan Province",
            "广西梧州": "Guangxi Wuzhou",
            "河北省邯郸市": "Handan City Hebei Province",
            "甘肃省平凉市": "Pingliang City Gansu Province",
            "重庆市": "Chongqing",
            "河南省鹤壁市": "Hebi City Henan Province",
            "山西省太原市": "Taiyuan Shanxi Province",
            "湖南省岳阳市": "Yueyang City Hunan Province",
            "湖北省襄樊市": "Xiangfan City Hubei Province",
            "山西省晋中市": "Jinzhong City Shanxi Province",
            "河北唐山": "Hebei Tangshan",
            "河南省濮阳市": "Puyang City Henan Province",
            "湖南省衡阳市": "Hengyang City Hunan Province",
            "贵州省遵义市": "Zunyi City Guizhou Province",
            "山西省大同市": "Datong City Shanxi Province",
            "陕西省西安市": "Xi'an Shaanxi Province",
            "福建省厦门市": "Xiamen City Fujian Province",
            "江西省吉安市": "Jian City Jiangxi Province",
            "湖北省黄石市": "Huangshi City Hubei Province",
            "江苏省徐州市": "Xuzhou City Jiangsu Province",
            "贵州省黔西南布依族苗族自治州": "Buyi and Miao Autonomous Prefecture in Southwest Guizhou Province",
            "江西省景德镇市": "Jingdezhen City Jiangxi Province",
            "江西省九江市": "Jiujiang City Jiangxi Province",
            "江苏省泰州市": "Taizhou City Jiangsu Province",
            "内蒙古包头市": "Baotou City Inner Mongolia",
            "云南省大理白族自治州": "Dali Bai Autonomous Prefecture Yunnan Province",
            "江苏省苏州市": "Suzhou City Jiangsu Province",
            "河北省唐山市": "Tangshan City Hebei Province",
            "广西省玉林市": "Yulin City Guangxi Province",
            "福建省莆田市": "Putian City Fujian Province",
            "湖南邵阳": "Hunan Shaoyang",
            "甘肃省庆阳市": "Qingyang City Gansu Province",
            "河南省许昌市": "Xuchang City Henan Province",
            "河北省石家庄市": "Shijiazhuang City Hebei Province",
            "湖北省随州市": "Suizhou City Hubei Province",
            "江苏省无锡市": "Wuxi City Jiangsu Province",
            "江苏省南通市": "Nantong City Jiangsu Province",
            "陕西延安": "Yan'an Shaanxi",
            "河北省保定市": "Baoding Hebei",
            "安徽省蚌埠市": "Bengbu City Anhui Province",
            "湖南省益阳市": "Yiyang City Hunan Province",
            "陕西省渭南市": "Weinan City Shaanxi Province",
            "湖北黄冈": "Hubei Huanggang",
            "浙江宁波": "Zhejiang Ningbo",
            "湖北省宜昌市": "Yichang City Hubei Province",
            "甘肃省金昌市": "Jinchang City Gansu Province",
            "山西省临汾市": "Linfen City Shanxi Province",
            "广东省汕头市": "Shantou City Guangdong Province",
            "山东省威海市": "Weihai City Shandong Province",
            "云南省临沧市": "Lincang City Yunnan Province",
            "山西省晋城市": "Jincheng City Shanxi Province",
            "陕西省安康市": "Ankang City Shaanxi Province",
            "广东省深圳市": "Shenzhen City Guangdong Province",
            "福建省福州市": "Fuzhou city of Fujian",
            "云南省楚雄彝族自治州": "Chuxiong Yi Autonomous Prefecture in Yunnan Province",
            "广西省南宁市": "Nanning City Guangxi Province",
            "河北邢台": "Xingtai Hebei",
            "四川省南充市": "Nanchong City Sichuan Province",
            "浙江省舟山市": "Zhoushan City Zhejiang Province",
            "湖南省株洲市": "Zhuzhou City Hunan Province",
            "河南省周口市": "Zhoukou City Henan Province",
            "河北省张家口市": "Zhangjiakou City Hebei Province",
            "湖北省武汉市": "Wuhan Hubei",
            "湖南省常德市": "Changde City Hunan Province",
            "甘肃省天水市": "Tianshui City Gansu Province",
            "贵州省六盘水市": "Liupanshui City Guizhou Province",
            "湖南省邵阳市": "Shaoyang City Hunan Province",
            "广西省柳州市": "Liuzhou City Guangxi Province",
            "山东省聊城市": "Liaocheng City Shandong Province",
            "江西省抚州市": "Fuzhou City Jiangxi Province",
            "内蒙古兴安盟": "Inner Mongolia Xing'an League",
            "广西省北海市": "Beihai City Guangxi Province",
            "广东广州": "Guangzhou Guangdong",
            "江西省新余市": "Xinyu City Jiangxi Province",
            "河北廊坊": "Hebei Langfang",
            "山东省德州市": "Dezhou City Shandong Province",
            "甘肃省兰州市": "Lanzhou City Gansu Province",
            "山西省长治市": "Changzhi City Shanxi Province",
            "山东省潍坊市": "Weifang City Shandong Province",
            "江西省赣州市": "Ganzhou City Jiangxi Province",
            "四川省绵阳市": "Mianyang City Sichuan Province",
            "浙江省温州市": "Wenzhou City Zhejiang Province",
            "广西省贺州市": "Hezhou City Guangxi Province",
            "山西淅川": "Shanxi Xichuan",
            "西藏拉萨市": "Lhasa Tibet",
            "广西南宁": "Guangxi Nanning",
            "广东省广州市": "Guangzhou Guangdong",
            "北京市": "Beijing",
            "甘肃省酒泉市": "Jiuquan City Gansu Province",
            "陕西省商洛市": "Shangluo City Shaanxi Province",
            "江西省宜春市": "Yichun City Jiangxi Province",
            "江苏省南京市": "Nanjing Jiangsu Province",
            "湖南省永州市": "Yongzhou City Hunan Province",
            "山东省滨州市": "Binzhou City Shandong Province",

            "山西": "Shanxi",
            "重庆": "Chongqing",
            "新疆": "Xinjiang",
            "广西": "Guangxi",
            "内蒙古": "Inner Mongolia",
            "宁夏": "Ningxia",
            "甘肃": "Gansu",
            "辽宁": "Liaoning",
            "山东": "Shandong",
        }

        with open(file, 'r+', encoding='utf8')as route_f:
            new_content = ""
            for line in route_f:
                field = line[:3]
                if field in ["SCD", "SEX", "AGE", "ACT", "BIR"]:
                    new_content += line.replace("无", "")
                elif field in ["CCD", "REP", "ACC", "SBF"]:
                    new_content += line.replace("噪声类", "Noise").replace("室内家具", "Indoor Furniture") \
                        .replace("北京顺义", "Beijing Shunyi").replace("低", "Low")
                # if field in ["ACC", "BIR"]:
                #     field_content = line.strip().split("\t")
                #     if len(field_content) == 1:
                #         new_content += field + "\t\n"
                #     elif len(field_content) == 2:
                #         new_content += field + "\t" + acc_bir_map.get(field_content[1], field_content[1]) + "\n"
                #     else:
                #         raise Exception("{}字段长度错误".format(field))
                # elif field == "ACT":
                #     field_content = line.strip().split("\t")
                #     if len(field_content) == 1:
                #         new_content += field + "\t\n"
                #     elif len(field_content) == 2:
                #         new_content += field + "\t" + act_map.get(field_content[1], field_content[1]) + "\n"
                #     else:
                #         raise Exception("{}字段长度错误".format(field))
                # elif field == "SEX":
                #     field_content = line.strip().split("\t")
                #     if len(field_content) == 1:
                #         new_content += field + "\t\n"
                #     elif len(field_content) == 2:
                #         new_content += field + "\t" + re.sub("Femal[e]*", "Female", field_content[1]) + "\n"
                #     else:
                #         raise Exception("{}字段长度错误".format(field))
                # elif field == 'MIT':
                #     field_content = line.strip().split("\t")
                #     if len(field_content) == 1:
                #         new_content += field + "\t\n"
                #     elif len(field_content) == 2:
                #         new_content += field + "\t" + mit_map.get(field_content[1], field_content[1]) + "\n"
                #     else:
                #         raise Exception("{}字段长度错误".format(field))
                # elif field == 'SRA':
                #     field_content = line.strip().split("\t")
                #     if len(field_content) == 1:
                #         new_content += field + "\t\n"
                #     elif len(field_content) == 2:
                #         new_content += field + "\t" + sra_map.get(field_content[1], field_content[1]) + "\n"
                #     else:
                #         raise Exception("{}字段长度错误".format(field))
                else:
                    new_content += line
            # print(new_content)
            route_f.seek(0)
            route_f.truncate()
            route_f.write(new_content)

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

    def delete_duplicate_data(self, file):
        """
        去重函数
        :param file:
        :return:
        """
        bloom = ScalableBloomFilter(initial_capacity=100, error_rate=0.00000001)
        temp_name = file.replace(".txt", "_temp.txt")
        with open(file, 'r', encoding='utf8')as r_f, open(temp_name, 'a', encoding='utf8')as w_f:
            for line in r_f:
                line_content = line.strip()
                if line_content not in bloom:
                    bloom.add(line_content)
                    w_f.write(line_content + "\n")
                else:
                    print(line_content)
        os.remove(file)
        os.rename(temp_name, file)

    def com_data(self):
        a = ["华中地区", "华南地区", "华东地区", "西南地区", "西北地区", "北京", "东北地区", "华北地区", "天津河北", "天津"]
        b = ["Central China", "South China", "East China", "Southwest China", "Northwest China", "Beijing",
             "Northeast China", "North China", "Tianjin Hebei", "Tianjin"]

        a = ["安徽", "天津", "河南", "香港", "山西", "重庆", "新疆", "北京", "广西", "湖北", "黑龙江", "福建", "浙江", "上海", "广东", "江西", "内蒙古",
             "河北", "云南", "湖南", "宁夏", "吉林", "四川", "贵州", "甘肃", "陕西", "辽宁", "江苏", "山东"]
        b = ["Anhui", "Tianjin", "Henan", "Hong Kong", "Shanxi", "Chongqing", "Xinjiang", "Beijing", "Guangxi", "Hubei",
             "Heilongjiang", "Fujian", "Zhejiang", "Shanghai", "Guangdong", "Jiangxi", "Inner Mongolia", "Hebei",
             "Yunnan", "Hunan", "Ningxia", "Jilin", "Sichuan", "Guizhou", "Gansu", "Shaanxi", "Liaoning", "Jiangsu",
             "Shandong"]
        for k, v in zip(a, b):
            print('"{k}": "{v}",'.format(**locals()))

    def run(self):
        project_path = r"\\10.10.30.14\语音数据_2016\apy161101025_739人中国儿童麦克风采集语音数据\完整数据包_processed\data\category"
        project_path = r"\\10.10.30.14\语音数据_2017\APY170701046_2_远场家居采集语音数据_噪音数据\完整数据包\Gnoise1\session01"
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith("metadata"):
                    file_path = os.path.join(root, file)
                    self.change_metadata(file_path)

        # file = r"\\10.10.30.14\语音数据_2016\APY161101015_D_20万条维语发音词典\完整数据包\data\维语发音词典.txt"
        # self.delete_duplicate_data(file)


if __name__ == '__main__':
    npd = NewProcessData()
    npd.run()
