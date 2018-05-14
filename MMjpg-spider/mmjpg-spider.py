import os
import requests
from bs4 import BeautifulSoup
from user_agent import get_random_useragent


def download(url, referer):
    try:
        headers = {
            'User-Agent': get_random_useragent(),
            'Referer': referer
        }
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            return resp
        else:
            return None
    except BaseException as e:
        print(e)
        return None


def get_content_urls(html):
    if not html:
        return None
    else:
        names = []
        urls = []
        soup = BeautifulSoup(html, 'html.parser')
        spans = soup.find_all('span', class_='title')
        for span in spans:
            a = span.find('a')
            urls.append(a.get('href'))
            names.append(a.string)
        return names, urls


def write_to_file(content, file_path):
    try:
        with open(file_path, 'wb') as fw:
            fw.write(content)
        return True
    except BaseException as e:
        print(e)
        return False


def make_dir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def main():
    page = 2
    if page == 1:
        target_url = 'http://www.mmjpg.com/'
    else:
        target_url = 'http://www.mmjpg.com/home/' + str(page)
    server_url = 'http://www.mmjpg.com'

    content_resp = download(target_url, server_url).text.encode('ISO-8859-1').decode('utf-8')
    if content_resp:
        names, urls = get_content_urls(content_resp)
        for i, url in enumerate(urls):
            print('crawl %s: %s' % (names[i], url))
            mm_id = url[url.rfind('/') + 1:]
            dir_path = './mm/' + names[i]
            img_keys = download('http://www.mmjpg.com/data.php?id='+mm_id+'&page=8999', url).text
            # http://img.mmjpg.com/2018/1347/1i43.jpg
            for j, key in enumerate(img_keys.split(',')):
                img_url = 'http://img.mmjpg.com/2018/' + mm_id + '/' + str(j + 1) + 'i' + key + '.jpg'
                print('downloading %s' % img_url)
                img_content = download(img_url, 'img.mmjpg.com')
                if img_content:
                    make_dir(dir_path)
                    if write_to_file(img_content.content, dir_path + '/' + str(j + 1) + 'i' + key + '.jpg'):
                        print('download %s successful!' % img_url)
                    else:
                        print('download %s failed!' % img_url)
                else:
                    print('图片地址有错！')
    else:
        print('目标地址请求出错！')


if __name__ == '__main__':
    main()
