#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/20 11:20
# @Author  : yangmingming
# @Site    : 
# @File    : ecp_sgcc.py
# @Software: PyCharm
import re
import requests
from lxml.html import etree


class EspSgcc(object):
    """
    国家电网中标（成交）结果公告抓取
    """

    def __init__(self):
        pass

    def parse_list_page(self, response) -> list:
        """
        解析列表页页面
        :param response: 列表页页面
        :return: 返回一页列表页信息
        """
        root = etree.HTML(response)
        info_li = root.xpath('//ul[@class="newslist01"]/li')
        for item in info_li:
            item_time = item.xpath("./span/text()")
            if item_time:
                item_time = item_time[0].strip()
            else:
                item_time = ''
            item_name = item.xpath("./a/@title")
            if item_name:
                item_name = item_name[0].replace("\r", '').replace("\t", '').replace("\n", '')
            else:
                item_name = ""
            item_detail_id = item.xpath("./a/@onclick")
            if item_detail_id:
                detail_id = item_detail_id[0].replace("showNewsDetail(", '').replace(");", '')
                item_id = [int(i.replace("'", '').replace('"', "")) for i in detail_id.split(",")]
            else:
                item_id = ()
            item_company = item.xpath("./a/text()")
            if item_company:
                company_name = re.findall("\[.*?\]", item_company[0])
                item_company_name = company_name[0]
            else:
                item_company_name = ""

            print(item_company_name)
            print(item_name)
            print(item_time)
            print(item_id)

        return []

    def crawl_project_list(self) -> list:
        """
        抓取项目列表信息
        :return: 返回信息列表
        """
        base_url = "http://ecp.sgcc.com.cn/news_list.jsp?site=global&column_code=014001007&company_id=00&news_name=all&pageNo=1"
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
        }
        response = requests.get(url=base_url, headers=headers).text
        info_page = self.parse_list_page(response)
        return []

    def run(self):
        """
        主流程控制
        :return: None
        """
        project_info_list = self.crawl_project_list()


if __name__ == '__main__':
    ES = EspSgcc()
    ES.run()
