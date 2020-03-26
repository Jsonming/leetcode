# -*- coding: UTF-8 -*-
import io
import sys

import chardet
import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
# print(sys.getdefaultencoding())

headers = {
    'sign': '236c2e3750a13fcd8b1edf6ad1e7f346',
    'ch': '2101',
    'pid': '001',
    'token': '-1',
    'locale': 'zh-CN;CN',
    'appid': 'Android#001#CN',
    'nw': '1',
    'ocp': '128',
    'oak': 'cdb09c43063ea6bb',
    'User-Agent': 'Android%2FOPPO+R9%2F22%2F5.1.1%2FUNKNOWN%2F2%2F2101%2F7503',
    't': '1585047343712',
    'appversion': '7.5.1',
    'id': '355757350850620///',
    'sg': '89848b94fd36e6321af8f1170081bb4d1c759437',
    'traceId': 'vlodC2tQ-1585047343716',
    'pkg-ver': '0',
    'romver': '-1',
    'ocs': 'Android%2FOPPO+R9%2F22%2F5.1.1%2FUNKNOWN%2F2%2FR11-user+5.1.1+NMF26X+500200305+release-keys%2F7503',
    'Accept': 'application/x2-protostuff; charset=UTF-8',
    'Host': 'api-cn.store.heytapmobi.com',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip, deflate, br',

}

url = 'https://api-cn.store.heytapmobi.com/common/v1/comment/list?appId=33773&size=10&start=160&token=-1&type=all'
# requests.packages.urllib3.disable_warnings()


response = requests.get(url=url, headers=headers, verify=False)
# print(response.apparent_encoding)
# print(response.text)

# encode = chardet.detect(response.content)
# print(encode)

# print(response.encoding)
# a = response.content.decode('Windows-1254')
# print(a.encode('utf8'))

# response.encoding = None
for char in response.text:
    print(ord(char))

"""
HTTP/1.1 200 OK
Server: jfe
Date: Tue, 24 Mar 2020 10:55:44 GMT
Content-Type: application/x2-protostuff
Connection: keep-alive
ocd: 1
ogv: 20190129302
x-ocip: 125.33.159.69
Alternate-Protocol: 443:npn-spdy/3.1
Strict-Transport-Security: max-age=86400
Content-Length: 2610

"""
