import urllib

import os
import requests
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


def download_imgs_by_url(url):
    """根据url获得页面，并解析出图片地址"""
    html = downloader(url)
    soup = BeautifulSoup(html, 'html.parser')
    img_list = soup.find_all('img', attrs={'class': 'img-responsive lazy image_dta'})
    for img in img_list:
        img_url = img['data-original']
        print(img_url)
        if not img_url.startwith('http'):
            img_url = 'http:' + img_url
        download_img(img_url)


def download_img(img_url):
    """下载图片，保存到本地"""
    filename = img_url.split('/')[-1]
    path = os.path.join(IMG_PATH, filename)
    urllib.request.urlretrieve(img_url, filename=path)


IMG_PATH = 'images'
BASE_URL = 'http://www.doutula.com/photo/list/?page='


def main():
    # 获取最后一页的数字
    last_page_number = get_last_page_number()
    # 生成页数的生成器
    page_list = (x for x in range(1, int(last_page_number) + 1))
    for i in page_list:
        # 拼接url
        url = BASE_URL + str(i)
        # 开始下载
        download_imgs_by_url(url)


if __name__ == '__main__':
    main()

