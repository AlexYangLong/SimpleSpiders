import requests
from user_agent import get_random_useragent


def main():
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
    resp1 = session.get('https://www.jianshu.com/p/cc3754e1a761', headers=headers)
    resp2 = session.get('https://www.jianshu.com/p/1f9663d82b58', headers=headers)
    print(resp1.cookies.get_dict())
    print(resp2.cookies.get_dict())


if __name__ == '__main__':
    main()
