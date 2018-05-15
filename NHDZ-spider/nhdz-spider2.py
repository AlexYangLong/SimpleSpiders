# 使用Xpath抓取内容
import requests
from user_agent import get_random_useragent
from lxml import etree


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

    def parser(self, html, xpath_rule):
        doc = etree.HTML(html)
        item_list = doc.xpath(xpath_rule)
        for i, item in enumerate(item_list):
            # print(type(item), item)
            item_list[i] = [item.xpath('string(.)').strip()]
        return item_list

    def write_to_file(self, content, file_path):
        try:
            with open(file_path, 'a', encoding='utf-8') as fw:
                fw.write(content + '\n')
        except BaseException as e:
            print(e)


def main():
    spider = NHDZSpider()

    page = 1
    target_url = 'http://www.neihan8.com/article/list_5_' + str(page) + '.html'
    html = spider.download(target_url)
    # print(html)
    if html:
        dz_list = spider.parser(html, '//div[@class="f18 mb20"]')
        print(dz_list)
        for dz in dz_list:
            print(dz)
            content = dz[0].replace("\r|\t|\n|\u3000", '')
            print(content)
            spider.write_to_file(content, './dz.txt')
    else:
        print('页面下载有误！')


if __name__ == '__main__':
    main()
