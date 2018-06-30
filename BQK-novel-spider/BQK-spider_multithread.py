import threading

import requests
from lxml import etree

origin_page_url_list = []
my_lock = threading.Lock()


class NovleSpider(threading.Thread):
    def run(self):
        global origin_page_url_list
        while True:
            my_lock.acquire()
            if not origin_page_url_list:
                my_lock.release()
                break
            page_url = origin_page_url_list.pop(0)
            my_lock.release()
            html = self.download_html(page_url)
            for title, n_url in self.parse_novels_to_generator(html):
                print(title, n_url)
                path = './novels/' + title + '.txt'
                chapters_html = self.download_html(n_url)
                for chapter, c_url in self.parse_chapters_to_generator(chapters_html):
                    print(chapter, n_url + c_url)
                    content = self.parse_chapter_content(n_url + c_url)
                    self.write_to_file(path, chapter, content)

    def download_html(self, url):
        headers = {
            'Host': 'www.biqukan.net',
            # 'If-None-Match': 1530271459|
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        try:
            resp = requests.get(url=url, headers=headers)
            if resp.status_code == 200:
                return resp.text.encode('iso-8859-1').decode('gbk')
            return None
        except BaseException as e:
            print('请求失败！ %s' % e)
            return None

    def parse_novels_to_generator(self, html):
        x_html = etree.HTML(html)
        hrefs = x_html.xpath('//table/tr/td[1]/a/@href')
        titles = x_html.xpath('//table/tr/td[1]/a/@title')
        for i in range(len(hrefs)):
            yield titles[i], hrefs[i]

    def parse_chapters_to_generator(self, chapters_html):
        x_html = etree.HTML(chapters_html)
        hrefs = x_html.xpath('//div[@id="list-chapterAll"]/dl/dd/a/@href')
        chapters = x_html.xpath('//div[@id="list-chapterAll"]/dl/dd/a/@title')
        for i in range(len(hrefs)):
            yield chapters[i], hrefs[i]

    def parse_chapter_content(self, url):
        content = []
        while url:
            con_html = self.download_html(url)
            x_html = etree.HTML(con_html)
            content.extend(x_html.xpath('//div[@id="htmlContent"]/text()'))
            if x_html.xpath('//div[@id="htmlContent"]/p'):
                url = x_html.xpath('//*[@id="linkNext"]/@href')[0]
            else:
                url = ''
        return ''.join(content)

    def write_to_file(self, path, chapter, content):
        with open(path, 'a', encoding='utf-8') as fw:
            fw.write(chapter + '\n')
            fw.write(content + '\n')


# 暂时不用
# class CustomUrl(threading.Thread):
#     def run(self):
#         global novel_url_list
#         while True:
#             my_lock.acquire()
#             if not novel_url_list:
#                 my_lock.release()
#                 continue
#             novel_dict = novel_url_list.pop(0)
#             my_lock.release()
#             path = './novels/' + novel_dict.get('title') + '.txt'
#             chapters_html = self.download_html(novel_dict.get('url'))
#             for chapter, c_url in self.parse_chapters_to_generator(chapters_html):
#                 print(chapter, novel_dict.get('url') + c_url)
#                 content = self.parse_chapter_content(novel_dict.get('url') + c_url)
#                 # print(content)
#                 self.write_to_file(path, chapter, content)
#
#     def download_html(self, url):
#         headers = {
#             'Host': 'www.biqukan.net',
#             # 'If-None-Match': 1530271459|
#             'Upgrade-Insecure-Requests': '1',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
#         }
#         try:
#             resp = requests.get(url=url, headers=headers)
#             if resp.status_code == 200:
#                 return resp.text.encode('iso-8859-1').decode('gbk')
#             return None
#         except BaseException as e:
#             print('请求失败！ %s' % e)
#             return None
#
#     def parse_chapters_to_generator(self, chapters_html):
#         x_html = etree.HTML(chapters_html)
#         hrefs = x_html.xpath('//div[@id="list-chapterAll"]/dl/dd/a/@href')
#         chapters = x_html.xpath('//div[@id="list-chapterAll"]/dl/dd/a/@title')
#         for i in range(len(hrefs)):
#             yield chapters[i], hrefs[i]
#
#     def parse_chapter_content(self, url):
#         content = []
#         while url:
#             con_html = self.download_html(url)
#             x_html = etree.HTML(con_html)
#             content += x_html.xpath('//div[@id="htmlContent"]/text()')
#             try:
#                 con_html.xpath('//div[@id="htmlContent"]/p')
#                 url = con_html.xpath('//*[@id="linkNext"]/@href')
#             except:
#                 url = ''
#         return ''.join(content)
#
#     def write_to_file(self, path, chapter, content):
#         with open(path, 'w', encoding='utf-8') as fw:
#             fw.write(chapter + '\n')
#             fw.write(content + '\n')


def parse_html(html):
    x_html = etree.HTML(html)
    max_page = x_html.xpath('//ul[@id="pagelink"]/li/a[@class="last"]/text()')
    return int(max_page[0])


def download_and_parse_html(url):
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
            return parse_html(resp.text.encode('iso-8859-1').decode('gbk'))
        return 0
    except BaseException as e:
        print('请求失败！ %s' % e)
        return 0


def main():
    origin_url = 'http://www.biqukan.net/fenlei%s/%s.html'
    for i in range(1, 9):
        url = origin_url % (str(i), '1')
        max_page = download_and_parse_html(url)
        for p in range(1, max_page + 1):
            page_url = origin_url % (str(i), str(p))
            origin_page_url_list.append(page_url)
    print('origin_page_url_list_length: %d' % len(origin_page_url_list))
    ns_list = []
    for _ in range(30):
        ns = NovleSpider()
        ns_list.append(p)
        ns.start()

    for ns in ns_list:
        ns.join()


if __name__ == '__main__':
    main()
