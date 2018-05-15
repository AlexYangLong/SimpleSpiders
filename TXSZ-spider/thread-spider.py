import requests
from bs4 import BeautifulSoup

from user_agent import get_random_useragent


def download(url):
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


def parser(html):
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


def write_to_file(content, file_path):
    pass


def main():
    total_page = 10
    for page in range(1,total_page + 1):
        pass


if __name__ == '__main__':
    main()
