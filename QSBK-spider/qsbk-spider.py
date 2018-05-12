from user_agent import get_random_useragent
import requests
from bs4 import BeautifulSoup


class HtmlDownloader(object):
    """下载器"""
    def download(self, session, url, referer=None):
        print(session.cookies.get_dict())
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'www.qiushibaike.com',
            'User-Agent': get_random_useragent()
        }

        if referer:
            headers['Referer'] = referer

        try:
            resp = session.get(url, headers=headers)
            return resp.text
        except BaseException as e:
            print('请求失败！爬取失败！', e)
            return None


class HtmlParser(object):
    """解析器"""

    def get_content_urls(self, server_url, html):
        """
        根据页面解析出每个joke的url
        :param server_url: server_url
        :param html: HTML string
        :return: list
        """
        urls = []
        soup = BeautifulSoup(html, 'html.parser')
        jokes_as = soup.find_all('a', class_='contentHerf')
        for a in jokes_as:
            urls.append(server_url + a.get('href'))

        return urls

    def get_data_content(self, html):
        """
        根据页面解析出joke的内容
        :param html: HTML string
        :return: content string
        """
        soup = BeautifulSoup(html, 'html.parser')
        joke_content = soup.find('div', class_='content') if soup.find('div', class_='content') \
            else soup.find('div', class_='content-text')

        if joke_content:
            return joke_content.get_text()
        else:
            return None


class SpiderMain(object):
    """主程序"""
    def __init__(self, target_url, server_url, page=1):
        if page == 1:
            self.target_url = target_url
        else:
            self.target_url = target_url + 'page/' + str(page) + '/'
        self.server_url = server_url

        self.content_urls = []

        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()

    def craw(self):
        session = requests.session()
        session.get(self.server_url)
        print(session.cookies.get_dict())
        html_content = self.downloader.download(session, self.target_url, self.target_url)
        if html_content:
            self.content_urls = self.parser.get_content_urls(self.server_url, html_content)
            print('urls count:', len(self.content_urls))
            for i, url in enumerate(self.content_urls):
                print('craw %d: %s' % ((i + 1), url))
                html_content = self.downloader.download(session, url, self.target_url)
                data_content = self.parser.get_data_content(html_content)
                print(data_content)
        else:
            print('爬去失败！')


def main():
    target_url = 'https://www.qiushibaike.com/text/'
    page = 1
    server_url = 'https://www.qiushibaike.com'

    spider = SpiderMain(target_url, server_url, page)
    spider.craw()


if __name__ == '__main__':
    main()
