from .mySqlDBTools import MySqlDBTools
from scrapy01.items import DingDIanItem, NovelContentItem


class DingDianPipeline(object):

    def process_item(self, item, spider):
        mysql = MySqlDBTools()
        if isinstance(item, DingDIanItem):
            name_id = item['name_id']
            res = mysql.dqlExecute('select * from novel where name_id="'+name_id+'"')
            if res:
                print('已经存在')
            else:
                r = mysql.dmlExecute('insert into novel (name_id, name, author, novel_url, category, serial_status, serial_number)'
                                     ' values("'+item['name_id']+'",'
                                     '"'+item['name']+'",'
                                     '"'+item['author']+'",'
                                     '"'+item['novelUrl']+'",'
                                     '"'+item['category']+'",'
                                     '"'+item['serialStatus']+'",'
                                     '"'+item['serialNumber']+'")')
                if r:
                    print('存储小说名成功')
                else:
                    print('存储小说名失败')
        if isinstance(item, NovelContentItem):
            r = mysql.dmlExecute('insert into content (name_id, chapter_name, chapter_content, chapter_url, sort_num)'
                                 ' values("' + item['name_id'] + '",'
                                 '"' + item['chapter_name'] + '",'
                                 '"' + item['chapter_content'] + '",'
                                 '"' + item['chapter_url'] + '",'
                                 '"' + str(item['sort_num']) + '")')
            if r:
                print('存储小说内容成功')
            else:
                print('存储小说内容失败')