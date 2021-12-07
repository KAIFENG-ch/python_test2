import json
from selenium import webdriver
import requests
import pymysql
import time
from random import randint

db = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    database='python_test2'
)


def video_message():
    url = 'https://www.bilibili.com/video/BV19v411M7Rs?from=search&seid=7813628168892053036&spm_id_from=333.337.0.0'
    dr = webdriver.ChromeOptions()
    dr.add_argument('headless')
    driver = webdriver.Chrome(options=dr)
    driver.get(url)
    for i in range(1, 5):
        likes = driver.find_element_by_xpath("//*[@id='arc_toolbar_report']/div[1]/span[{num}]".format(num=i)).text
        print(likes)


def get_html(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/94.0.4606.81 Safari/537.36 '
    }
    res = requests.get(url, timeout=30, headers=headers)
    res.raise_for_status()
    res.encoding = 'utf-8'
    return res.text


def get_comment(url_json):
    # global goal
    comment = []
    html_ = get_html(url_json)
    try:
        goal = json.loads(html_)
    except:
        print('load error!')
    comment_num = len(goal['data']['replies'])
    pg = 0
    while pg < comment_num:
        comments = goal['data']['replies'][pg]
        dic = {'uname': comments['member']['uname'],
               'likes': comments['like'],
               'content': comments['content']['message'],
               'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(comments['ctime']))
               }
        comment.append(dic)
        pg = pg + 1
        cursor = db.cursor()
        sql = "insert into bilibili_news(uname, likes, content, times) VALUES ('%s', '%s', '%s', '%s')" % \
              (dic['uname'], dic['likes'], dic['content'], dic['time'])
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        reply_pg = 0
        reply_comment_num = len(comments['replies'])
        while reply_pg < reply_comment_num:
            reply_comments = comments['replies'][reply_pg]
            reply_dic = {
                'uname': reply_comments['member']['uname'],
                'likes': reply_comments['like'],
                'content': reply_comments['content']['message'],
                'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime((reply_comments['ctime'])))
            }
            comment.append(reply_dic)
            reply_pg = reply_pg + 1
            cursor = db.cursor()
            sql = "insert into bilibili_news(uname, likes, content, times) VALUES ('%s', '%s', '%s', '%s')" % \
                  (reply_dic['uname'], reply_dic['likes'], reply_dic['content'], reply_dic['time'])
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()

    print(comment)
    return comment


if __name__ == '__main__':
    video_message()
    for i in range(1, 5):
        url_ = 'https://api.bilibili.com/x/v2/reply?pn={pg}&type=1&oid=251187473&sort=2'.format(pg=i)
        get_comment(url_)
        time.sleep(randint(1, 5))
    db.close()
