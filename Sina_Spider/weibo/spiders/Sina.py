import json
from scrapy import Request, Spider
from weibo.items import *
import re
from weibo import db


class WeiboSpider(Spider):
    name = 'sina'

    allowed_domains = ['m.weibo.cn']

    sql = "CREATE TABLE IF NOT EXISTS `title`(`id` varchar(255)  NOT NULL,`title` varchar(255) ,`openurl` varchar(" \
          "255) ,`key` varchar(255) ,`isCrawled` int ,`auth_id` varchar(255) ,`auth_name` varchar(255) ," \
          "`text` longtext ,`time` datetime(0) ,`read_num` int  ,`forward_num` int ,`comment_num` int ,`like_num` int "\
          ",`comment_id`  varchar(255),`comment_times`  int  PRIMARY KEY (`id`) USING BTREE) ; "

    db.exec_(sql)
    # sql = """CREATE TABLE IF NOT EXISTS url  (`url` varchar(255) NOT NULL)"""
    # db.exec_(sql)
    # sql = """CREATE TABLE IF NOT EXISTS `key`  (`key` varchar(255) NOT NULL)"""
    # db.exec_(sql)

    # keywords = ['教育', '教学', '体育教育', '智慧教育', '科技', '体育', ]

    # keywords = ['国际教育', '特殊教育', '学科竞赛', '职业教育', 'K12', "婴儿教育", "幼儿教育"]

    keywords = ['艺术培训', '远程教育', '线下教育', 'steam教育', '应试教育', '中考', '高考', '课外辅导', '科普教育', '海外教育', '爱国教育', ]

    search_url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D21%26q%3D{' \
                 'keyword}%26t%3D0&page_type=searchall&page={page} '
    # "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D21%26q%3D%E6%95%99%E5%AD%A6%26t%3D0&page_type=searchall&page=1"
    urls = []

    def start_requests(self):

        for keyword in self.keywords:
            page = 1

            yield Request(self.search_url.format(keyword=keyword, page=page), callback=self.parse_titles,
                          meta={'keyword': keyword, 'page': page})

    def parse_titles(self, response):
        """
        解析搜索结果
        """
        print(self.keywords)
        result = json.loads(response.text)
        try:
            if result.get('data').get('cards')[0].get('card_group'):
                card_group_list = result.get('data').get('cards')[0].get('card_group')
                for card_group in card_group_list:

                    openurl = card_group.get('openurl')
                    try:
                        id = re.findall(r'https://weibo.com/ttarticle/p/show\?id=(\d+)', openurl)[0]

                        title_item = TitleItem()
                        title_item['openurl'] = openurl
                        title_item['title'] = card_group.get('title_sub')

                        title_item['id'] = id
                        # print(title_item)
                        title_item['key'] = response.meta.get('keyword')

                        yield title_item
                    except:
                        pass

        except:
            pass

        # 已爬取网页进行记录
        urlitem = UrlItem()
        urlitem['url'] = response.url
        yield urlitem

        # 下一页
        page = response.meta.get('page') + 1
        keyword = response.meta.get('keyword')
        yield Request(self.search_url.format(keyword=keyword, page=page), callback=self.parse_titles,
                      meta={'keyword': keyword, 'page': page})
