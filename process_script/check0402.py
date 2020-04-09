import os
import re
import logging
import logging.config


logger = logging.getLogger("oracle__")
log_path = os.getcwd() + '/Logs/'
print(log_path)
n=1
log_name = log_path + str(n)+'-log.log'
while os.path.exists(log_name):
    n+=1
    log_name = log_path + str(n)+'-log.log'

fh = logging.FileHandler(log_name, mode='a', encoding="utf8")
logger.addHandler(fh)


pattern = '[#￥{}【】；‘’：“”《》，。+=、？·&*$^\[\]\(\)/]'
def check_out(input_str,path):
    global noisy_list
    # pattern = '[\\[\\]\\(\\)\\/]'
    global pattern
    # 先去掉所有噪音符号
    new_str = remove_noisy(input_str)
    new_str = new_str.replace('[/',' ').replace('/]',' ').replace('[((',' ').replace('))]',' ')

    if re.search(pattern, new_str):
        logger.error(f'{path}\t{input_str}\tout')



def check_noisy(input_str,path):
    global noisy_list
    for noisy in noisy_list:
        input_str = input_str.replace(noisy,' ')
    flag = False
    for noisy in noisy_list:
        noisy_new = noisy.replace('[[','').replace(']]','')

        if noisy_new in input_str:
            # print(noisy_new)
            flag = True
    if flag:
        logger.error(f'{path}\t{input_str}\tnoisy')


def remove_noisy(input_str):
    global noisy_list
    for noisy in noisy_list:
        input_str = input_str.replace(noisy, ' ')
    return input_str


def check_in(input_str,path):
    input_str = remove_noisy(input_str)
    res1 = re.findall('\\[\\(\\(.*?\\)\\)\\]',input_str)
    # pattern = '[\\[\\]\\(\\)\\/]'
    global pattern
    flag = False
    if len(res1)>0:
        for each in res1:
            new_str = each[3:-3]
            new_str = remove_noisy(new_str)
            if re.search(pattern, new_str):
                flag = True

    res2 = re.findall('\\[\\/.*?\\/\\]',input_str)
    if len(res2) > 0:
        for each in res2:
            new_str = each[2:-2]
            new_str = remove_noisy(new_str)
            if re.search(pattern,new_str):
                # print(path,input_str)
                flag = True
    if flag:
        logger.error(f'{path}\t{input_str}\tin')


if __name__ == '__main__':
    noisy_list = []
    noisy_list.append('[[lipsmack]]')
    noisy_list.append('[[cough]]')
    noisy_list.append('[[sneeze]]')
    noisy_list.append('[[breath]]')
    noisy_list.append('[[background]]')
    noisy_list.append('[[laugh]]')

    # txt_path = r'apy161101034_r.txt'

    count = 0

    # with open(txt_path,'r',encoding='utf-8') as f:
    #     for line in f.readlines():
    #         line = line.strip()
    #         source_path = line.split('\t')[0].strip()
    #         content = line.split('\t')[-1].strip()
    #         check_in(content,source_path)
    #         check_out(content,source_path)
    #         check_noisy(content,source_path)

    work_dir = r'E:\数据备份'
    for root,dirs,files in os.walk(work_dir):
        for file in files:
            if file.endswith('txt'):
                txt_path = os.path.join(root,file)
                with open(txt_path,'r',encoding='utf-8') as f:
                    content = f.read()
                    check_out(content,txt_path)
                    check_in(content,txt_path)
                    check_noisy(content,txt_path)
