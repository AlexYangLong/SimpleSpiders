import json
from hashlib import md5
from multiprocessing import Pool
from urllib.parse import urlencode

import re

import os
import requests
from bs4 import BeautifulSoup


def downloader(url):
    """根据url下载资源"""
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp
        return None

    except BaseException as e:
        print('请求失败！' + e)
        return None


# def downloader_detail(url):
#     try:
#         resp = requests.get(url, allow_redirects=False)
#         if resp.status_code == 200:
#             return resp.text
#         elif resp.status_code == 301:
#             print(resp.url)
#             downloader_detail(resp.url)
#         return None
#
#     except BaseException as e:
#         print('请求详情页失败！' + e)
#         return None


def parse_listpage_data(html):
    """解析列表页，是一个生成器"""
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')


def parse_detailpage_data(content, url):
    """解析详情页，并下载图片，返回一个包含图片url的字典"""
    soup = BeautifulSoup(content, 'html.parser')
    title = soup.select('title')[0].get_text()
    # print(title)
    img_pattern = re.compile(r'gallery: JSON.parse\("(.*?)"\),', re.S)
    res = re.search(img_pattern, content)
    # print(res.group(1).replace('\\', ''))
    if res:
        # 使用正则匹配的字符串中包含了很多 \ 转义，所以用空白符替换
        data = json.loads(res.group(1).replace('\\', ''))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            # 下载图片
            for img in images:
                content = downloader(img).content
                if content:
                    print('正在下载 %s' % img)
                    save_to_file(content, title)
                    print('保存成功')
            return {
                'url': url,
                'title': title,
                'images': images
            }


def save_to_file(content, title):
    dir_path = './images/%s' % title
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    file_path = dir_path + '/%s.%s' % (md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as fw:
            fw.write(content)


def main(offset):
    # offset = 0
    keyword = '街拍'
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 1,
        'from': 'search_tab'
    }
    target_url = 'https://www.toutiao.com/search_content/?' + urlencode(data)

    html = downloader(target_url).text
    # print(html)

    for url in parse_listpage_data(html):
        if url:
            url = 'https://www.toutiao.com/a' + url.split('/')[-2] + '/'
            print(url)
            content = downloader(url).text
            # print(content)
            if content:
                res = parse_detailpage_data(content, url)
                print(res)


if __name__ == '__main__':
    # main()
    # 使用多进程下载（进程池）
    groups = [x * 20 for x in range(10)]
    pool = Pool()
    pool.map(main, groups)