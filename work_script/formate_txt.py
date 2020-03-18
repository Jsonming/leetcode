import os
import re


def E_trans_to_C(string):
    E_pun = u',.!?[]()<>"\''
    C_pun = u'，。！？【】（）《》“‘'
    table = {ord(f): ord(t) for f, t in zip(E_pun, C_pun)}
    return string.translate(table)


def strQ2B(txt_path):
    global noise
    """全角转半角"""
    with open(txt_path, 'r', encoding='utf-8') as fr:
        ustring = fr.read()

    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif 65281 <= inside_code <= 65374:  # 全角字符（除空格）根据关系转化
            inside_code -= 65248
        rstring += chr(inside_code)
    rstring = rstring.replace('。', '.').replace('【', '[').replace('】', ']').replace('〜', '~')

    # 检查拼写错误
    noise_find = re.findall('\\[\\[.*?\\]\\]', rstring)
    for each in noise_find:
        if each not in noise:
            print("*" * 300)
            print('noise_err:\t' + each + "\t" + txt_path)
            print("*" * 300)

    label = re.sub("\\[\(\(.*?\)\)\\]", " ", rstring)
    label = re.sub("\\[/.*?/\\]", " ", label)
    label = re.sub("\\[\\[.*?\\]\\]", " ", label)

    return label


def to_start(work_dir):
    for root, dirs, files in os.walk(work_dir):
        for file in files:
            if file.endswith('txt'):
                txt_path = os.path.join(root, file)
                new_string = strQ2B(txt_path)

                # 检查不合法的[]
                if '[' in new_string or ']' in new_string:
                    # with open(txt_path,'r',encoding='utf-8') as fr:
                    #     s = fr.read()
                    #
                    # with open(txt_path,'w',encoding='utf-8') as fw:
                    #     s  = s.replace('[{','').replace('}]','')
                    #     s= s.replace('[babble/]','')
                    #     s = s.replace('[/babble]', '')
                    #     s = s.replace('[music/]', '')
                    #     s = s.replace('[/music]', '')
                    #     fw.write(s)
                    print(new_string)
                    print(root)
                    print(file)


if __name__ == '__main__':
    noise = []
    noise.append('[[lipsmack]]')
    noise.append('[[laugh]]')
    noise.append('[[cough]]')
    noise.append('[[sneeze]]')
    noise.append('[[breath]]')
    noise.append('[[background]]')
    noise = set(noise)

    # work_dir = r'\\IT-20190729TRCT\数据备份_liuxd\apy170901049_347小时意大利语手机采集语音数据\完整数据包_加密后数据\data\category'
    # work_dir = r'\\IT-20190729TRCT\数据备份_liuxd\apy170801048_338小时西班牙语手机采集语音数据\完整数据包_processed\data\category'
    # work_dir = r'\\IT-20190729TRCT\数据备份_liuxd\apy161101034_r_227小时西班牙语手机采集语音数据\完整数据包_processed\data\category'
    # work_dir = r'\\IT-20190729TRCT\数据备份_liuxd\apy161101034_g_343人西班牙语手机采集语音数据\完整数据包_processed\data\category'
    # work_dir = r'\\IT-20190729TRCT\数据备份_liuxd\apy161101033_r_232小时法语手机采集语音数据\完整数据包_processed\data\category'
    # work_dir = r'\\IT-20190729TRCT\数据备份_liuxd\apy161101033_g_405人法语手机采集语音数据\完整数据包_processed\data\category'
    # work_dir = r'\\IT-20190729TRCT\数据备份_liuxd\apy161101028_r_215小时意大利语手机采集语音数据_朗读\完整数据包_加密后数据\data\category'
    work_dir = r'\\IT-20190729TRCT\数据备份_liuxd\apy161101028_g_351人意大利语手机采集语音数据\完整数据包_processed\data\category'

    to_start(work_dir)
