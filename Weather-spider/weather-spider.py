import json

import requests
import time
from bs4 import BeautifulSoup
from user_agent import get_random_useragent
from echarts import Echart, Bar, Axis


def downloader(url):
    """
    下载器函数，用于下载url所代表的页面
    :param url: url
    :return: 下载页面的字符串
    """
    headers = {
        'Host': 'www.weather.com.cn',
        'Referer': 'http://www.weather.com.cn/forecast/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': get_random_useragent()
    }

    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            return resp.text.encode('iso-8859-1').decode('utf-8')
    except BaseException as e:
        print(e)
    return None


def get_temperature(urls):
    """
    通过html解析出数据
    :param urls: url列表
    :return: 返回一个字典
    """
    all_data = []

    for url in urls:
        html_body = downloader(url)
        time.sleep(2)

        if not html_body:
            continue
        soup = BeautifulSoup(html_body, 'html.parser')
        conMidtab2_list = soup.find_all('div', class_='conMidtab')[0].find_all('div', class_='conMidtab2')

        for div in conMidtab2_list:
            provence_data = {}
            tr_list = div.find_all('tr')[2:]
            provence = tr_list[0].find_all('td')[0].text.replace('\n', '')
            city_list = []
            for index, tr in enumerate(tr_list):
                # 如果是第一个tr ，那么城市名和省份名是放在一行的
                city_temperature = {}
                if index == 0:
                    city = tr.find_all('td')[1].text.replace('\n', '')
                    max_temperature = tr.find_all('td')[4].text.replace('\n', '')
                    min_temperature = tr.find_all('td')[7].text.replace('\n', '')
                # 如果不是，那么该行就只有城市名
                else:
                    city = tr.find_all('td')[0].text.replace('\n', '')
                    max_temperature = tr.find_all('td')[3].text.replace('\n', '')
                    min_temperature = tr.find_all('td')[6].text.replace('\n', '')
                city_temperature['city'] = city
                city_temperature['max_temperature'] = max_temperature
                city_temperature['min_temperature'] = min_temperature
                city_list.append(city_temperature)
                provence_data['provence'] = provence
                provence_data['city_list'] = city_list
            all_data.append(provence_data)
    return all_data


def main():
    # target_urls = ['http://www.weather.com.cn/textFC/hb.shtml',
    #                'http://www.weather.com.cn/textFC/db.shtml',
    #                'http://www.weather.com.cn/textFC/hd.shtml',
    #                'http://www.weather.com.cn/textFC/hz.shtml',
    #                'http://www.weather.com.cn/textFC/hn.shtml',
    #                'http://www.weather.com.cn/textFC/xb.shtml',
    #                'http://www.weather.com.cn/textFC/xn.shtml']
    #
    # all_data = get_temperature(target_urls)
    # print(all_data)
    # 将数据保存到文件
    # with open('temperature.json', 'w', encoding='utf-8') as fw:
    #     fw.write(json.dumps(all_data))

    # 从文件中读取数据
    with open('temperature.json', 'r') as fr:
        all_data = json.loads(fr.read())
    # print(all_data)

    # 重新构造list结构
    temp_city_list = []
    for data in all_data:
        provence = data['provence']
        city_list = data['city_list']
        for city in city_list:
            city['city'] = '%s-%s' % (provence, city['city'])
            temp_city_list.append(city)
    print(temp_city_list)

    # 按照最高温度排序
    sort_max_temp_list = sorted(temp_city_list, key=lambda t: int(t.__getitem__('max_temperature')))
    # 按照最低温度排序
    sort_min_temp_list = sorted(temp_city_list, key=lambda t: int(t.__getitem__('min_temperature')))
    print(sort_max_temp_list)
    print(sort_min_temp_list)

    # 获取温度最高的10条数据
    top10_max = sort_max_temp_list[-10:]
    top10_max_city = []
    top10_max_temp = []
    print(top10_max)
    for item in top10_max:
        top10_max_city.append(item['city'])
        top10_max_temp.append(item['max_temperature'])

    # 获取温度最低的10条数据
    top10_min = sort_min_temp_list[:10]

    # 使用第三方Echarts库在浏览器中输出图形统计界面
    echart = Echart(u'全国温度统计')
    bar = Bar(u'最高温度', top10_max_temp)
    axis = Axis('category', 'bottom', data=top10_max_city)
    echart.use(bar)
    echart.use(axis)
    echart.plot()


if __name__ == '__main__':
    main()
