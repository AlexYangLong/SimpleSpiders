"""
Author：Alex Yang
Time: 2018-07-28
Target：使用redis存储爬取的代理
Package：redis
"""

import redis
from random import choice

MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = None
STORE_KEY = 'proxies'


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化
        :param host: Redis地址
        :param port: Redis端口
        :param password: Redis密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理，设置初始分数
        :param proxy: 代理
        :param score: 分数
        :return: 添加的结果
        """
        if not self.db.zscore(STORE_KEY, proxy):
            return self.db.zadd(STORE_KEY, score, proxy)

    def random(self):
        """
        随机获取有效代理，首先尝试获取最高分数的代理，如果不存在，则按照排序来获取，不存在返回None
        :return: 代理
        """
        results = self.db.zrangebyscore(STORE_KEY, MAX_SCORE, MAX_SCORE)
        if len(results):
            return choice(results)
        else:
            results = self.db.zrevrange(STORE_KEY, MIN_SCORE, MAX_SCORE)
            if len(results):
                return choice(results)
            else:
                return None

    def decrease(self, proxy):
        """
        代理的分数递减一分，当分数小于最小值，删除
        :param proxy: 代理
        :return: 修改后的代理的分数
        """
        score = self.db.zscore(STORE_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理：{}，当前分数{}，减1'.format(proxy, score))
            return self.db.zincrby(STORE_KEY, proxy, -1)
        else:
            print('代理：{}，当前分数{}，移除'.format(proxy, score))
            return self.db.zrem(STORE_KEY, proxy)

    def exist(self, proxy):
        """
        判断代理是否存在
        :param proxy: 代理
        :return: 是否存在
        """
        return not self.db.zscore(STORE_KEY, proxy) == None

    def max(self, proxy):
        """
        将代理设置为最大分数
        :param proxy: 代理
        :return: 设置结果
        """
        print('代理：{}，可用，分数设置为：{}'.format(proxy, MAX_SCORE))
        return self.db.zadd(STORE_KEY, MAX_SCORE, proxy)

    def count(self):
        """
        获取redis中代理的数量
        :return: 代理的数量
        """
        return self.db.zcard(STORE_KEY)

    def all(self):
        """
        返回所有代理
        :return: 所有代理的列表
        """
        return self.db.zrangebyscore(STORE_KEY, MIN_SCORE, MAX_SCORE)
