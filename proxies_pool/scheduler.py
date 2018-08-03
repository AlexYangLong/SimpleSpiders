"""
Author：Alex Yang
Time: 2018-07-31
Target：调度器，调度各个模块
Package：
"""
from multiprocessing import Process

import time

from proxies_pool.getter import Getter
from proxies_pool.proxy_api import app
from proxies_pool.tester import Tester

TESTER_CYCLE = 20
GETTER_CYCLE = 20
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True


class Scheduler(object):
    def scheduler_tester(self, cycle=TESTER_CYCLE):
        tester = Tester()
        while True:
            print('测试器开始运行')
            tester.run()
            time.sleep(cycle)

    def scheduler_getter(self, cycle=GETTER_CYCLE):
        getter = Getter()
        while True:
            print('抓取器开始抓取')
            getter.run()
            time.sleep(cycle)

    def scheduler_api(self):
        app.run(host='127.0.0.1', port=5000)

    def run(self):
        print('代理池开始运行')

        if GETTER_ENABLED:
            getter_process = Process(target=self.scheduler_getter)
            getter_process.start()
        if TESTER_ENABLED:
            tester_process = Process(target=self.scheduler_tester)
            tester_process.start()
        if API_ENABLED:
            api_process = Process(target=self.scheduler_api)
            api_process.start()

        if GETTER_ENABLED:
            getter_process.join()
        if TESTER_ENABLED:
            tester_process.join()
        if API_ENABLED:
            api_process.join()


if __name__ == '__main__':
    Scheduler().run()
