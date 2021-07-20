# coding:utf-8
import requests
import random
import re
from lxml import etree
import db
import time

# Cookie = "SINAGLOBAL=4869597537665.138.1625798329174;
# SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWqJo27J9mECw8c1aw.JsMd5JpX5KMhUgL.Fo
# -NeoM0ehB7SKq2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMfS0zNe05Xeh-c; ALF=1657678694; SSOLoginState=1626142694;
# SCF=AqXAEhlSMyrGIXnlBHjJmmK7cp32TYkKKmD1f_mp18VDUA69my3jfktpy2WwuWZDGMG_OxXtpQ9Qf5gnn88uM9I.;
# SUB=_2A25N6Ie3DeRhGeNJ6VUS8CrMzjqIHXVun_5_rDV8PUNbmtB-LXLSkW9NS_Qb5Yx00hEvGTDaMHZCxInu2RhGD-LV;
# _s_tentry=login.sina.com.cn; UOR=,,login.sina.com.cn; Apache=9080337338255.385.1626142695519;
# ULV=1626142695528:3:3:1:9080337338255.385.1626142695519:1625807096984; XSRF-TOKEN=PC6s5hIgJHi0h4JmFuvJG0D8;
# WBPSESS=_KL16Cq3pX7RAefey_hd4OzP_i6Oj_2E8FMtqPv1NGN8Va1uz9rr-LseFN0
# -M3SixB6tDXSVqhVfDt6tSCtidxWN5HQuvL4uIm_bJKX4cUhiYa3eJRvEDvNIYvr5d0GL; WBStorage=2ceabba76d81138d|undefined;
# cross_origin_proto=SSL"

# Cookie = [ "SINAGLOBAL=4869597537665.138.1625798329174; UOR=,,login.sina.com.cn;
# webim_unReadCount=%7B%22time%22%3A1626255519501%2C%22dm_pub_total%22%3A2%2C%22chat_group_client%22%3A0%2C
# %22chat_group_notice%22%3A0%2C%22allcountNum%22%3A41%2C%22msgbox%22%3A0%7D;
# SCF=AqXAEhlSMyrGIXnlBHjJmmK7cp32TYkKKmD1f_mp18VDI0NpfDaqAQWnoLOvGWDSpwR86k0bF14M-oQeb08LasM.;
# _s_tentry=login.sina.com.cn; Apache=2618915491380.0874.1626315291359;
# ULV=1626315291381:9:9:7:2618915491380.0874.1626315291359:1626272421500; WBStorage=2ceabba76d81138d|undefined;
# login_sid_t=183a6b4b2b9a43b5d5c7c1028e2d5cbc; cross_origin_proto=SSL; wb_view_log=1536*8641.125;
# SUB=_2A25N6-6JDeRhGeBG7VoY8yfNyTmIHXVugUdBrDV8PUNbmtAKLWLBkW9NQeq--U_UsNjZzrPG6ZU56RLMD9vHL3JX;
# SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhLvj0mrSsdwLfLlKKlQ3hV5JpX5KzhUgL.FoqRSon4e0.peo-2dJLoIpMLxKML1h-L12-LxK.LBK
# -LB.eR1K-fSntt; ALF=1657852502; SSOLoginState=1626316505; XSRF-TOKEN=xbupPxxB9Bf1tNvpeqAj-Qzl;
# WBPSESS=-wBW-KVUno8Ie1kgkRyp1I2JV3QKEDOCvfNpthjfAH-vUHp-nRc-U8e6qzWHv4B94iQEOE57AmzXlC0AhM4vc
# -5PqCdww3qQyYqbWEP1HcKgYbafdtbJdRLCwnrucAcf", "SINAGLOBAL=4869597537665.138.1625798329174;
# SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWqJo27J9mECw8c1aw.JsMd5JpX5KMhUgL.Fo
# -NeoM0ehB7SKq2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMfS0zNe05Xeh-c; ALF=1657678694; SSOLoginState=1626142694;
# SCF=AqXAEhlSMyrGIXnlBHjJmmK7cp32TYkKKmD1f_mp18VDUA69my3jfktpy2WwuWZDGMG_OxXtpQ9Qf5gnn88uM9I.;
# SUB=_2A25N6Ie3DeRhGeNJ6VUS8CrMzjqIHXVun_5_rDV8PUNbmtB-LXLSkW9NS_Qb5Yx00hEvGTDaMHZCxInu2RhGD-LV;
# _s_tentry=login.sina.com.cn; UOR=,,login.sina.com.cn; Apache=9080337338255.385.1626142695519;
# ULV=1626142695528:3:3:1:9080337338255.385.1626142695519:1625807096984; XSRF-TOKEN=PC6s5hIgJHi0h4JmFuvJG0D8;
# WBPSESS=_KL16Cq3pX7RAefey_hd4OzP_i6Oj_2E8FMtqPv1NGN8Va1uz9rr-LseFN0
# -M3SixB6tDXSVqhVfDt6tSCtidxWN5HQuvL4uIm_bJKX4cUhiYa3eJRvEDvNIYvr5d0GL; WBStorage=2ceabba76d81138d|undefined;
# cross_origin_proto=SSL", "SINAGLOBAL=4869597537665.138.1625798329174; UOR=,,login.sina.com.cn;
# SCF=AqXAEhlSMyrGIXnlBHjJmmK7cp32TYkKKmD1f_mp18VDI0NpfDaqAQWnoLOvGWDSpwR86k0bF14M-oQeb08LasM.;
# _s_tentry=login.sina.com.cn; Apache=2618915491380.0874.1626315291359;
# ULV=1626315291381:9:9:7:2618915491380.0874.1626315291359:1626272421500;
# login_sid_t=183a6b4b2b9a43b5d5c7c1028e2d5cbc; cross_origin_proto=SSL; wb_view_log=1536*8641.125;
# XSRF-TOKEN=xbupPxxB9Bf1tNvpeqAj-Qzl; WBPSESS=-wBW-KVUno8Ie1kgkRyp1I2JV3QKEDOCvfNpthjfAH-vUHp-nRc
# -U8e6qzWHv4B94iQEOE57AmzXlC0AhM4vc-5PqCdww3qQyYqbWEP1HcKgYbafdtbJdRLCwnrucAcf;
# WBStorage=2ceabba76d81138d|undefined;
# SUB=_2A25N69JFDeRhGeBP61QQ8CrOyj-IHXVugUSNrDV8PUNbmtAKLUvHkW9NRZQcmZHGpZkYYbJ9R1URS1Oa96PsRGWW;
# SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhsUrMIY8fkXPb9CT.pEwbZ5JpX5KzhUgL.FoqpehqpehBEeKe2dJLoIEyBH-iGi--fiK.7iKn0i
# --4i-zRi-2pi--fi-z7iKysi--NiK.4i-i2; ALF=1657853333; SSOLoginState=1626317334; wvr=6;
# wb_view_log_6106104213=1536*8641.125; webim_unReadCount=%7B%22time%22%3A1626317338548%2C%22dm_pub_total%22%3A0%2C
# %22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A22%2C%22msgbox%22%3A0%7D",
# "login_sid_t=f37b592607728c338cd67bc6fc2ca1b4; cross_origin_proto=SSL; WBStorage=2ceabba76d81138d|undefined;
# wb_view_log=1536*8641.25; _s_tentry=passport.weibo.com; Apache=4260929582780.697.1626317678602;
# SINAGLOBAL=4260929582780.697.1626317678602; ULV=1626317678610:1:1:1:4260929582780.697.1626317678602:;
# SUB=_2A25N69MkDeRhGeFI71cX-SfIyT-IHXVugUPsrDV8PUNbmtAKLWTYkW9NfQNEu5uPoN15-UWyZAoTHVb9iCYVMBt2;
# SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWaU7ahVYVW321VI3O7fY4N5JpX5KzhUgL.FoMcSh-c1K.Xeoe2dJLoI7LWHHxleKMReh-t;
# ALF=1657853684; SSOLoginState=1626317685; wvr=6; wb_view_log_7645699423=1536*8641.25;
# WBtopGlobal_register_version=2021071510; webim_unReadCount=%7B%22time%22%3A1626317847508%2C%22dm_pub_total%22%3A3
# %2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A34%2C%22msgbox%22%3A0%7D", ]
Cookie = 'SINAGLOBAL=4869597537665.138.1625798329174; UOR=,,login.sina.com.cn; wvr=6; webim_unReadCount={' \
         '"time":1626318925513,"dm_pub_total":0,"chat_group_client":0,"chat_group_notice":0,"allcountNum":22,' \
         '"msgbox":0}; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhsUrMIY8fkXPb9CT.pEwbZ5JpX5KMhUgL' \
         '.FoqpehqpehBEeKe2dJLoIEyBH-iGi--fiK.7iKn0i--4i-zRi-2pi--fi-z7iKysi--NiK.4i-i2; ALF=1657937126; ' \
         'SSOLoginState=1626401127; ' \
         'SCF=AqXAEhlSMyrGIXnlBHjJmmK7cp32TYkKKmD1f_mp18VD1YhjIbnHKAOrJg8ylNVjbZa1crs31J_TcHVNSrC8Dbk.; ' \
         'SUB=_2A25N9Jk3DeRhGeBP61QQ8CrOyj-IHXVug43_rDV8PUNbmtAKLVCikW9NRZQcmSsY9OAagUcfRBZ2bSJlOO20KSin; ' \
         '_s_tentry=login.sina.com.cn; Apache=4072972089919.9863.1626401132849; ' \
         'ULV=1626401132883:10:10:8:4072972089919.9863.1626401132849:1626315291381 '


# 爬起文章页面
def get_content(id):
    openurl = "https://weibo.com/ttarticle/p/show?id=" + id
    # print(openurl)

    # openurl = "https://weibo.com/ttarticle/p/show?id=2309404658196294795275"  # 测试用的
    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Cookie": Cookie,
        "Host": "weibo.com",
        "cache-control": "no-cache",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-user": "?1",
        "Referer": openurl,
        "sec-ch-ua": '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.124 Safari/537.36 "
    }
    get_text = requests.post(openurl, headers=header).text
    # print(get_text)
    sql = ''
    text = ''
    print(openurl)

    try:

        # print(get_text)
        auth_id = int(re.findall(r'\$CONFIG\[\'oid\'] = \'(\d+)\'', get_text)[0])
        auth_name = re.findall(r'\$CONFIG\[\'onick\'] = \'(.*?)\';', get_text)[0]
        html = etree.HTML(get_text)
        time_sql = html.xpath("//span[@class='time']/text()")[0][:-1]
        if ':' in time_sql:
            time_sql = '2021-' + time_sql
        else:
            time_sql = time_sql[:10]
        time_sql = time_sql[:10]
        # 阅读数
        read_num = html.xpath("//div[@class = 'W_fr']/span/text()")[0]
        read_num = re.findall(r'阅读数：(\d+.+)', read_num)[0]
        read_num = int(re.sub(r'万\+', '0000', read_num))
        # print(read_num)
        # 转发数
        num = html.xpath("//ul[@class = 'WB_row_line WB_row_r3 clearfix S_line2']/li/a/span/span//text()")
        # print(num)
        forward_num = re.findall(r'转发(\s+\d+)', num[0])

        if len(forward_num) == 0:
            forward_num = 0
        else:
            forward_num = int(forward_num[0])
        # print(forward_num)
        # 评论
        comment_num = re.findall(r'评论(\s+\d+)', num[1])

        if len(comment_num) == 0:
            comment_num = 0
        else:
            comment_num = int(comment_num[0])
        # 评论ID

        comment_id = html.xpath("//div[@action-type='feed_list_item']/@mid")[0]
        # print(comment_id)

        # 点赞数
        like_num = html.xpath("//ul[@class = 'WB_row_line WB_row_r3 clearfix S_line2']/li/a/span/span/span/em/text()")
        if len(like_num) == 0:
            like_num = 0
        else:
            like_num = int(like_num[0])
        # print(like_num)
        html_text = html.xpath('//div[@class="WB_editor_iframe_new"]//text()')
        if not html_text:
            html_text = html.xpath("//div[@class='WB_editor_iframe_word']//text()")
        for i in html_text:
            text += i
        text = re.sub(u'\u200b', '', text)
        text = re.sub(u'\xa0', '', text)
        text = re.sub(r'\s', '', text)
        isCrawled = 1

        # sql = f"UPDATE title SET `read_num` = '{read_num}' ,`time`='{time_sql}',`forward_num`='{forward_num}',
        # `comment_num`='{comment_num}' ,`like_num`='{like_num}' ,`isCrawled`={isCrawled},`auth_id`='{auth_id}',
        # `auth_name`='{auth_name}' ,`text`=\"{text}\" WHERE `id`='{id}';"
        if text == '':
            isCrawled = -2
        sql = f'UPDATE title SET `comment_times`=0,`comment_id` =\'{comment_id}\', `read_num` = \'{read_num}\' ,' \
              f'`time`=\'{time_sql}\',`forward_num`=\'{forward_num}\',`comment_num`=\'{comment_num}\' ,`like_n' \
              f'um`=\'{like_num}\' ,`isCrawled`={isCrawled},`auth_id`=\'{auth_id}\',`auth_name`=\'{auth_name}\' ,' \
              f'`text`="{text}" WHERE `id`=\'{id}\'; '

        # print(sql)

        # print(time_sql, read_num, forward_num, comment_num, like_num, )
        # print(sql)

    except:
        sql = f"UPDATE title SET `isCrawled`=-1 WHERE `id`='{id}'"

    finally:
        print(sql)
        db.exec(sql, id)


def main():
    while True:
        print("**************************")
        query_sql = 'select id from title where isCrawled=0  limit 1;'
        query = db.query(query_sql)
        if len(query) == 1:
            id = query[0][0]

            get_content(id)

        else:
            break
        a = random.randint(6, 10)
        time.sleep(a)


if __name__ == "__main__":
    main()
    # id = '2309404658889747726705'
    # id = '2309404610306109210909'
    #
    # id = '2309404437466168819771'
    # id = '2309354572906054353120'
    # get_content(id)

    # 进度完成情况
    # SELECT isCrawled,count(isCrawled) FROM title GROUP BY isCrawled;
    # print(db.query(SQL))

    # update title set isCrawled=0 where isCrawled=1;

    # 关键字
    # SELECT `key`FROM title GROUP BY `key`;
