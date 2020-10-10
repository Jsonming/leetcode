import hashlib
import os
import shutil


def get_md5_value(src):
    """
        调用获取md5值的函数，返回文件的十六进制结果，并返回Md5结果
    :param src:
    :return:
    """
    try:
        with open(src, "rb") as fobj:
            code = fobj.read()

            myMd5 = hashlib.md5()  # 调用hashlib里的md5()生成一个md5 hash对象
            myMd5.update(code)  # 生成hash对象后，就可以用update方法对字符串进行md5加密的更新处理
            myMd5_Digest = myMd5.hexdigest()  # 加密后的十六进制结果

            return myMd5_Digest  # 返回十六进制结果
    except Exception as e:
        raise e


if __name__ == '__main__':
    work_list = []
    md5_dict = {}

    work_list.append(r'\\10.10.30.14\apy181115001_43408张人体抠图及18关键点数据\完整数据包_processed - 副本\data')
    dest_dir = r'\\10.10.30.14\apy181115001_43408张人体抠图及18关键点数据\重复'

    with open('img_result.txt', 'a', encoding='utf-8') as f:
        for work_dir in work_list:
            for root, dirs, files in os.walk(work_dir):
                for file in files:
                    if file.lower().endswith('jpg') or file.lower().endswith('png') or file.lower().endswith('jpeg'):
                        img_path = os.path.join(root, file)

                        md5_value = get_md5_value(img_path)  # 生成md5
                        if md5_value not in md5_dict:
                            md5_dict[md5_value] = img_path
                        else:
                            f.write(md5_dict[md5_value] + '\t' + img_path + '\n')  # 记录重复的数据

                            file_name, suffix = os.path.splitext(file)
                            metadata_path = root + '\\' + file_name + '.json'  # 获取图片对应的metadata路径

                            jpg_dest = img_path.replace(work_dir, dest_dir)  # 图片目标路径
                            metadata_dest = metadata_path.replace(work_dir, dest_dir)  # metadata目标路径

                            # 移动重复文件
                            dirname = os.path.dirname(jpg_dest)
                            if not os.path.exists(dirname):
                                os.makedirs(dirname)
                            shutil.move(img_path, jpg_dest)
                            shutil.move(metadata_path, metadata_dest)
