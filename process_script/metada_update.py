# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import re
import sys
import pandas as pd
import openpyxl as px

meta_map = {
    'SES': 'dirname',
    'DIR': 'dirpath',
    'FIP': 'dirpath',
    'SAM': 'frame',
    'SNB': 'sample_width',
    'SBF': 'lohi',
    'SSB': 'per_bits',
    'QNT': 'type',
    'NCH': 'channels',
    'SCD': 'dirname',
    'LBD': 'mark_file',
    'LBR': 'length',
    'ORS': 'text'
}

empty_map = {
    u'bir': '', u'city': '', u'phone_type': '', u'per_bits': u'16', u'text': '', u'frame': u'16000', u'sex': '',
    u'channels': u'1', u'age': '', u'length': '', u'lohi': u'lohi', u'dirpath': '', u'local_accent': '', u'dirname': '',
    u'type': u'wav', u'mark_file': '', u'sample_width': u'2'
}


def mkdir_if_not_exists(filepath):
    if not os.path.exists(filepath):
        os.makedirs(filepath)


class AudioMetadata():
    @property
    def template(self):
        return u"""LHD\t{LHD}
DBN\t{DBN}
SES\t{SES}
CMT\t{CMT}
FIP\t{FIP}
CCD\t{CCD}
REP\t{REP}
RED\t{RED}
RET\t{RET}
CMT\t{CMT}
SAM\t{SAM}
SNB\t{SNB}
SBF\t{SBF}
SSB\t{SSB}
QNT\t{QNT}
NCH\t{NCH}
CMT\t{CMT}
SCD\t{SCD}
SEX\t{SEX}
AGE\t{AGE}
ACC\t{ACC}
ACT\t{ACT}
BIR\t{BIR}
CMT\t{CMT}
SNQ\t{SNQ}
MIP\t{MIP}
MIT\t{MIT}
SCC\t{SCC}
CMT\t{CMT}
LBD\t{LBD}
LBR\t{LBR}
LBO\t{LBO}
CMT\t{CMT}
SRA\t{CMT}
EMO\t{EMO}
ORS\t{text}"""


def load_xlsx(filename, sheet_titles=[], columns=[], rows=[]):
    wb = px.load_workbook(filename=filename)
    workbook = {}
    for ws in wb:
        if sheet_titles and not ws.title in sheet_titles:
            continue
        workbook[ws.title] = []
        for row in ws.rows:
            vals = []
            for cell in row:
                vals.append(cell.value)
            workbook[ws.title].append(vals)
    return workbook


def read_meta(filepath):
    infos = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            info = line.strip().split('\t')
            if len(info) != 2:
                info = line.strip().split(' ')
            if len(info) == 2:
                k, v = info
                infos.update({k: v})
    return infos


def write_meta(dstpath, data):
    with open(dstpath, 'w', encoding='utf-8') as f:
        f.write(data)


def read_supplement(workbook):
    """
    读取需要更新的 execl表格, 表格约定，第一列为需要更新的组，后面列为需要更新的字段
    :param workbook:
    :return:
    """
    if os.path.exists(workbook):
        df = pd.read_excel(workbook, index_col=0)
        return df


def read_spain_supplement(workbook):
    attributes = ["sex", "age", "local_accent", "city", "phone_type"]
    if not os.path.exists(workbook) or not os.path.isfile(workbook):
        return {}

    try:
        supplement_table = load_xlsx(workbook)['Speakerinfo'][1:]
    except KeyError as e:
        return {}

    users_info = {}
    for row in supplement_table:
        if row and any(row):
            userinfo = {}
            end = min(len(row), 7)
            for i, cell in enumerate(row[2:end]):
                if cell == None or cell == '':
                    continue

                attr = attributes[i]
                if attr == 'age':
                    userinfo[attr] = int(float(cell))
                else:
                    userinfo[attr] = cell.strip()

            username = row[1].strip()
            userinfo.update({'bir': userinfo['city']})
            if userinfo['city'] in users_info:
                users_info[userinfo['city']].update({username: userinfo})
            else:
                users_info[userinfo['city']] = {username: userinfo}

    return users_info


GROUP_REGEX = re.compile('(?P<group>[G|Z]\d+)[A-F\d_]*(?P<session>S\d+)\.wav')


def update(src, dst, excelpath):
    errors = []
    userinfo = read_supplement(excelpath)
    for path, dirs, filenames in os.walk(src):
        for filename in filenames:
            if not filename.endswith('.metadata'):
                continue
            r = GROUP_REGEX.search(filename)
            if r:
                group = r.group('group').strip()
            else:
                group = os.path.basename(path)

            infos = read_meta(os.path.join(path, filename))
            valid_infos = {meta_map[key]: value for key, value in infos.items() if key in meta_map}
            try:
                valid_infos.update(userinfo[group])
            except KeyError as e:
                if group not in errors:
                    print(group)
                errors.append(group)
                continue
            metadata = AudioMetadata()
            # import pdb;pdb.set_trace()
            try:
                content = metadata.template.format(**valid_infos)
            except KeyError as e:
                # valid_infos.update(empty_map)
                # content = metadata.template.format(**valid_infos)
                print("can't match {}".format(filename))
                continue
            relpath = os.path.relpath(os.path.join(path, filename), src)
            meta_path = os.path.join(dst, relpath)
            mkdir_if_not_exists(os.path.dirname(meta_path))
            write_meta(meta_path, content)


if __name__ == '__main__':
    # src = r'\\10.10.8.123\700小时墨西哥哥伦比亚西班牙语采集标注项目-自有\结果数据\自有入库\哥伦比亚\data\category\G00002'
    # dst = r'\\10.10.8.123\700小时墨西哥哥伦比亚西班牙语采集标注项目-自有\结果数据\新版metadata'
    # excelpath = r'E:\linguist\spain\info\700小时西班牙语-非西班牙.xlsx'
    src = sys.argv[1]
    dst = sys.argv[2]
    excelpath = sys.argv[3]
    # handle(src, dst, excelpath)
