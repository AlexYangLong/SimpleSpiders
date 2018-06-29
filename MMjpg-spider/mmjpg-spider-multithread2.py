"""
多线程爬取MMJPG网页的图片，并将图片保存到本地
"""

import threading

import os
import requests
import time
from lxml import etree
from pymongo import MongoClient

from user_agent import get_random_useragent


origin_url_list = []
data_url_list = []
my_lock = threading.Lock()


class ProductUrl(threading.Thread):

    def run(self):
        global origin_url_list
        global data_url_list
        while True:
            my_lock.acquire()
            if not origin_url_list:
                my_lock.release()
                break
            url = origin_url_list.pop(0)
            my_lock.release()
            html = self.download(url=url)
            if html:
                href_list = self.parse_html(html=html.encode('ISO-8859-1').decode('utf-8'))
                my_lock.acquire()
                data_url_list.extend(href_list)
                my_lock.release()
            time.sleep(0.05)

    def download(self, url):
        headers = {
            'Host': 'www.mmjpg.com',
            'Referer': 'http://www.mmjpg.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_useragent()
        }

        try:
            resp = requests.get(url=url, headers=headers)
            if resp.status_code == 200:
                return resp.text
            return None
        except BaseException as e:
            print(e)
            return None

    def parse_html(self, html):
        x_html = etree.HTML(html)
        pattern = '//div[@class="pic"]/ul/li/a/@href'
        return x_html.xpath(pattern)


class CustomUrl(threading.Thread):

    def run(self):
        global data_url_list
        while True:
            my_lock.acquire()
            if not data_url_list:
                my_lock.release()
                continue
            url = data_url_list.pop(0)
            my_lock.release()
            mn_id = url.split('/')[-1]
            img_key_url = 'http://www.mmjpg.com/data.php?id=%s&page=8999' % mn_id
            keys = self.download(img_key_url, url)
            if keys:
                img_origin_url = 'http://fm.shiyunjj.com/2018/%s/%s.jpg'
                keys_list = keys.split(',')
                for i in range(len(keys_list)):
                    img_url = img_origin_url % (mn_id, str(i + 1) + 'i' + keys_list[i])
                    dir_path = './mm/' + mn_id
                    if not os.path.exists(dir_path):
                        os.mkdir(dir_path)
                    img_path = os.path.join(dir_path, str(i + 1) + 'i' + keys_list[i] + '.jpg')
                    self.download_img(img_url, img_path)
            time.sleep(0.05)

    def download(self, url, referer):
        headers = {
            'Host': 'www.mmjpg.com',
            'Referer': referer,
            'User-Agent': get_random_useragent()
        }

        try:
            resp = requests.get(url=url, headers=headers)
            if resp.status_code == 200:
                return resp.text
            return None
        except BaseException as e:
            print(e)
            return None

    def download_img(self, url, img_save_path):
        headers = {
            'Referer': 'http://www.mmjpg.com/mm/1334',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        try:
            resp = requests.get(url=url, headers=headers)
            if resp.status_code == 200:
                self.save_to_file(resp.content, img_save_path)
                print('%s 下载保存成功' % url)
            else:
                print('%s 下载错误' % url)
        except BaseException as e:
            print(e)
            print('%s 请求错误' % url)

    def save_to_file(self, content, path):
        with open(path, 'wb') as fw:
            fw.write(content)


def main():
    target_url = 'http://www.mmjpg.com/'

    origin_url_list.append(target_url)
    origin_url_list.extend([target_url+'home/'+str(i) for i in range(2, 11)])
    # print(origin_url_list)
    # html = download(target_url)
    # parse_html(html.encode('ISO-8859-1').decode('utf-8'))

    p_list = []
    for _ in range(10):
        p = ProductUrl()
        p_list.append(p)
        p.start()

    c_list = []
    for _ in range(20):
        c = CustomUrl()
        c_list.append(c)
        c.start()

    for p in p_list:
        p.join()
    for c in c_list:
        c.join()

    # print(img_url_list)
    # print(len(img_url_list))


if __name__ == '__main__':
    main()
