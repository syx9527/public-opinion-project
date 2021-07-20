# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class TitleItem(scrapy.Item):
    name = 'title'
    title = scrapy.Field()
    openurl = scrapy.Field()
    id = scrapy.Field()
    key = scrapy.Field()


class TextItem(scrapy.Item):
    read_num = scrapy.Field()
    time_sql = scrapy.Field()
    forward_num = scrapy.Field()
    comment_num = scrapy.Field()
    like_num = scrapy.Field()
    auth_id = scrapy.Field()
    auth_name = scrapy.Field()
    text = scrapy.Field()
    id = scrapy.Field()
    isCrawled = scrapy.Field()



class UrlItem(scrapy.Item):
    name = 'redis'
    url = scrapy.Field()
