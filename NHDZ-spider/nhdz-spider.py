# 使用正则抓取内容
import re
import requests
from user_agent import get_random_useragent


class NHDZSpider(object):

    def download(self, url):
        try:
            headers = {
                'User-Agent': get_random_useragent()
            }
            resp = requests.get(url, headers=headers)
            if resp.status_code == 200:
                return resp.text.encode('ISO-8859-1').decode('gbk')
            else:
                return None
        except BaseException as e:
            print(e)
            return None

    def parser(self, html, regex):
        pattern = re.compile(regex, re.S)
        item_list = pattern.findall(html)
        return item_list

    def write_to_file(self, content, file_path):
        try:
            with open(file_path, 'a', encoding='utf-8') as fw:
                fw.write(content)
        except BaseException as e:
            print(e)


def main():
    spider = NHDZSpider()

    page = 1
    target_url = 'http://www.neihan8.com/article/list_5_' + str(page) + '.html'
    html = spider.download(target_url)
    # print(html)
    if html:
        dz_list = spider.parser(html, '<div class="f18 mb20">(.*?)</div>')
        for dz in dz_list:
            content = dz.replace("<p>", '').replace("</p>", '').replace("<br />", '').replace('\xa0', '')
            spider.write_to_file(content, './dz.txt')
            # print()
    else:
        print('页面下载有误！')


if __name__ == '__main__':
    main()
