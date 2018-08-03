"""
Author：Alex Yang
Time: 2018-07-28
Target：爬取手机淘宝商品的内容页
Package：selenium
"""

from selenium import webdriver


def main():
    # url = 'https://market.m.taobao.com/app/dinamic/h5-tb-detail/index.html?id=569988617860'
    url = 'https://item.taobao.com/item.htm?id=569988617860'

    # 设置 User-Agent
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent="MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')
    # 模拟Chrome浏览器
    chrome_driver = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
    broswer = webdriver.Chrome(chrome_driver, chrome_options=options)

    # 打开浏览器，请求url
    broswer.get(url)
    # 隐式等待3秒
    broswer.implicitly_wait(3)
    # 滚动条向下移动 1000 px
    broswer.execute_script('window.scrollTo(0, 1000)')
    # /html/body/div[1]/div[1]/div[9]/div/div[2]/div[1]/span
    # 模拟点击 规格 按钮
    broswer.find_element_by_xpath('/html/body/div[1]/div[1]/div[9]').click()
    broswer.implicitly_wait(2)

    # 用于保存数据
    data_list = []
    # 获取跳出框的所有颜色 li 标签
    color_lis = broswer.find_elements_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div/div/div[2]/div[2]/ul/li')
    # 遍历 颜色 按钮
    for i in range(len(color_lis)):
        # 模拟点击
        color_lis[i].click()
        broswer.implicitly_wait(2)
        # 因为每次点击弹出框的按钮都会刷新，所以要重新获取 颜色 按钮li标签
        this_li = broswer.find_elements_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div/div/div[2]/div[2]/ul/li[' + str(i+1) +']')

        data = dict(color=this_li[0].text)
        data['size_list'] = []

        # 获取所有尺码 li 标签
        size_lis = broswer.find_elements_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div/div/div[2]/div[1]/ul/li')
        # 遍历
        for j in range(len(size_lis)):
            size_lis[j].click()
            broswer.implicitly_wait(2)
            # 获取价格
            price = broswer.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div/div/div[1]/div/div[2]/div/p[1]').text[1:]
            # 获取库存
            quantity = broswer.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div/div/div[1]/div/div[2]/div/p[2]').text.split(':')[-1]
            # 重新获取 尺码 li 标签
            s_li = broswer.find_elements_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div/div/div[2]/div[1]/ul/li[' + str(j+1) +']')
            s_dict = dict(size=s_li[0].text, price=price, quantity=quantity)
            data['size_list'].append(s_dict)

            # 重新获取所有尺码 li 标签
            size_lis = broswer.find_elements_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div/div/div[2]/div[1]/ul/li')
        data_list.append(data)
        # 重新获取所有颜色 li 标签
        color_lis = broswer.find_elements_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div/div/div[2]/div[2]/ul/li')
    print(data_list)

    broswer.implicitly_wait(2)

    # 关闭浏览器
    broswer.quit()


if __name__ == '__main__':
    main()
