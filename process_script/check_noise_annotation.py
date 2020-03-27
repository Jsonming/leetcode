import os
import re
import logging

logger = logging.getLogger("yueyu")


def get_noise_list():
    # 获取噪音符号的配置文件
    noise_config_path = r'noise.txt'
    noise_list = []
    with open(noise_config_path, 'r', encoding='utf-8') as fn:
        for line in fn.readlines():
            noise_list.append(line.strip())
    return noise_list


def check_noise_annotation_old_norm(txt_path, input_str):
    # 获取配置文件的噪音标注列表
    noise_right_list = get_noise_list()
    # 匹配句子中的噪音标注
    noise_find_list = re.findall('\\[\\[.*?\\]\\]', input_str)
    for word in noise_find_list:
        if word not in noise_right_list:
            logger.error("{} has wrong noise_annotation".format(txt_path))
    # 去除所有正确标注后，检测多余中括号
    new_str = re.sub("\\[((.*?))\\]", " ", input_str)
    new_str = re.sub("\\[/.*?/\\]", " ", new_str)
    new_str = re.sub("\\[\\[.*?\\]\\]", " ", new_str)
    if '[' in new_str or ']' in new_str:
        logger.error('{} Noise label format error'.format(txt_path))


if __name__ == '__main__':
    work_dir = r'C:\Users\Administrator\Desktop\qit\session01'
    for root, dirs, files in os.walk(work_dir):
        for file in files:
            if file.endswith('txt'):
                txt_path = os.path.join(root, file)
                with open(txt_path, 'r', encoding='utf-8') as f:
                    str_read = f.read().strip()
                    check_noise_annotation_old_norm(txt_path, str_read)
