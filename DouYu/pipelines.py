# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
'''

/.virtualenvs/py2/local/lib/python2.7/site-packages/scrapy/pipelines$


'''
import os
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from settings import IMAGES_STORE
import pymongo


class DouyuImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        yield scrapy.Request(item['image_link'])

    def item_completed(self, results, item, info):

        print "--" * 30
        print results
        print "--" * 30
        '''
           [(True,
            {
            'url': 'https://rpic.douyucdn.cn/acrpic/171012/3140944_v0954.jpg',
            'path': 'full/ff7ba0e592ce219866e865115a2596039c7a574a.jpg',
             'checksum': '04d656db8f1eacea2f607f92c903d605'

            }
            )]


        '''

        img_path=[x['path'] for ok,x in results if ok]

        #保存路径到item中
        item['image_path']=IMAGES_STORE+item['nick_name']+'.jpg'

        #用文件改变文件的名字 os.rename 新名字-原名字
        os.rename(IMAGES_STORE + img_path[0], item['image_path'])

        return item


class DouyuMongoDBPipeline(object):
    def __init__(self):
        # 创建MongoDB数据库连接
        self.client = pymongo.MongoClient(host="127.0.0.1", port=27017)
        # 指定MongoDB的数据库名
        self.db_name = self.client['Douyu']
        # 指定数据库表名
        self.sheet_name = self.db_name['DouyuDirector']

    def process_item(self, item, spider):
        # 向表里插入数据，参数是一个字典
        self.sheet_name.insert(dict(item))
        return item





