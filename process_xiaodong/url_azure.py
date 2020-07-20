#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/8 17:57
# @Author  : yangmingming
# @Site    : 
# @File    : url_azure.py
# @Software: PyCharm

sige_url = "https://datamallwangpan.blob.core.chinacloudapi.cn/test/get_azure_url_2.py?sv=2019-02-02&st=2020-07-08T09%3A44%3A04Z&se=2020-07-09T09%3A44%3A04Z&sr=b&sp=r&sig=4ks2ApYql%2BdZ8dCLX95ghoQ75ZoP3jwE0iIXqYcz7pk%3D"

url = "https://datamallwangpan.blob.core.chinacloudapi.cn/test/get_azure_url_2.py?" \
      "sv=2019-02-02&" \
      "st=2020-07-08T09:44:04Z&" \
      "se=2020-07-09T09:44:04Z&" \
      "sr=b&" \
      "sp=r&" \
      "sig=4ks2ApYql+dZ8dCLX95ghoQ75ZoP3jwE0iIXqYcz7pk="

sv = "字段包含共享访问签名的服务版本该值指定此共享访问签名使用的共享密钥授权的版本"
st = "可选的。共享访问签名变为有效的时间 就是秘钥生成的时间"
se = "需要。共享访问签名变为无效的时间 字段必须表示为UTC时间"
sr = "字段指定哪些资源是经由共享接入签名访问"
sp = "需要。与共享访问签名关联的权限。"
sig = "签名字符串是一个唯一的字符串，由必须验证的字段构成以授权请求。签名是使用SHA256算法在字符串到符号和密钥上计算的HMAC，然后使用Base64编码进行编码。"

# StringToSign = signedpermissions + "\n" +
#                signedstart + "\n" +
#                signedexpiry + "\n" +
#                canonicalizedresource + "\n" +
#                signedidentifier + "\n" +
#                signedIP + "\n" +
#                signedProtocol + "\n" +
#                signedversion + "\n" +
#                signedResource + "\n"
#                signedSnapshotTime + "\n" +
#                rscc + "\n" +
#                rscd + "\n" +
#                rsce + "\n" +
#                rscl + "\n" +
#                rsct