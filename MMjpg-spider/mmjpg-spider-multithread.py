"""
多线程爬取MMJPG网页的图片，并将图片的url保存到MongoDB
"""

import threading

import requests
import time
from lxml import etree
from pymongo import MongoClient

from user_agent import get_random_useragent


origin_url_list = []
data_url_list = []
my_lock = threading.Lock()

client = MongoClient('mongodb://127.0.0.1:27017')
db = client['mmjpg']
collection = db['mn_img_url']


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
                my_lock.acquire()
                data = dict({'mn_id': mn_id})
                data_list = []
                for i in range(len(keys_list)):
                    img_url = img_origin_url % (mn_id, str(i + 1) + 'i' + keys_list[i])
                    data_list.append(img_url)
                data['imgs_list'] = data_list
                self.save_to_db(data)
                my_lock.release()
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

    def save_to_db(self, data):
        collection.insert_one(data)


def main():
    target_url = 'http://www.mmjpg.com/'

    origin_url_list.append(target_url)
    origin_url_list.extend([target_url+'home/'+str(i) for i in range(2, 11)])
    # print(origin_url_list)
    # html = download(target_url)
    # parse_html(html.encode('ISO-8859-1').decode('utf-8'))

    p_list = []
    for _ in range(5):
        p = ProductUrl()
        p_list.append(p)
        p.start()

    c_list = []
    for _ in range(10):
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
