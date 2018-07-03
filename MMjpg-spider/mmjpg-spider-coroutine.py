import os

import aiohttp
import asyncio
from lxml import etree


class MmjpgSpider(object):

    def __init__(self):
        self.target_url = 'http://www.mmjpg.com/'
        self.img_interface_url = 'http://www.mmjpg.com/data.php?id=%s&page=8999'
        self.img_base_url = 'http://fm.shiyunjj.com/2018/%s/%s.jpg'
        self.packages_url_list = []

    async def download(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.target_url) as response:
                self.packages_url_list, titles = await self.parse_html(await response.text())
            print(self.packages_url_list)
            print(titles)
            for i in range(len(self.packages_url_list)):
                print('开始下载 %s: %s' % (titles[i], self.packages_url_list[i]))
                mn_id = self.packages_url_list[i].split('/')[-1]
                headers = {'Referer': self.packages_url_list[i], 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
                async with session.get(self.img_interface_url % mn_id, headers=headers) as response:
                    keys_list = await self.parse_img_keys(await response.text())
                    img_dir = './mm/' + titles[i]
                    self.make_dir(img_dir)
                    for j in range(len(keys_list)):
                        img_url = self.img_base_url % (mn_id, str(j + 1) + 'i' + keys_list[j])
                        print('开始下载 %s' % img_url)
                        async with session.get(img_url, headers=headers) as response:
                            img_path = os.path.join(img_dir, str(j + 1) + 'i' + keys_list[j] + '.jpg')
                            await self.save_img_to_file(img_path, await response.read())

    def make_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    async def parse_html(self, html):
        x_html = etree.HTML(html)
        hrefs = x_html.xpath('//div[@class="pic"]/ul/li/a/@href')
        titles = x_html.xpath('//div[@class="pic"]/ul/li/span/a/text()')
        return hrefs, titles

    async def parse_img_keys(self, html):
        return html.split(',')

    async def save_img_to_file(self, path, content):
        with open(path, 'wb') as fw:
            fw.write(content)

    def run(self):
        loop = asyncio.get_event_loop()
        task = asyncio.wait([self.download()])
        loop.run_until_complete(task)


if __name__ == '__main__':
    mmjpg = MmjpgSpider()
    mmjpg.run()
