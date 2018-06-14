# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo


class ScrapydangdangPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'), mongo_db=crawler.settings.get('MONGO_DB'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        # self.db[item.collection].insert(dict(item))
        self.db[item.collection].update({'title': item['title']}, {'$set': item},
                                        True)  # True:根据title的查找条件查找(相当于以title为唯一索引)，如果找到（有重复）则更新，没找到执行插入操作
        return item

    def close_spider(self, spider):
        self.client.close()


from scrapydangdang.items import DangdangItem
import logging
import csv

class DangDangCsvPipeline(object):
    def __init__(self):
        self.items = DangdangItem().fields
        self.filename = open('data.csv', 'a', encoding='utf-8')
        self.logger = logging.getLogger('__name__')
        fieldnames = [ item for item in self.items]
        self.__writer = csv.DictWriter(self.filename, fieldnames=fieldnames)
        self.__writer = self.__writer.writeheader()

    def process_item(self, item, spider):
        if self.__writer.writerow(dict(item)):
            self.logger.info('--------------存储到csv成功-----------------------！')
        else:
            self.logger.info('--------------存储csv失败-----------------------！')

        return item

    def close_spider(self, spider):
        self.filename.close()