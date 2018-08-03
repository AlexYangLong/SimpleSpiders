"""
Author：Alex Yang
Time: 2018-07-31
Target：异步检测获取的代理是否可用
Package：aiohttp
"""
import aiohttp
import asyncio
import time

from proxies_pool.db import RedisClient

VALID_STATUS_CODES = [200]
TEST_URL = 'http://www.baidu.com'
BATCH_TEST_SIZE = 100


class Tester(object):
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        """
        测试单个代理
        :param proxy: 代理
        :return: None
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('正在测试：{}'.format(proxy))
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis.max(proxy)
                        print('代理{}，可用'.format(proxy))
                    else:
                        self.redis.decrease(proxy)
                        print('代理{}，请求响应不合法'.format(proxy))
            except BaseException as e:
                print('测试出错', e)
                self.redis.decrease(proxy)
                print('代理{}，请求失败'.format(proxy))

    def run(self):
        """
        测试主函数
        :return: None
        """
        print('测试函数运行')
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            for i in range(0, len(proxies), BATCH_TEST_SIZE):
                test_proxies = proxies[i: i+BATCH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except BaseException as e:
            print('测试器发生错误', e)
