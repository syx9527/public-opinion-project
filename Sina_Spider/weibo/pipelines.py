# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re, time

import logging
import pymongo

from weibo.items import *
import weibo.db as db


class WeiboPipeline:
    def process_item(self, item, spider):
        if isinstance(item, TitleItem):
            print(item)

            sql = f"INSERT INTO title VALUES ('{item['id']}', '{item['title']}', '{item['openurl']}','{item['key']}',0,0,'','','0-0-0 0:0:0',0,0,0,0,NULL)"
            db.exec_(sql)

        # if isinstance(item, UrlItem):
        #     sql = f"INSERT INTO `url` VALUES ('{item['url']}')"
        #     db.exec_(sql)

        if isinstance(item, TextItem):
            if item.isCrawled == 1:
                sql = f"UPDATE title SET `read_num` = '{item.read_num}' ,`time`='{item.time_sql}',`forward_num`='{item.forward_num}',`comment_num`='{item.comment_num}' ,`like_num`='{item.like_num}' ,`comment_times`=0,`isCrawled`=1,`auth_id`='{item.auth_id}',`auth_name`='{item.auth_name}' ,`text`=\"{item.text}\" WHERE `id`='{item.id}';"
            elif item.isCrawled == -1:
                sql = f"UPDATE title SET `isCrawled`=-1 WHERE `id`='{id}'"
            db.exec(sql, item.id)


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

        self.db[TitleItem.collection].create_index([('openurl', pymongo.ASCENDING)])

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, TitleItem):
            self.db[item.collection].update({'openurl': item.get('openurl')}, {'$set': item}, True)

        return item
