import requests
from bs4 import BeautifulSoup
from user_agent import get_random_useragent
import  json


class TXSZSpider(object):
    def download(self, url):
        try:
            headers = {
                'User-Agent': get_random_useragent(),
            }
            resp = requests.get(url, headers=headers)
            if resp.status_code == 200:
                return resp.text
            else:
                return None
        except BaseException as e:
            print(e)
            return None

    def parser(self, html):
        soup = BeautifulSoup(html, 'lxml')
        trs = soup.select('table[class="tablelist"] tr[class="even"], table[class="tablelist"] tr[class="odd"]')
        # print(trs)
        item_list = []
        for tr in trs:
            item = {}

            item['name'] = tr.select('td a')[0].get_text()
            item['detail_url'] = tr.select('td a')[0].get('href')
            item['catalog'] = tr.select('td')[1].get_text()
            item['wanted_num'] = tr.select('td')[2].get_text()
            item['work_location'] = tr.select('td')[3].get_text()
            item['publish_time'] = tr.select('td')[4].get_text()
            # print(item)
            item_list.append(item)
        return item_list

    def write_to_file(self, content, file_path):
        try:
            with open(file_path, 'w', encoding='utf-8') as fw:
                fw.write(content)
        except BaseException as e:
            print(e)


def main():
    spider = TXSZSpider()

    page = 1
    root_url = 'https://hr.tencent.com/'
    target_url = root_url + 'position.php?&start=' + str((page - 1) * 10) + '#a'
    html = spider.download(target_url)
    if html:
        zp_list = spider.parser(html)
        # print(zp_list)
        content = json.dumps(zp_list, ensure_ascii=False)
        spider.write_to_file(content, './txzp.json')
    else:
        print('目标url有误')


if __name__ == '__main__':
    main()
