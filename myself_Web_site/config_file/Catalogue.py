#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-



from multiprocessing.dummy import Pool as ThreadPool
import requests, random, pymysql, bs4, datetime
from lxml import etree



class xiaoshuoxiazai():
    def __init__(self):
        self.taobao_con = pymysql.connect(
            host='120.27.147.99',
            user="root",
            password="Root_12root",
            database="python_taobao_demo",
            charset='utf8'
        )

        self.taobao_cur = self.taobao_con.cursor()


    def  get_proxy(self):
        proxy_sql = "SELECT proxy FROM `proxy_table`"
        try:
            self.taobao_cur.execute(proxy_sql)
        except Exception as E:
            print("查询错误！{}".format(E))

        aa = self.taobao_cur.fetchall()
        proxy_list = [i[0] for i in aa]

        return proxy_list




    def GetPageNum(self, channel):
        countNum_sql = "SELECT COUNT(1), FLOOR(COUNT(1)/50) FROM ebook.xiaoshuotable WHERE category='{}'".format(channel)

        try:
            self.taobao_cur.execute(countNum_sql)
        except Exception as E:
            print("查询总页码失败：", E)

        return self.taobao_cur.fetchall()




    def GetBookCatalogue(self, channel):

        proxy = eval(random.choice(self.get_proxy()))

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "_abcde_qweasd=0; BAIDU_SSP_lcr=https://www.baidu.com/link?url=DTNoYVxwKIlIcikGYo0FnNxZyrhRKANnArGjHlJspLK&wd=&eqid=ad2e729f000f4611000000045de74efb; _abcde_qweasd=0; Hm_lvt_169609146ffe5972484b0957bd1b46d6=1575440125; bdshare_firstime=1575440125457; Hm_lpvt_169609146ffe5972484b0957bd1b46d6=1575440134",
            "Host": "www.xbiquge.la",
            "Referer": "http://www.xbiquge.la/paihangbang/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
        }

        page = 1

        reql = requests.get("http://www.xbiquge.la/fenlei/{}_1.html".format(channel), proxies=proxy, headers=headers)

        html = etree.HTML(reql.text)

        while page <= int(html.xpath('//*[@id="pagestats"]//text()')[0].split('/')[1])/10:
            if page != 1:
                reql = requests.get("http://www.xbiquge.la/fenlei/{}_{}.html".format(channel, page), proxies=proxy, headers=headers)
                html = etree.HTML(reql.text)
            for i in range(1, len(html.xpath('//*[@id="newscontent"]/div[1]/ul/li'))):
                bookName = html.xpath('//*[@id="newscontent"]/div[1]/ul/li[{}]/span[1]/a//text()'.format(i))[0]
                bookUrl = html.xpath('//*[@id="newscontent"]/div[1]/ul/li[{}]/span[1]/a//@href'.format(i))[0]
                auth = html.xpath('//*[@id="newscontent"]/div[1]/ul/li[{}]/span[3]//text()'.format(i))[0]
                updateTime = datetime.datetime.now().strftime("%Y") + "-" + html.xpath('//*[@id="newscontent"]/div[1]/ul/li[{}]/span[2]/text()'.format(i))[0][1:-1]
                latestChapter = html.xpath('//*[@id="newscontent"]/div[1]/ul/li[{}]/span[2]/a/text()'.format(i))[0]
                ChapterUrl = "http://www.xbiquge.la" + html.xpath('//*[@id="newscontent"]/div[1]/ul/li[{}]/span[2]/a//@href'.format(i))[0]
                bookNumber = str(bookUrl).split('/')[-2]

                insert_sql = "INSERT INTO ebook.xiaoshuotable (bookNumber, bookName, bookUrl, author, category, `update`, latestChapter, ChapterUrl) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(bookNumber, bookName, bookUrl, auth, channel, updateTime, latestChapter, ChapterUrl)
                try:
                    self.taobao_cur.execute(insert_sql)
                    self.taobao_con.commit()
                except Exception as E:
                    if "PRIMARY" in str(E):
                        updateSql = "UPDATE ebook.xiaoshuotable SET `update`='{}', latestChapter='{}', ChapterUrl='{}' WHERE bookNumber='{}'".format(updateTime, latestChapter, ChapterUrl, bookNumber)
                        try:
                            self.taobao_cur.execute(updateSql)
                            self.taobao_con.commit()
                        except Exception as F:
                            print("更改数据失败！", F)

            page += 1





    def catalogue(self, bookUrl):
        proxy = eval(random.choice(self.get_proxy()))
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "_abcde_qweasd=0; bdshare_firstime=1575541295951; Hm_lvt_169609146ffe5972484b0957bd1b46d6=1575547687,1575548658,1575548669,1575548711; Hm_lpvt_169609146ffe5972484b0957bd1b46d6=1575550033",
            "Host": "www.xbiquge.la",
            "If-Modified-Since": "Thu, 05 Dec 2019 08:04:17 GMT",
            "If-None-Match": "W/5de8ba01-9b132",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36,"
        }

        reql_html = requests.get(bookUrl, proxies=proxy, headers=headers)
        reql_html.encoding = "utf-8"
        self.html = etree.HTML(reql_html.text)
        catalogueList = self.html.xpath('//*[@id="list"]/dl/dd')
        aList = [i for i in range(1, len(catalogueList) + 1)]

        pool = ThreadPool(100)
        pool.map(self.process, aList)
        pool.close()
        pool.join()
        self.taobao_cur.close()
        self.taobao_con.close()


    def process(self, sectionnum):
        taobao_con = pymysql.connect(
            host='120.27.147.99',
            user="root",
            password="Root_12root",
            database="python_taobao_demo",
            charset='utf8'
        )

        taobao_cur = taobao_con.cursor()
        section = self.html.xpath('//*[@id="list"]/dl/dd[{}]/a/text()'.format(sectionnum))[0]
        sectionUrl = self.html.xpath('//*[@id="list"]/dl/dd[{}]/a//@href'.format(sectionnum))[0]
        bookNum = sectionUrl.split('/')[2]

        insertSql = "INSERT INTO ebook.sectionTable (bookNum, sectionName, sectionUrl, sortNum) VALUES({}, '{}', '{}', {})".format(bookNum, section, sectionUrl, sectionnum)

        try:
            taobao_cur.execute(insertSql)
            taobao_con.commit()
        except Exception as E:
            pass



    def Get_date(self, channel, page):
        date_sql = "SELECT bookName, bookUrl, author, `update`, latestChapter, ChapterUrl FROM ebook.xiaoshuotable WHERE category='{}'  ORDER BY `update` DESC LIMIT {}, 50".format(channel, page)
        try:
            self.taobao_cur.execute(date_sql)
        except Exception as E:
            print("查询总页码失败：", E)

        return self.taobao_cur.fetchall()



    def selectbookdate(self, bookNum):
        print(bookNum)
        selectSql = "SELECT sectionName, sectionUrl FROM ebook.sectionTable WHERE bookNum={} ORDER BY sortNum".format(bookNum)
        try:
            self.taobao_cur.execute(selectSql)
        except Exception as E:
            print("查询总页码失败：", E)

        return self.taobao_cur.fetchall()




    def GetContent(self, bookUrl):
        proxy = eval(random.choice(self.get_proxy()))
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "_abcde_qweasd=0; bdshare_firstime=1575541295951; Hm_lvt_169609146ffe5972484b0957bd1b46d6=1575548658,1575548669,1575548711,1575593024; Hm_lpvt_169609146ffe5972484b0957bd1b46d6=1575603234",
            "Host": "www.xbiquge.la",
            "If-Modified-Since": "Tue, 20 Aug 2019 00:14:37 GMT",
            "If-None-Match": "W/5d5b3b6d-3de7",
            "Referer": "http://www.xbiquge.la/0/7/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
        }

        reql_html = requests.get(bookUrl, proxies=proxy, headers=headers)
        reql_html.encoding = "utf-8"
        html = etree.HTML(reql_html.text)

        content = html.xpath('//*[@id="content"]/text()')

        contentText = ""
        for i in content:
            contentText = contentText + i + "\n"

        return contentText






if __name__ == '__main__':
    xiaoshuoxiazai = xiaoshuoxiazai()
    xiaoshuoxiazai.GetBookCatalogue(1)


