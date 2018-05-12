from urllib import request


def main():
    url = 'http://www.baidu.com'
    resp = request.urlopen(url)
    print(resp.getcode())  # 获取状态码
    print(resp.read())  # 打印返回内容
    # resp.seek(0)
    # print(len(resp.read()))  # 获取返回内容的长度

    # 注意：如果url中包含了中文需要使用 request.quote() 进行编码
    # request.quote()  # 因为URL里含中文，需要进行编码


if __name__ == '__main__':
    main()
