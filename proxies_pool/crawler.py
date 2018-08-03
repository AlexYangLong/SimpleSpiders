"""
Author：Alex Yang
Time: 2018-07-29
Target：使用redis存储爬取的代理
Package：redis
"""

import json

from pyquery import PyQuery as pq

from proxies_pool.utils import get_page


class ProxyMetaClass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaClass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval('self.{}()'.format(callback)):
            print('成功获取到代理：{}'.format(proxy))
            proxies.append(proxy)
        return proxies

    def crawl_89ip(self, page_count=5):
        """
        获取89ip代理
        :param page_count: 页码
        :return: 代理
        """
        base_url = 'http://www.89ip.cn/index_{}.html'
        urls = [base_url.format(i) for i in range(1, page_count + 1)]
        for url in urls:
            print('正在爬取{}的代理'.format(url))
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc.find('.layui-form table tr').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    # def crawl_proxy360(self):
    #     """
    #     获取proxy360的代理
    #     :return: 代理
    #     """
    #     base_url = 'http://www.proxy360.cn/Region/China'
    #     print('正在爬取{}的代理'.format(base_url))

