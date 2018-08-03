"""
Author：Alex Yang
Time: 2018-07-30
Target：动态调用所有以 crawl 开头的方法
Package：
"""

from .db import RedisClient
from .crawler import Crawler


POOL_MAX_THRESHOLD = 1000


class Getter(object):
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        """
        判断是否达到代理池的最大值
        :return: 布尔值
        """
        if self.redis.count() > POOL_MAX_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print('开始获取')
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.redis.add(proxy)
