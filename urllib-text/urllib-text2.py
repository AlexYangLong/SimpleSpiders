from urllib import request


def main():
    url = 'http://www.baidu.com'
    # 模拟请求头 request
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    req = request.Request(url, headers=header)

    resp = request.urlopen(req)
    print(resp.getcode())  # 获取状态码
    print(resp.read())  # 打印返回内容


if __name__ == '__main__':
    main()
