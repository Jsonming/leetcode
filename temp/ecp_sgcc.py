#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/20 11:20
# @Author  : yangmingming
# @Site    : 
# @File    : ecp_sgcc.py
# @Software: PyCharm
import re
import os
import time
from urllib import parse

import requests
import tabula
from docx import Document
from lxml.html import etree
from win32com import client as wc


class EspSgcc(object):
    """
    国家电网中标（成交）结果公告抓取
    """

    def __init__(self):
        pass

    def crawl_project_list(self) -> list:
        """
        抓取项目列表信息
        :return: 返回信息列表
        """
        summary_info = []

        base_url = "http://ecp.sgcc.com.cn/news_list.jsp?site=global&column_code=014001007&company_id=00&news_name=all&pageNo=1"
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
        }
        response = requests.get(url=base_url, headers=headers).content.decode('utf8')
        info_page = self.parse_list_page(response)
        summary_info.extend(info_page)
        return summary_info

    def parse_list_page(self, response) -> list:
        """
        解析列表页页面
        :param response: 列表页页面
        :return: 返回一页列表页信息
        """
        info_data = []

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
                item_id = [i.replace("'", '').replace('"', "").strip() for i in detail_id.split(",")]
            else:
                item_id = ()
            item_company = item.xpath("./a/text()")
            if item_company:
                company_name = re.findall("\[.*?\]", item_company[0])
                item_company_name = company_name[0].replace("[", '').replace(']', "")
            else:
                item_company_name = ""
            info_data.append(
                {"company_name": item_company_name, "name": item_name, "time": item_time, "detail_id": item_id})

        return info_data

    def crawl_detail_page(self, detail_id: list) -> str:
        """
        抓取详细页面
        :param detail_id: 页面id
        :return: 页面内容
        """
        url = r"http://ecp.sgcc.com.cn/html/news/{}/{}.html".format(*detail_id)
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
        }
        return requests.get(url=url, headers=headers).content.decode('utf8')

    def parse_detail_page(self, content: str) -> list:
        """
        解析详情页面，两种形式，一种在页面中展示，一种在附件中展示
        :param content: html文本
        :return: 返回详细信息列表
        """
        # 解析页面中的表格
        d_root = etree.HTML(content)
        info_tables = d_root.xpath('//table')
        for table in info_tables:
            res = self.parse_table(table)

        # 下载附件附件， 原以为附件只有pdf,后来发现还有word
        pdf_ps = d_root.xpath('//p[@class="bot_list"]//a/@href')
        for pdf in pdf_ps:
            e_url = "http://ecp.sgcc.com.cn" + pdf
            file_name = self.crawl_enclosure(e_url)
            if file_name.endswith("pdf"):
                self.parse_pdf(file_name)
            elif file_name.endswith("docx"):
                self.parse_word(file_name)
            elif file_name.endswith("doc"):
                self.doc_to_docx(file_name)
                file_docx = file_name.replace("doc", "docx")
                self.parse_word(file_docx)

    def parse_table(self, table) -> list:
        """
        解析html中的表格数据， 将表格转化为dataframe
        :param table: 一个html的table对象
        :return:  返回一个列表嵌套列表 表示一个表格
        """
        res = []
        trs = table.xpath('.//tr')
        for tr in trs:
            tds = tr.xpath(".//td")
            res.append(["".join(td.xpath(".//text()")).strip() for td in tds])
        return res

    def crawl_enclosure(self, base_url):
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
        e_name = parse.unquote(e_response.url).split('/')[-1]
        e_content = e_response.content
        with open(e_name, 'wb', )as f:
            f.write(e_content)
        return e_name

    def doc_to_docx(self, file_path):
        """
        将doc 转化为docx 文件
        :param file_path: doc 文件路径
        :return: None
        """
        w = wc.Dispatch('Word.Application')
        # 或者使用下面的方法，使用启动独立的进程：
        # w = wc.DispatchEx('Word.Application')
        file = os.getcwd() + "\\" + file_path
        doc = w.Documents.Open(file)

        doc.SaveAs(file.replace("doc", "docx"), FileFormat=16)
        doc.Close()
        time.sleep(3)

    def parse_pdf(self, file_name):
        """
        解析pdf
        :param file_name:
        :return:
        """
        df = tabula.read_pdf(file_name, encoding='gbk', pages='all')


    def parse_word(self, file_name):
        document = Document(file_name)
        return document.tables

    def run(self):
        """
        主流程控制
        :return: None

        """
        project_info_list = self.crawl_project_list()
        for project in project_info_list:
            detail_id = project.get("detail_id")
            project_name = project.get("name")
            if "物资" in project_name:
                content = self.crawl_detail_page(detail_id)
                detail_info = self.parse_detail_page(content)


if __name__ == '__main__':
    ES = EspSgcc()
    ES.run()
