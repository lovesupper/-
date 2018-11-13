# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class DushuPipeline(object):
    def open_spider(self, spider):
        self.fp = open('dushu.json','w',encoding='utf-8')

    def process_item(self, item, spider):

        print(item)

        obj = dict(item)
        print('*'*50)
        print(obj)
        print('*' * 50)
        str1 = json.dumps(obj,ensure_ascii=False)
        self.fp.write(str1)
        return item

    def close_spider(self, spider):
        self.fp.close()
from scrapy.utils.project import get_project_settings
import pymysql
'''
把连接参数放到settings文件中  
然后再管道中通过from scrapy.utils.project import get_project_settings
 的get_project_settings方法获取settings文件的参数
 然后建立与数据库之间的连接
 然后访问
'''
class MysqlPipeline(object):
    #如何把settings中的内容拿过来
    def __init__(self):
        #通过get_project_settions()方法获取settings
        settings = get_project_settings()
        #通过=左边的值 获取等号右边的值
        self.host = settings['DB_HOST']
        self.port = settings['DB_PORT']
        self.user = settings['DB_USER']
        self.pwd = settings['DB_PWD']
        self.name = settings['DB_NAME']
        self.charset = settings['DB_CHARSET']
        #参数获取之后  就需要建立和数据库之间的连接
        self.connect()
    #这个都是准备工作
    def connect(self):
        self.conn = pymysql.connect(host=self.host,
                                    port=self.port,
                                    user=self.user,
                                    password=self.pwd,
                                    db=self.name,
                                    charset=self.charset)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = 'insert into book1(src, alt, author) values("%s", "%s", "%s")' % (
        item['src'], item['alt'], item['author'])
        # 执行sql语句
        self.cursor.execute(sql)
        print('#'*50)
        yield item
        # self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()
        self.cursor.close()
