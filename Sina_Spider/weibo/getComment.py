# coding:utf-8
import json
import requests
import re
from lxml import etree
import db
from pymysql.converters import escape_string
import time


def get_comment(title_id, comment_id):
    page = 1
    Cookie: str = "SINAGLOBAL=4869597537665.138.1625798329174; UOR=,,login.sina.com.cn; wvr=6; " \
                  "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhsUrMIY8fkXPb9CT.pEwbZ5JpX5KMhUgL.FoqpehqpehBEeKe2dJLoIEyBH" \
                  "-iGi--fiK.7iKn0i--4i-zRi-2pi--fi-z7iKysi--NiK.4i-i2; " \
                  "ULV=1626406388024:11:11:9:3659980741847.2397.1626406388001:1626401132883; ALF=1658193793; " \
                  "SSOLoginState=1626657794; " \
                  "SCF=AqXAEhlSMyrGIXnlBHjJmmK7cp32TYkKKmD1f_mp18VDOQZ5Ta2lRrPe1kvY-XlqYMbNnjI4J-4-9BMt2B7Zq7s.; " \
                  "SUB=_2A25N8KRRDeRhGeBP61QQ8CrOyj-IHXVuh5KZrDV8PUNbmtB-LUzfkW9NRZQcmYj82o7wqvQ1tzDs79ADUXavwrFt "

    while True:
        url = f"https://weibo.com/aj/v6/comment/big?ajwvr=6&id={comment_id}&page={page}"

        header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                      "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": Cookie,
            "Host": "weibo.com",
            "cache-control": "no-cache",
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-user": "?1",
            "Referer": url,
            "sec-ch-ua": '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/91.0.4472.124 Safari/537.36 "
        }

        get_text = requests.post(url, headers=header).text

        get_text = json.loads(get_text)
        # print(get_text)
        html = etree.HTML(get_text['data']['html'])
        # print(get_text['data']['html'])
        user = html.xpath("//div[@class='list_con']")

        if user:
            for data in user:
                i = data.xpath("./div[@class='WB_text']")[0]
                db_time = data.xpath(".//div[@class='WB_from S_txt2']/text()")[0][:-1]
                user = i.xpath("./a[1]/text()")[0]
                to_user = i.xpath('./a/text()')[-1]

                # print(to_user)

                if user == to_user:
                    to_user = ''
                    comment_text = i.xpath("./text()[2]")
                else:
                    to_user = to_user[1:]
                    comment_text = i.xpath("./text()[3]")

                try:
                    db_time = re.findall(r"(\d+)月(\d+)日(.+)", db_time)[0]
                    db_time = '2021-' + db_time[0] + '-' + db_time[1] + db_time[2]

                except:
                    pass

                comment_text = comment_text[0][1:]

                user = escape_string(user)
                to_user = escape_string(to_user)
                comment_text = escape_string(comment_text)
                db_time = escape_string(db_time)

                print(user, to_user, comment_text, db_time, title_id)

                sql = """
                    INSERT INTO comment(`title_id`,`user`,`to_user`,`time`,`comment_text`) SELECT
                    %s,'%s','%s','%s','%s'
                    FROM
                    DUAL
                    WHERE
                    NOT EXISTS (
                    SELECT
                    `title_id`
                    FROM
                    comment
                    WHERE
                    `title_id`=%s and `user`='%s' and `to_user`='%s' and `time`='%s' and `comment_text`='%s'
                    );
                    """ % (
                    title_id, user, to_user, db_time, comment_text, title_id, user, to_user, db_time, comment_text)
                # print(sql)
                db.exec_(sql)
                page += 1
        else:
            break
        time.sleep(2)


def main():
    while True:
        print("*******************************************")
        query_sql = 'select title_id,comment_id from title where isCrawled!=-1 and comment_times=0 and comment_id is ' \
                    'not NULL limit 1; '

        query = db.query(query_sql)

        if len(query) == 1:
            title_id = query[0][0]
            coment_id = query[0][1]

            get_comment(title_id, coment_id)
            end_sql = "update title set `comment_times`=1 where `title_id`='%s'" % title_id
            db.exec_(end_sql)

            time.sleep(1)
        else:
            break


def great_table():
    sql = """CREATE TABLE IF NOT EXISTS `comment`  (
    `id` int NOT NULL AUTO_INCREMENT,
    `title_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
    `user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
    `to_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
    `time` datetime(0) NULL DEFAULT NULL,
    `comment_text` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
    PRIMARY KEY (`id`) USING BTREE
    ) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;"""

    db.exec_(sql)


if __name__ == '__main__':
    great_table()
    main()

    # # 回归初始状态
    # end_sql = "update title set `comment_times`=1 where `comment_times` is not null"
    # db.exec_(end_sql)

    # title_id = '2309354572906054353120'
    # coment_id = '4572906040331693'
    # get_comment(title_id, coment_id)

    # 进度完成情况
    # SELECT comment_times,count(comment_times) FROM title comment_id is not NULL GROUP BY comment_times;
