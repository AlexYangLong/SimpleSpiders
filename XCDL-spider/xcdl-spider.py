import urllib
import urllib.request
import time

import requests
from lxml import etree
from bs4 import BeautifulSoup

from user_agent import get_random_useragent


def download(url):
    headers = {
        'Host': 'www.xicidaili.com',
        'Referer': 'http://www.xicidaili.com/',
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


def parse_html(html):
    # print(html)
    # x_html = etree.HTML(html)
    # ip_list = x_html.xpath('//*[@id="ip_list"]/tbody/tr/td[2]/text()')
    # port_list = x_html.xpath('//*[@id="ip_list"]/tbody/tr/td[3]/text()')
    # type_list = x_html.xpath('//*[@id="ip_list"]/tbody/tr/td[6]/text()')

    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table', attrs=({'id': 'ip_list'}))
    alltr = table.find_all('tr')[1:]
    proxy_list = []
    for tr in alltr:
        alltd = tr.find_all('td')
        ip = alltd[1].get_text()
        port = alltd[2].get_text()
        type_ = alltd[5].get_text()

        # print('{}://{}:{}'.format(type_, ip, port))
        proxy_list.append('{}://{}:{}'.format(type_, ip, port))

    return proxy_list


def validate_ip(proxy):
    headers = {
        'User-Agent': get_random_useragent()
    }
    # 代理设置
    proxy_handler = urllib.request.ProxyHandler({'http': proxy})
    opener = urllib.request.build_opener(proxy_handler)
    urllib.request.install_opener(opener)

    # 请求网址
    validateUrl = 'https://www.baidu.com'
    req = urllib.request.Request(url=validateUrl, headers=headers)
    # 延时,等待反馈结果
    time.sleep(4)

    #判断结果
    try:
        res = urllib.request.urlopen(req)
        # 延时,等待反馈结果
        time.sleep(2)
        content = res.read()
        # 写入文件
        if content and res.status == 200:
            print('%s is ok' % proxy)
            write('./proxy.txt', proxy)
        else:
            # 未通过
            print('%s is not ok' % proxy)
    except urllib.request.URLError as e:
        print('%s error %s' % (proxy, e.reason))

# 写入文档
def write(path, text):
    with open(path, 'a', encoding='utf-8') as f:
        f.writelines(text)
        f.write('\n')
# 清空文档
def truncatefile(path):
    with open(path, 'w', encoding='utf-8') as f:
        f.truncate()
# 读取文档
def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        txt = []
        for s in f.readlines():
            txt.append(s.strip())
    return txt


def main():
    proxy_list = []
    for i in range(10):
        xc_url = 'http://www.xicidaili.com/wt/%s' % str(i + 1)
        html = download(url=xc_url)
        proxy_list.extend(parse_html(html=html))

    print(proxy_list)
    print(len(proxy_list))

    # proxy_list = [
    #     'http://106.56.102.131:8070',
    #     'http://221.228.17.172:8181',
    #     'http://124.89.2.250:63000',
    #     'http://101.236.19.165:8866',
    #     'http://125.121.116.43:808',
    #     'http://223.145.229.165:666',
    #     'http://182.88.14.206:8123',
    #     'http://183.128.240.76:666',
    #     'http://117.86.9.145:18118'
    # ]

    # 验证ip是否可用
    for proxy in proxy_list:
        validate_ip(proxy)


if __name__ == '__main__':
    main()