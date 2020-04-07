#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/3 18:58
# @Author  : yangmingming
# @Site    : 
# @File    : project_check.py
# @Software: PyCharm
import logging
import os
import re
import wave

logger = logging.getLogger("yueyu")
log_path = os.path.dirname(os.getcwd()) + '/Logs/'
log_name = log_path + 'log.log'
fh = logging.FileHandler(log_name, mode='a', encoding="utf8")
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logger.addHandler(fh)
logger.addHandler(console)


class ProjectCheck(object):
    def __init__(self):
        pass

    def check_file_complete(self, projec_path):
        """
        检查项目中文件完整性
        :param projec_path:
        :return:
        """
        logging.warning("project file check start")
        for root, dirs, files in os.walk(project_path):
            for file in files:
                name, suffix = os.path.splitext(file)
                wav_file = os.path.join(root, name + ".wav")
                txt_file = os.path.join(root, name + ".txt")
                meta_file = os.path.join(root, name + ".metadata")
                for item in [wav_file, txt_file, meta_file]:
                    if not os.path.exists(item):
                        logger.error("{}\tdoes not exist".format(item))
        logging.warning("project file check end")

    def check(self, project_path):
        """
        检查项目
        :param project_path:
        :return:
        """
        logging.warning("Start")
        self.check_file_complete(project_path)  # 检查文件的完整性

        for root, dirs, files in os.walk(project_path):
            for file_name in files:
                file = os.path.join(root, file_name)
                if file.endswith("wav"):
                    wav = WAV(file)
                    wav.check()
                elif file.endswith("metadata"):
                    meta = Metadata(file)
                    meta.check()
                else:
                    txt = TXT(file)
                    txt.check()


class File(object):
    GROUP_REGEX = re.compile('(?P<group>[G|Z]\d+)[A-F\d_]*(?P<session>S\d+)\.')

    def __init__(self, filepath):
        self.filepath = filepath
        self.flag = True
        r = self.GROUP_REGEX.search(os.path.basename(filepath))
        if r:
            self.group = r.group('group').strip()
        else:
            self.group = os.path.basename(filepath)

    def read_file(self):
        """
         读取文件,捕获编码，如果不是utf8 抛出异常
        :return:
        """
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return f.readlines()
        except UnicodeDecodeError as e:
            logger.error("{}\t not encode utf-8".format(self.filepath))


class TXT(File):
    def is_double_str(self, lines):
        """
        是否包含全角
        :param lines:
        :return:
        """
        double_s = []
        double_str = lambda x: ord(x) == 0x3000 or 0xFF01 <= ord(x) <= 0xFF5E
        for line in lines:
            for x in line:
                if double_str(x):
                    double_s.append(x)
        if double_s:
            logger.error("{}\t Has double str(quan jiao) is {}".format(self.filepath, double_s))

    def is_one_line(self, lines: list):
        """
         判断是否为一行
        :param lines: 文本行
        :return:
        """
        if len(lines) == 0:
            logger.error("{}\t the file is empty".format(self.filepath))
        elif len(lines) > 1:
            logger.error("{}\t the file is Multi-line".format(self.filepath))
        else:
            content = lines[0].strip()
            if not content:
                logger.error("{}\t the file is line break".format(self.filepath))

    def is_have_digit(self, lines):
        """
        是否包含数字
        :param lines:
        :return:
        """
        P_DIGIT = re.compile(u'\d+')
        digit = P_DIGIT.findall(lines[0])
        if digit:
            logger.error("{}\t contains numbers is {}".format(self.filepath, digit))

    def is_have_symbol(self, lines):
        """
        判断是否有特殊字符
        :param lines: 行内容
        :return:
        """
        P_SYMBOL_FULL = re.compile('[#￥{}【】；‘’：“”《》，。、？·&*$^]')
        special_symbol = P_SYMBOL_FULL.findall(lines[0])
        if special_symbol:
            logger.error("{}\t contains special symbol is {}".format(self.filepath, special_symbol))

    def check(self, lines=None):
        # 检查单行多行
        if not lines:
            lines = self.read_file()
        self.is_one_line(lines)

        # 如果不存在空行和多行的情况进入的特殊字符的检查
        if self.flag:
            self.is_have_digit(lines)
            self.is_have_symbol(lines)
            self.is_double_str(lines)


class Metadata(File):
    def check(self):
        z = re.compile(u'[\u4e00-\u9fa5]')
        meta_no_null = ['SEX', 'AGE', 'ACC', 'ACT', "BIR"]
        meta = {}

        lines = self.read_file()
        for line in lines:
            line = line.strip()
            if z.search(line) and 'ORS' not in line:
                logger.error("{}\t content contains chinese".format(self.filepath))

            if len(line.split('\t')) > 3:
                logger.error("{}\t content redundant TAB keys".format(self.filepath))
            elif len(line.split('\t')) == 3:
                if "LBR" in line or "LBO" in line:
                    pass
                else:
                    logger.error("{}\t content redundant TAB keys, {}".format(self.filepath, line.split('\t')[0]))
            elif len(line.split('\t')) == 1:
                if line.split('\t')[0] in meta_no_null:
                    logger.error("{}\t {} key is null".format(self.filepath, line.split('\t')[0]))
            else:
                key = line.split('\t')[0]
                valve = line.split('\t')[1]
                meta[key] = valve

        for m in meta_no_null:
            if m not in meta.keys():
                logger.error("{}\t {} key is null".format(self.filepath, m))
            else:
                if not meta['SEX'] in ['Male', 'Female']:
                    logger.error("{}\t value format is err".format(self.filepath))


class WAV(object):
    min_length = 15
    audio_channel = 1
    sample_width = 2
    framerate = [16000, 22050, 44100]

    def __init__(self, file_path):
        self.filepath = file_path

    def check(self):
        fsize = os.path.getsize(self.filepath)
        if fsize / float(1024) < self.min_length:
            logger.error("{}\t size error".format(self.filepath))
        else:
            with wave.open(self.filepath, 'rb') as f:
                if not f.getnchannels() == self.audio_channel:
                    logger.error("{}\t channel error".format(self.filepath))
                if not f.getframerate() in self.framerate:
                    logger.error("{}\t sample error".format(self.filepath))
                if not f.getsampwidth() == self.sample_width:
                    logger.error("{}\t sample width error".format(self.filepath))


if __name__ == '__main__':
    # project_path = r"\\10.10.30.14\刘晓东\oracle_交付\apy161101028_g_351人意大利语手机采集语音数据\完整数据包_processed\data"
    # project_path = r"\\10.10.30.14\刘晓东\oracle_交付\apy161101028_r_215小时意大利语手机采集语音数据_朗读\完整数据包_加密后数据\data"
    # project_path = r"\\10.10.30.14\刘晓东\oracle_交付\apy161101033_g_405人法语手机采集语音数据\data"
    # project_path = r"\\10.10.30.14\刘晓东\oracle_交付\apy161101033_r_232小时法语手机采集语音数据\data"
    # project_path = r"\\10.10.30.14\刘晓东\oracle_交付\apy161101034_g_343人西班牙语手机采集语音数据\data"
    project_path = r"\\10.10.30.14\刘晓东\oracle_交付\apy161101034_r_227小时西班牙语手机采集语音数据\data"
    pc = ProjectCheck()
    pc.check(project_path)
