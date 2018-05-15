import requests
from user_agent import get_random_useragent
from bs4 import BeautifulSoup
from collections import OrderedDict


def get_title_url(html):
    title_dict = OrderedDict()
    soup = BeautifulSoup(html, 'html.parser')
    all_a = soup.find_all('a', class_='title')
    for a in all_a:
        title_dict[a.string] = a.get('href')
    return title_dict


def get_content(html):
    content = ''
    soup = BeautifulSoup(html, 'html.parser')
    all_p = soup.find('div', class_='show-content-free').find_all('p')
    for p in all_p:
        content += p.text + '\n'
    return content


def main():
    target_url = 'https://www.jianshu.com/c/yD9GAd?utm_medium=index-collections&utm_source=desktop'
    server_url = 'https://www.jianshu.com'

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'www.jianshu.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': get_random_useragent()
    }

    session = requests.session()
    session.get('https://www.jianshu.com', headers=headers)
    print(session.cookies.get_dict())

    resp = session.get(target_url, headers=headers)
    print(resp.cookies.get_dict())

    title_dict = get_title_url(resp.text)
    for title, url in title_dict.items():
        r = session.get(server_url + url, headers=headers)
        print(r.cookies.get_dict())

        content = get_content(r.text)
        with open('./' + title + '.txt', 'w', encoding='utf-8') as fw:
            fw.write(content)


if __name__ == '__main__':
    main()