import os
import requests
from bs4 import BeautifulSoup
from user_agent import get_random_useragent


class HtmlDownloader(object):
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.mmjpg.com',
            'Referer': 'http://www.mmjpg.com/',
            'Upgrade-Insecure-Requests': '1'
        }

    def download(self, url, referer):
        # self.headers['User-Agent'] = get_random_useragent()
        self.headers['Referer'] = referer
        resp = requests.get(url, headers=self.headers)
        print(resp.status_code)
        if resp.status_code == 200:
            return resp.text.encode('ISO-8859-1').decode('utf-8')
        else:
            return None

    def download_img(self, url, referer):
        # self.headers['User-Agent'] = get_random_useragent()
        self.headers['Referer'] = referer
        self.headers['Host'] = 'img.mmjpg.com'
        resp = requests.get(url, headers=self.headers)
        print(resp.status_code)
        if resp.status_code == 200:
            return resp.content
        else:
            return None


class HtmlParser(object):

    def get_urls(self, html):
        if not html:
            return None
        else:
            names = []
            urls = []
            soup = BeautifulSoup(html, 'html.parser')
            spans = soup.find_all('span', class_='title')
            for span in spans:
                a = span.find('a')
                # print(a.string)
                urls.append(a.get('href'))
                names.append(a.string)
            return names, urls

    def get_content_urls(self, html, server_url):
        if not html:
            return None
        else:
            content_urls = []
            soup = BeautifulSoup(html, 'html.parser')
            all_a = soup.find('div', id='page').find_all('a')
            last = int(all_a[-2].string)
            url = all_a[-2].get('href')[:all_a[-2].get('href').rfind('/') + 1]
            # print(url)
            for i in range(1, last + 1):
                content_urls.append(server_url + url + str(i))
            return content_urls

    def get_img_url(self, html):
        if not html:
            return None
        else:
            soup = BeautifulSoup(html, 'html.parser')
            div = soup.find('div', class_='content')
            mm_img_url = div.a.img.get('src')
            return mm_img_url


class HtmlOutputer(object):
    def __init__(self):
        self.downloader = HtmlDownloader()

    def write_to_file(self, path, mm_url, referer):
        print(path, mm_url)
        content = self.downloader.download_img(mm_url, referer)
        print(content)
        if not content:
            return None
        else:
            try:
                with open(path, 'wb') as fw:
                    fw.write(content)
            except:
                print('%s 下载出错' % mm_url)


class SpiderMain(object):
    def __init__(self, server_url, target_url, page):
        self.server_url = server_url
        if page == 1:
            self.target_url = server_url
        else:
            self.target_url = target_url + str(page)
        self.path = './mm/'

        self.names = []
        self.urls = []
        self.content_urls = []

        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.outputer = HtmlOutputer()

    def craw(self):
        referer = self.server_url
        html_content = self.downloader.download(self.target_url, referer)
        self.names, self.urls = self.parser.get_urls(html_content)
        print(self.urls)
        for i in range(len(self.urls)):
            filepath = self.path + self.names[i]
            self.mkdir(filepath)
            print('craw %s: %s' % (self.names[i], self.urls[i]))

            html_content = self.downloader.download(self.urls[i], referer)
            self.content_urls = self.parser.get_content_urls(html_content, self.server_url)
            print('%s 的所有页urls %s' % (self.names[i], self.content_urls))
            for j in range(len(self.content_urls)):
                if j == 0:
                    referer = self.server_url
                elif j == 1:
                    referer = self.urls[i]
                else:
                    referer = self.content_urls[j - 1]
                html_content = self.downloader.download(self.content_urls[j], referer)
                mm_img_url = self.parser.get_img_url(html_content)
                print('downloading %s' % mm_img_url)

                filename = filepath + '/' + str(j + 1) + '.jpg'
                self.outputer.write_to_file(filename, mm_img_url, self.server_url)

    def mkdir(self, path):
        if not os.path.exists(path):
            os.mkdir(path)


def main():
    target_url = 'http://www.mmjpg.com/home/'
    page = 1
    server_url = 'http://www.mmjpg.com'

    spider = SpiderMain(server_url, target_url, page)
    spider.craw()


if __name__ == '__main__':
    main()
