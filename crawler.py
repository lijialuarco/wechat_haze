# coding=utf-8

import requests
import urllib.request
from bs4 import BeautifulSoup
import os
import time
import logging
import logging.config
from PIL import Image
import pytesseract
import re
import json
from datetime import datetime
import datetime as dt


def amendmentName(index, base):
    index = int(index)
    return (base + dt.timedelta(days=index // 9 - 1, hours=((index - 1) % 8) * 3)).strftime('%Y年%m月%d日%H时')


def addtwodimdict(thedict, key_a, key_b, val):
    if key_a in thedict:
        thedict[key_a].update({key_b: val})
    else:
        thedict.update({key_a: {key_b: val}})


def setup_logging(
        default_path='./log/config.json',
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    """Setup logging configuration
    
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


setup_logging()

logging.info('#############开始同步')
res = dict()

url = 'http://www3.nhk.or.jp/news/taiki/img/casu_asia_jp_'
tail = '.png'
folder_path = './photo/'
if os.path.exists(folder_path) == False:  # 判断文件夹是否已经存在
    os.makedirs(folder_path)  # 创建文件夹

range = ['01', '02', '03', '04', '05', '06', '07', '08', '09'] + list(range(10, 65))
try:
    for index in range:
        index = str(index)
        logging.info(url + index + tail)
        html = requests.get(url + index + tail)  # get函数获取图片链接地址，requests发送访问请求
        img_name = folder_path + index + tail
        with open(img_name, 'wb') as file:  # 以byte形式将图片数据写入
            file.write(html.content)
            file.flush()
        file.close()  # 关闭文件
        logging.info('第%s张图片下载完成' % (index))
        time.sleep(1)

        text = pytesseract.image_to_string(Image.open(img_name), lang='chi_sim')
        if text[0] != str(2):
            text = amendmentName(index, datetime.today().replace(hour=0, minute=0, second=0, microsecond=0))
        text = re.sub('\s', '', text[:22]).encode('utf-8')
        logging.info('文字分析完成:%s' % (text))
        im = Image.open(img_name)
        rgb_im = im.convert('RGB')
        rgb_im = im.convert('RGB')
        r, g, b = rgb_im.getpixel((120, 228))
        res.update({text: {'r': r, 'g': g, 'b': b}})
except Exception as e:
    logging.error(e)

json.dumps(res)
f = open('./data/res.json', 'w')
f.write(json.dumps(res, ensure_ascii=False))
f.close()

logging.info('同步完成')
