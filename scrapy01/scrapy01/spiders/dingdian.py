import re
import scrapy
from scrapy.http import Request  # 跟进url时需要用到它
from bs4 import BeautifulSoup
from scrapy01.items import DingDIanItem, NovelContentItem
from scrapy01.mysqlpipelines.mySqlDBTools import MySqlDBTools


class DingDianSpider(scrapy.Spider):
    name = 'dingdian'
    allow_domain = ['23us.so']
    base_url = 'http://www.23us.so/'

    def start_requests(self):
        for i in range(1, 11):
            if i == 10:
                url = self.base_url + 'full.html'
            else:
                url = self.base_url + 'list/' + str(i) + '_1.html'
            # print(url)
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        # print(response.text)
        last_page = BeautifulSoup(response.text, 'html.parser').find('a', class_='last').string
        url = response.url
        base_url = response.url[:-6]
        # print(response.url[:-6])
        for i in range(1, int(last_page) + 1):
            if url[-9:] == 'full.html':
                url = 'http://www.23us.so/modules/article/articlelist.php?fullflag=1&page=' + str(i)
            else:
                url = base_url + str(i) + '.html'
            yield Request(url=url, callback=self.get_name)

    def get_name(self, response):
        trs = BeautifulSoup(response.text, 'html.parser').find_all('tr', bgcolor="#FFFFFF")
        for tr in trs:
            novel_name = tr.find('a').string
            novel_url = tr.find('a').get('href')
            yield Request(url=novel_url, callback=self.get_novel_detail, meta={'name': novel_name, 'novelUrl':novel_url})

    def get_novel_detail(self, response):
        item = DingDIanItem()
        tds = BeautifulSoup(response.text, 'html.parser').find('table', id='at').find_all('td')
        name_id = response.url.split('/')[-1][:-5]
        item['name_id'] = name_id
        item['name'] = response.meta['name']
        item['author'] = tds[1].get_text().replace('\xa0', '')
        item['novelUrl'] = response.meta['novelUrl']
        item['category'] = tds[0].get_text().replace('\xa0', '')
        item['serialStatus'] = tds[2].get_text().replace('\xa0', '')
        item['serialNumber'] = tds[4].get_text().replace('\xa0', '')

        chapters_url = BeautifulSoup(response.text, 'html.parser').find('p', class_='btnlinks').find('a', class_='read').get('href')

        # return item
        # print(item)
        yield item
        yield Request(chapters_url, callback=self.get_chapters, meta={'name_id': name_id})

    def get_chapters(self, response):
        urls = BeautifulSoup(response.text, 'html.parser').find('table', id='at').find_all('a')
        num = 0
        for url in urls:
            num += 1
            chapter_url = url.get('href')
            chapter_name = url.string
            mysql = MySqlDBTools()
            res = mysql.dqlExecute('select * from content where chapter_url="'+chapter_url+'"')
            if res:
                print('已经存在该章节')
            else:
                yield Request(chapter_url, callback=self.get_content, meta={'name_id': response.meta['name_id'],
                                                                        'chapter_name': chapter_name,
                                                                        'chapter_url': chapter_url,
                                                                        'sort_num': num})

    def get_content(self, response):
        item = NovelContentItem()
        item['name_id'] = response.meta['name_id']
        item['chapter_name'] = response.meta['chapter_name']
        item['chapter_url'] = response.meta['chapter_url']
        item['sort_num'] = response.meta['sort_num']
        content = BeautifulSoup(response.text, 'html.parser').find('dd', id='contents').get_text()
        item['chapter_content'] = content.replace('\xa0', '')
        return item
