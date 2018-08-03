"""
Author：Alex Yang
Time: 2018-07-28
Target：爬取淘宝搜索页前几页iPad相关的数据
Package：selenium、pyquery、urllib.parse、pymongo
"""
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pyquery import PyQuery as pq
import pymongo

MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DB = 'taobaoDB'
MONGODB_COLLECTION = 'ipad'

MAX_PAGE = 5
KEY_WOED = 'iPad'


chrome_driver = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
browser = webdriver.Chrome(chrome_driver)
wait = WebDriverWait(browser, 5)


def start_crawl(page):
    print('正在爬取第{}页'.format(page))

    url = 'https://s.taobao.com/search?q=' + quote(KEY_WOED)
    try:
        browser.get(url=url)
        if page > 1:
            input_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
            input_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
            input_box.clear()
            input_box.send_keys(page)
            input_btn.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .m-itemlist .items .item')))
        get_products()
    except BaseException as e:
        print(e)
        start_crawl(page)
    print('爬取解析成功')


def get_products():
    html = pq(browser.page_source)
    items = html('#mainsrp-itemlist .m-itemlist .items .item').items()
    for item in items:
        product = {
            # 'id': item.find('.pic .img').attr('id').split('_')[-1],
            'img': 'https:' + item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text().replace('\n', ''),
            'deal_num': item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        # print(product)
        save_to_db(product)


conn = pymongo.MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)
db = conn[MONGODB_DB]


def save_to_db(product):
    try:
        print(product)
        # db[MONGODB_COLLECTION].update({'title': product['title']}, {'$set': product}, upsert=True)
        db[MONGODB_COLLECTION].insert(product)
        print('存储成功')
    except BaseException as e:
        print(e)
        print('存储失败')


def main():
    for i in range(1, MAX_PAGE + 1):
        start_crawl(i)
    browser.quit()
    conn.close()


if __name__ == '__main__':
    main()
