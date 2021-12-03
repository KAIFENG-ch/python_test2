import requests
from lxml import etree
from selenium import webdriver
from random import randint
import time
import pymysql

db = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    database='python_test2'
)


class News:
    url = 'https://jwch.fzu.edu.cn/jxtz.htm'

    def __init__(self):
        self.urlList = []
        self.titles = []
        self.writers = []
        self.dates = []
        self.articles = []
        self.files = []

    def getHtml(self):
        res = requests.get(self.url)
        html_ = etree.HTML(res.content.decode())
        i = 1
        while True:
            path = '/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/ul/li[{pg}]/a/@href'.format(pg=i)
            i = i + 1
            if not html_.xpath(path):
                break
            else:
                news_url = 'https://jwch.fzu.edu.cn/' + html_.xpath(path)[0]
                self.urlList.append(news_url)
        # print(self.urlList)
        pg = 163
        while pg >= 160:
            url = 'https://jwch.fzu.edu.cn/jxtz/{page}.htm'.format(page=pg)
            res = requests.get(url)
            html_ = etree.HTML(res.content.decode())
            for i in range(1, 21):
                new_url = html_.xpath(
                    '/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/ul/li[{n}]/a/@href'.format(n=i))
                url_ = new_url[0].split('/')[0]
                goal_url = 'https://jwch.fzu.edu.cn/' + new_url[0].lstrip(url_)
                self.urlList.append(goal_url)
            pg = pg - 1
        # print(self.urlList)
        # print(len(self.urlList))
        return self.urlList

    def getPage(self, urls_):
        news_title_path = "/html/body/div/div[2]/div[2]/form/div/div[1]/div/div[1]/h4"
        news_writer_path = "/html/body/div/div[2]/div[1]/p/a[3]"
        news_date_path = "/html/body/div/div[2]/div[2]/form/div/div[1]/div/div[2]/div[1]/span[1]"
        for url in urls_:
            res = requests.get(url)
            html_ = etree.HTML(res.content.decode())
            news_title = html_.xpath(news_title_path)
            news_writer = html_.xpath(news_writer_path)
            news_date = html_.xpath(news_date_path)
            option = webdriver.ChromeOptions()
            option.add_argument('headless')
            driver = webdriver.Chrome(options=option)
            driver.get(url)
            article = driver.find_element_by_id("detailCon")
            # print(news_title[0].text, "\n", news_writer[0].text, "\n", news_date[0].text, "\n", article.text)
            # self.titles.append(news_title[0].text)
            # self.writers.append(news_writer[0].text)
            # self.dates.append(news_date[0].text)
            # self.articles.append(article.text)
            flag = 1
            file_str = ''
            while True:
                file_path = '/html/body/div/div[2]/div[2]/form/div/div[1]/div/ul/li[{page}]/a'.format(page=flag)
                file_load_path = '/html/body/div/div[2]/div[2]/form/div/div[1]/div/ul/li[{pages}]/span'.format(
                    pages=flag)
                flag = flag + 1
                if not html_.xpath(file_path):
                    break
                else:
                    file_load = driver.find_element_by_xpath(file_load_path)
                    # print(html_.xpath(file_path)[0].text, ' ', file_load.text)
                    file_str = file_str + html_.xpath(file_path)[0].text + ' 下载次数：' + file_load.text + ' '
            self.files.append(file_str)
            cursor = db.cursor()
            sql = "insert into fzunews(url, titles, writer, dates, articles, files) values ('%s', '%s','%s','%s'," \
                  "'%s','%s')" % \
                  (url, news_title[0].text, news_writer[0].text, news_date[0].text, article.text, file_str)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                print('error')
                db.rollback()

            print('verify OK')
            time.sleep(randint(1, 5))
        db.close()
    # def insertDB(self):
    #     db = pymysql.connect(
    #         host='localhost',
    #         user='root',
    #         password='123456',
    #         database='python_test2'
    #     )
    #     for column in range(20):
    #         cursor = db.cursor()
    #         sql = "INSERT INTO fzunews(url, titles, writer, dates, articles, files)" \
    #               " values ('%s','%s','%s','%s','%s','%s')" % \
    #               (self.urlList[column], self.titles[column], self.writers[column], self.dates[column],
    #                self.articles[column], self.files[column])
    #         try:
    #             cursor.execute(sql)
    #             db.commit()
    #         except:
    #             print('error')
    #             db.rollback()
    #     db.close()


if __name__ == '__main__':
    fzu = News()
    urls = fzu.getHtml()
    fzu.getPage(urls)
    # fzu.insertDB()
