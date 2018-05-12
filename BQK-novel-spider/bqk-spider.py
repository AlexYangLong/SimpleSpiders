import re
import requests
# from requests import exceptions
from bs4 import BeautifulSoup
from user_agent import get_random_useragent


class HtmlDownloader(object):
    """下载器"""

    def download(self, url):
        """
        根据url下载页面
        :param url: url
        :return: html string
        """
        try:
            headers = {
                'User-Agent': get_random_useragent()
            }
            resp = requests.get(url, headers=headers)
            return resp.text
        except BaseException as e:
            print(e)
            return None


class HtmlParser(object):
    """解析器"""

    def parse_to_chapters(self, server_url, html):
        """
        解析出html中的所有章节名及其对应的url
        :param server_url: server_url
        :param html: html string
        :return: urls, names
        """
        urls = []
        names = []
        div_soup = BeautifulSoup(html, 'html.parser')
        all_a = div_soup.find('div', class_='listmain').find_all('a')
        # all_a = div.find_all('a')
        for a in all_a[12:]:
            names.append(a.string)
            urls.append(server_url + a.get('href'))
        # for a in all_a[:12]:
        #     names.append(a.string)
        #     urls.append(server_url + a.get('href'))
        return urls, names

    def parse_to_content(self, html):
        """
        解析出html页面的章节的内容
        :param html: html string
        :return: content
        """
        div_soup = BeautifulSoup(html, 'html.parser')
        div = div_soup.find('div', id='content')
        # 将不需要的字符替换掉  # content = div.text.replace('\xa0' * 8, '\n\n')
        content = div.text.replace('\xa0' * 8, '\n\n')
        content = re.sub(r'&1t;/p>|&1t;|tab1e  sty1e="idth:1oo%;  text-a1ign:netter;">|tr>|td>|/tab1e>', '', content)
        return content


class WriteFile(object):
    """书写器"""

    def write_to_file(self,chapter_name, chapter_content, path):
        """
        将章节名和对应的内容写到文件中
        :param chapter_name: chapter_name
        :param chapter_content: chapter_content
        :param path: path
        :return: written results
        """
        try:
            with open(path, 'a', encoding='utf-8') as fw:
                fw.write(chapter_name + '\n')
                fw.writelines(chapter_content)
                fw.write('\n\n')
                return '%s written successful!' % chapter_name
        except BaseException as e:
            return '%s written failed! reason: %s' % (chapter_name, e)


class SpiderMain(object):
    """主程序"""
    def __init__(self, server_url, target_url, file_path):
        self.server_url = server_url  # 服务器地址
        self.target_url = target_url  # 目标地址
        self.chapter_names = []  # 用于存放章节名
        self.chapter_urls = []  # 用于存放章节对应的url
        self.chapter_num = 0  # 章节总数
        self.file_path = file_path  # 保存路径

        # self.url_manager = UrlManager()
        self.html_downloader = HtmlDownloader()  # 下载器
        self.html_parser = HtmlParser()  # 解析器
        self.write_file = WriteFile()  # 书写器

    def craw(self):
        """爬数据"""
        chapter_content = self.html_downloader.download(self.target_url)
        if chapter_content:
            self.chapter_urls, self.chapter_names = self.html_parser.parse_to_chapters(self.server_url, chapter_content)
            self.chapter_num = len(self.chapter_urls)
            print('共%d章' % self.chapter_num)
            for i in range(self.chapter_num):
                new_url = self.chapter_urls[i]
                print('craw %d: %s %s' % ((i+1), new_url, self.chapter_names[i]))

                html_content = self.html_downloader.download(new_url)
                if html_content:
                    chapter_content = self.html_parser.parse_to_content(html_content)
                    res = self.write_file.write_to_file(self.chapter_names[i], chapter_content, self.file_path)
                    print(res)
                else:
                    print('%s 章节下载失败！' % self.chapter_names[i])
        else:
            print('小说下载失败！')


def main():
    server_url = 'http://www.biqukan.com'
    target_url = 'http://www.biqukan.com/1_1452/'
    file_path = './novels/hahaha.txt'

    spider = SpiderMain(server_url, target_url, file_path)
    spider.craw()


if __name__ == '__main__':
    main()
