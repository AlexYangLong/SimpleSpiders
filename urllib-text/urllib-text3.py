from urllib import request
import http.cookiejar


def main():
    url = 'http://www.baidu.com'

    # 声明一个CookieJar对象实例来保存cookie
    cookie = http.cookiejar.CookieJar()

    # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    handler = request.HTTPCookieProcessor(cookie)
    # 通过CookieHandler创建opener
    opener = request.build_opener(handler)
    # 安装opener
    request.install_opener(opener)

    resp = request.urlopen(url)
    print(resp.getcode())  # 获取状态码
    print(cookie)  # 打印cookie
    print(resp.read())  # 打印返回内容


if __name__ == '__main__':
    main()
