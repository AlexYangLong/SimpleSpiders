import urllib
import threading

import os
import requests
import time
from bs4 import BeautifulSoup


def downloader(url):
    """下载页面"""
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.text
    except BaseException as e:
        print(e)
    return None


def get_last_page_number():
    """解析出最后一页的数字"""
    url = 'http://www.doutula.com/photo/list/'
    html_content = downloader(url)
    # print(html_content)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        last_page_li = soup.find('ul', class_='pagination').find_all('li')[-2]
        # print(last_page_li)
        return last_page_li.text


def download_imgs_by_url():
    """根据url获得页面，并解析出图片地址"""
    while True:
        lock.acquire()
        if len(PAGE_URL) == 0:
            lock.release()
            continue
        url = PAGE_URL.pop()
        lock.release()
        print(url)
        html = downloader(url)
        soup = BeautifulSoup(html, 'html.parser')
        img_list = soup.find_all('img', attrs={'class': 'img-responsive lazy image_dta'})
        lock.acquire()
        for img in img_list:
            img_url = img['data-original']
            if not img_url.startswith('http'):
                img_url = 'http:' + img_url
            IMG_URL.append(img_url)
        lock.release()
        # 没下载一页就休息1秒
        time.sleep(1)


def download_img():
    """下载图片，保存到本地"""
    while True:
        lock.acquire()
        if len(IMG_URL) == 0:
            lock.release()
            continue
        img_url = IMG_URL.pop()
        lock.release()
        filename = img_url.split('/')[-1]
        path = os.path.join(IMG_PATH, filename)
        urllib.request.urlretrieve(img_url, filename=path)


IMG_PATH = 'images'
BASE_URL = 'http://www.doutula.com/photo/list/?page='
PAGE_URL = []
IMG_URL = []
lock = threading.Lock()


def main():
    # 获取最后一页的数字
    last_page_number = get_last_page_number()
    # 生成页数的生成器
    page_list = (x for x in range(1, int(last_page_number) + 1))
    for i in page_list:
        # 拼接url
        url = BASE_URL + str(i)
        # 拼接后，加入PAGE_URL
        PAGE_URL.append(url)

    # 使用多线程下载
    # 使用3个线程从PAGE_URL中取出页面地址，下载图片的地址，并放入IMG_URL中
    for _ in range(3):
        threading.Thread(target=download_imgs_by_url).start()

    # 使用5个线程从IMG_URL去除图片地址，并下载图片
    for _ in range(5):
        threading.Thread(target=download_img).start()


if __name__ == '__main__':
    main()