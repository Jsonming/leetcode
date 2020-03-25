import logging
import os
import re
import shutil
import sys
import wave

from process_script.metada_update import AudioMetadata, write_meta, read_supplement

logger = logging.getLogger("yueyu")


class Check(object):
    def __init__(self, src, dst, workbook):
        self.src = src
        self.dst = dst
        self.workbook = workbook

    def move(self, src_path):
        dst_path = os.path.join(self.dst, os.path.relpath(src_path, self.src))
        dirname = os.path.dirname(dst_path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        shutil.move(src_path, dst_path)
        shutil.move(src_path.replace('.wav', '.txt'), dst_path.replace('.wav', '.txt'))
        shutil.move(src_path.replace('.wav', '.metadata'), dst_path.replace('.wav', '.metadata'))

    def spain(self, userinfo):
        userinfos = {}
        for group, infos in userinfo.items():
            if infos['city'] in userinfos:
                userinfos[infos['city']].update({group: infos})
            else:
                userinfos.update({infos['city']: {group: infos}})
        return userinfos

    def checkers(self, option):
        logger.error("Start")

        # 用户信息，不知道在哪里用
        userinfo = read_supplement(self.workbook)
        userinfo = self.spain(userinfo)

        errors = []
        for path, dirs, files in os.walk(self.src):
            for file in files:
                if os.path.splitext(file)[-1] == '.wav':
                    audio_f = os.path.join(path, file)
                    txt_f = audio_f.replace('.wav', '.txt')
                    meta_f = audio_f.replace('.wav', '.metadata')

                    wav_checker = WAV(audio_f)
                    if os.path.exists(txt_f):
                        txt_checker = TXT(txt_f)
                    else:
                        logger.error("Don't have txt file {}".format(audio_f))
                        continue
                    if os.path.exists(meta_f):
                        meta_checker = Metadata(meta_f)
                    else:
                        logger.error("Don't have meta file {}".format(audio_f))
                        continue

                    if option == 'update':
                        lines = txt_checker.update()
                        txt_checker.check(lines)
                        meta_checker.update(userinfo, self.src, self.dst, errors)
                        meta_checker.check()
                        wav_checker.check()

                    elif option == 'check':
                        txt_checker.check()
                        # meta_checker.update(userinfo, self.src, self.dst, errors)
                        meta_checker.check()
                        wav_checker.check()

                    # if not txt_checker.flag or not meta_checker.flag or not wav_checker.flag:
                    #     self.move(audio_f)

        logger.error("End")


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
            logger.error("{} not encode utf-8".format(self.filepath))
            self.flag = False

    def is_has_ch(self, lines):
        # 是否含有中文
        z = re.compile(u'[\u4e00-\u9fa5]')
        for line in lines:
            if z.search(line):
                self.flag = False
                logger.error("Has chinese in {}".format(self.filepath))
                return

    def write_file(self, lines):
        with open(self.filepath, 'w') as f:
            for line in lines:
                f.write(line)


class TXT(File):
    def ch_to_en(self, lines):
        # 中文标点转英文
        table = {ord(f): ord(t) for f, t in zip('【】；‘’：“”《》，。、？', '[];\'\':""<>,. ?')}
        return [text.translate(table) for text in lines]

    def remove(self, lines):
        # 去除斜杠
        new_lines = []
        for line in lines:
            new_lines.append(re.sub('/|~', '', line))
        return new_lines

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
            self.flag = False
            logger.error("Has double str(quan jiao) {} is {}".format(self.filepath, double_s))

    def dbc2sbc(self, lines):
        """全角转半角"""
        new_lines = []
        for line in lines:
            rstring = ''
            for uchar in line:
                inside_code = ord(uchar)
                if inside_code == 0x3000:
                    inside_code = 0x0020
                else:
                    inside_code -= 0xfee0
                if not (0x0021 <= inside_code and inside_code <= 0x7e):
                    rstring += uchar
                    continue
                rstring += chr(inside_code)
            new_lines.append(rstring)

        return new_lines

    def is_one_line(self, lines: list):
        """
         判断是否为一行
        :param lines: 文本行
        :return:
        """
        if len(lines) != 1:
            self.flag = False
            logger.error("{} the file is empty or multi-line".format(self.filepath))
        else:
            content = lines[0].strip()
            if not content:
                self.flag = False
                logger.error("{} the file is line break".format(self.filepath))

    def is_have_digit(self, lines):
        """
        是否包含数字
        :param lines:
        :return:
        """
        P_DIGIT = re.compile(u'\d+')
        digit = P_DIGIT.findall(lines[0])
        if digit:
            self.flag = False
            logger.error("{} contains numbers is {}".format(self.filepath, digit))

    def is_have_symbol(self, lines):
        """
        判断是否有特殊字符
        :param lines: 行内容
        :return:
        """
        P_SYMBOL_FULL = re.compile('[@~#￥%{}【】；‘’：“”《》，。、？·&*$^\[\]/]')
        special_symbol = P_SYMBOL_FULL.findall(lines[0])
        if special_symbol:
            self.flag = False
            logger.error("{} contains special symbol is {}".format(self.filepath, special_symbol))

    def update(self):
        # 更新
        lines = self.read_file()
        for updater in [self.ch_to_en, self.dbc2sbc, self.remove]:
            lines = updater(lines)
        self.write_file(lines)
        return lines

    def check(self, lines=None):
        # 检查
        if not lines:
            lines = self.read_file()
        self.is_one_line(lines)

        # 如果不存在空行和多行的情况进入的特殊字符的检查
        if self.flag:
            self.is_have_digit(lines)
            # self.is_have_symbol(lines)
            self.is_double_str(lines)


class Metadata(File):
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

    def read_meta(self):
        infos = {}
        with open(self.filepath, 'r', encoding='utf-8') as f:
            for line in f:
                info = line.strip().split('\t')
                if len(info) != 2:
                    info = line.strip().split(' ')
                if len(info) == 2:
                    k, v = info
                    infos.update({k: v})
        return infos

    def update(self, userinfo, src, dst, errors):
        infos = self.read_meta()
        valid_infos = {self.meta_map[key]: value for key, value in infos.items() if key in self.meta_map}
        try:
            valid_infos.update(userinfo[self.group])
        except KeyError as e:
            if self.group not in errors:
                logger.error("Don't have group in userinfo {}".format(self.group))
            errors.append(self.group)
            return ''
        metadata = AudioMetadata()
        # import pdb;pdb.set_trace()
        try:
            content = metadata.template.format(**valid_infos)
        except KeyError as e:
            logger.error("can't match {}".format(self.filepath))
            return ''
        # relpath = os.path.relpath(self.filepath, src)
        # meta_path = os.path.join(dst, relpath)
        # mkdir_if_not_exists(os.path.dirname(meta_path))
        write_meta(self.filepath, content)
        # return meta_path

    def check(self):
        z = re.compile(u'[\u4e00-\u9fa5]')
        meta_no_null = ['SEX', 'AGE', 'ACC', 'ACT', 'ORS']
        lines = self.read_file()
        meta = {}

        for line in lines:
            line = line.strip()
            if z.search(line) and 'ORS' not in line:
                self.flag = False
                logger.error("{} content contains chinese".format(self.filepath))

            if len(line.split('\t')) > 2:
                self.flag = False
                logger.error("{} content redundant TAB keys".format(self.filepath))
            elif len(line.split('\t')) == 1:
                if line.split('\t')[0] in meta_no_null:
                    self.flag = False
                    logger.error("{} key is null".format(self.filepath))
            else:
                key = line.split('\t')[0]
                valve = line.split('\t')[1]
                meta[key] = valve
        # print(meta)
        for m in meta_no_null:
            # print(meta[m])
            if not m in meta.keys():
                self.flag = False
                logger.error("{} {} key is null".format(self.filepath, m))
            else:
                if not meta['SEX'] in ['Male', 'Female']:
                    self.flag = False
                    logger.error("{} value format is err".format(self.filepath))


class WAV(File):
    min_length = 15
    audio_channel = 1
    sample_width = 2
    framerate = [16000, 22050, 44100]

    def check(self):
        fsize = os.path.getsize(self.filepath)
        txt_file = self.filepath.replace('.wav', '.txt')
        meta_file = self.filepath.replace('.wav', '.metadata')

        if not os.path.exists(txt_file) or not os.path.exists(meta_file):
            self.flag = False
            logger.error("{} missing files".format(self.filepath))

        if fsize / float(1024) < self.min_length:
            self.flag = False
            logger.error("{} size error".format(self.filepath))
        else:
            with wave.open(self.filepath, 'rb') as f:
                if not f.getnchannels() == self.audio_channel:
                    self.flag = False
                    logger.error("{} channel error".format(self.filepath))

                if not f.getframerate() in self.framerate:
                    self.flag = False
                    logger.error("{} sample error".format(self.filepath))
                if not f.getsampwidth() == self.sample_width:
                    self.flag = False
                    logger.error("{} sample width error".format(self.filepath))


if __name__ == '__main__':
    # root, audio_size, audio_sample, audio_channel, meta_key, sy_list = read_ini('config.txt')

    try:
        # 脚本使用
        src_path = sys.argv[1]
        dst_path = sys.argv[2]
        workbook = sys.argv[3]
        option = sys.argv[4]
    except Exception as e:
        # 集成环境使用
        src_path = r'\\10.10.30.14\刘晓东\数据分类\语音数据\apy161101031_r_215小时美式英语手机采集语音数据\开发用demo'
        dst_path = ''
        workbook = ''
        option = 'check'

    c = Check(src_path, dst_path, workbook)
    c.checkers(option)