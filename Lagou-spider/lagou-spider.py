"""
爬取拉勾网
有问题，在爬取职位详情页时，被阻隔
"""

import requests
import time
from bs4 import BeautifulSoup
from user_agent import get_random_useragent
import json


def crawl_positiondesc(session, p_id):
    url = 'https://www.lagou.com/jobs/%s.html' % p_id
    headers = {
        'User-Agent': get_random_useragent(),
        'Host': 'www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
        'Upgrade-Insecure-Requests': '1'
    }

    resp = session.get(url=url, headers=headers)
    print(resp.text.encode('iso-8859-1').decode('utf-8'))
    # soup = BeautifulSoup(resp.content, 'html.parser')
    # job_bt = soup.find('dd', attrs={'class': 'job_bt'})
    # return job_bt.text


def main():
    headers = {
        'User-Agent': get_random_useragent(),
        'Host': 'www.lagou.com',
        'Referer': 'www.lagou.com',
        'Upgrade-Insecure-Requests': '1',
    }
    target_url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E6%88%90%E9%83%BD&needAddtionalResult=false'

    # 获取session-cookie
    session = requests.session()
    session.get('https://www.lagou.com', headers=headers)

    headers['Referer'] = 'https://www.lagou.com/jobs/list_python?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput='
    headers['X-Anit-Forge-Code'] = '0'
    headers['X-Anit-Forge-Token'] = 'None'
    headers['X-Requested-With'] = 'XMLHttpRequest'
    positions = []
    for x in range(1, 8):
        data = {
            'first': 'true',
            'pn': x,
            'kd': 'python'
        }
        resp = session.post(target_url, headers=headers, data=data)
        json_str = resp.json()
        page_position = json_str['content']['positionResult']['result']
        for position in page_position:
            position_dict = {
                'positionId': position['positionId'],
                'positionName': position['positionName'],
                'positionDesc': crawl_positiondesc(session, position['positionId']),
                'education': position['education'],
                'city': position['city'],
                'createTime': position['createTime'],
                'companyShortName': position['companyShortName'],
                'financeStage': position['financeStage'],
                'salary': position['salary'],
                'industryField': position['industryField'],
                'district': position['district'],
                'positionAdvantage': position['positionAdvantage'],
                'companySize': position['companySize'],
                'companyLabelList': position['companyLabelList'],
                'workYear': position['workYear'],
                'positionLables': position['positionLables'],
                'companyFullName': position['companyFullName'],
                'firstType': position['firstType'],
                'secondType': position['secondType'],
                'subwayline': position['subwayline'],
                'stationname': position['stationname']
            }
            positions.append(position_dict)
        # print(positions)
        time.sleep(10)

    # line = json.dumps(positions, ensure_ascii=False)
    # with open('lagou_position.json', 'w', encoding='utf-8') as fw:
    #     fw.write(line)


if __name__ == '__main__':
    main()
    # crawl_positiondesc(4613044)