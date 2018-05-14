# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DingDIanItem(scrapy.Item):
    # define the fields for your item here like:
    name_id = scrapy.Field()  # 小说编号
    name = scrapy.Field()  # 小说名
    author = scrapy.Field()  # 作者
    novelUrl = scrapy.Field()  # 小说地址
    category = scrapy.Field()  # 类别
    serialStatus = scrapy.Field()  # 连载状态
    serialNumber = scrapy.Field()  # 连载字数


class NovelContentItem(scrapy.Item):
    name_id = scrapy.Field()  # 小说id
    chapter_name = scrapy.Field()  # 小说章节名
    chapter_content = scrapy.Field()  # 小说内容
    chapter_url = scrapy.Field()  # 章节地址
    sort_num = scrapy.Field()  # 绑定章节顺序
