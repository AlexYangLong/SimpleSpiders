import json
from multiprocessing import Pool

import re

import os
import requests
from requests.exceptions import RequestException

from user_agent import get_random_useragent


def downloader(url):
    """下载页面"""
    headers = {
        'Host': 'maoyan.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': get_random_useragent()
    }
    try:
        resp = requests.get(url=url, headers=headers)
        if resp.status_code == 200:
            return resp.text
        return None
    except RequestException as e:
        print('请求 %s 失败' % url)
        print(e)
        return None


def parse_page(html):
    """解析页面，返回字典"""
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?class="name">'
                         '<a.*?>(.*?)</a></p>.*?class="star">(.*?)</p>.*?class="releasetime">'
                         '(.*?)</p>.*?class="integer">(.*?)</i>.*?class="fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    # print(items)
    for item in items:
        yield {
            'index': item[0].strip(),
            'image': item[1].strip(),
            'title': item[2].strip(),
            'actors': item[3].strip()[3:],
            'show_time': item[4].strip()[5:],
            'score': item[5].strip() + item[6].strip()
        }


def write_to_file(content):
    """将获取的信息保存到文件"""
    with open('result.txt', 'a', encoding='utf-8') as fw:
        fw.write(json.dumps(content, ensure_ascii=False) + '\n')


def save_movie_img(url, path):
    """保存电影封面"""
    resp = requests.get(url)
    if resp.status_code == 200:
        with open(path, 'wb') as fw:
            fw.write(resp.content)


def main(offset):
    target_url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = downloader(target_url)
    # print(html)

    for movie in parse_page(html):
        print(movie)
        write_to_file(movie)
        # 封面文件夹不存在则创建
        dir_path = './covers/' + movie['title']
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        save_movie_img(movie['image'], './covers/' + movie['title'] + '/' + movie['title'] + '.jpg')


if __name__ == '__main__':
    # main(0)
    pool = Pool()
    pool.map(main, [i * 10 for i in range(10)])