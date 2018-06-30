import threading

import requests
import time
from lxml import etree

chapters_title_list = []
chapters_url_list = []
novel_name = ''
my_lock = threading.Lock()


class Utils(object):
    @staticmethod
    def download_html(url):
        headers = {
            'Host': 'www.biqukan.net',
            # 'If-None-Match': 1530271459|
            'Referer': 'http://www.biqukan.net/fenlei1/1.html',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        try:
            resp = requests.get(url=url, headers=headers)
            if resp.status_code == 200:
                return resp.text.encode('iso-8859-1').decode('gbk')
            return None
        except BaseException as e:
            print(e)
            return None

    @staticmethod
    def parse_html(html, pattern):
        x_html = etree.HTML(html)
        return x_html.xpath(pattern)


class CustomUrl(threading.Thread):
    def __init__(self, novel_url):
        super(CustomUrl, self).__init__()
        self.novel_url = novel_url

    def run(self):
        global chapters_url_list
        global chapters_title_list
        while True:
            my_lock.acquire()
            if not chapters_url_list:
                my_lock.release()
                break
            chapter_url = chapters_url_list.pop(0)
            chapter_title = chapters_title_list.pop(0)
            try:
                content = self.download_and_parse(self.novel_url + chapter_url)
                path = './novels/' + novel_name + '.txt'
                self.write_to_file(path, chapter_title, content)
                print('%s: %s 下载保存成功' %(chapter_title, self.novel_url + chapter_url))
            except:
                print('%s: %s 下载失败' % (chapter_title, self.novel_url + chapter_url))
            my_lock.release()
            time.sleep(0.05)

    def download_and_parse(self, url):
        content = []
        while url:
            con_html = Utils.download_html(url=url)
            content.extend(Utils.parse_html(html=con_html, pattern='//div[@id="htmlContent"]/text()'))
            if Utils.parse_html(html=con_html, pattern='//div[@id="htmlContent"]/p'):
                url = Utils.parse_html(html=con_html, pattern='//*[@id="linkNext"]/@href')[0]
            else:
                url = ''
        return ''.join(content)

    def write_to_file(self, path, chapter, content):
        with open(path, 'a', encoding='utf-8') as fw:
            fw.write(chapter + '\n')
            fw.write(content)


def main():
    novel_url = 'http://www.biqukan.net/book/80265/'
    html = Utils.download_html(url=novel_url)
    global chapters_url_list, chapters_title_list, novel_name
    chapters_url_list = Utils.parse_html(html=html, pattern='//div[@id="list-chapterAll"]/dl/dd/a/@href')
    chapters_title_list = Utils.parse_html(html=html, pattern='//div[@id="list-chapterAll"]/dl/dd/a/@title')
    novel_name = Utils.parse_html(html=html, pattern='/html/body/div[2]/div[1]/div/div/div[2]/h1/text()')[0]
    print(novel_name)
    print(chapters_url_list)
    print(len(chapters_url_list), len(chapters_title_list))

    c_list = []
    for _ in range(10):
        c = CustomUrl(novel_url)
        c_list.append(c)
        c.start()
    for c in c_list:
        c.join()


if __name__ == '__main__':
    main()
