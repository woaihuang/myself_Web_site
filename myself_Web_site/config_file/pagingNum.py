#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-



import pymysql



class paging_algorithm():
    def __init__(self):
        self.taobao_con = pymysql.connect(
            host='120.27.147.99',
            user="root",
            password="Root_12root",
            database="python_taobao_demo",
            charset='utf8'
        )

        self.taobao_cur = self.taobao_con.cursor()


    def GetPageNum(self):
        countNum_sql = "SELECT COUNT(1), FLOOR(COUNT(1)/50) FROM myTest WHERE username='19'"

        try:
            self.taobao_cur.execute(countNum_sql)
        except Exception as E:
            print("查询总页码失败：", E)

        return self.taobao_cur.fetchall()

    def Get_date(self, page):
        # date_sql = "SELECT a.* FROM (SELECT * FROM myTest) as a LIMIT {}, 50".format(page)
        date_sql = "SELECT * FROM myTest LIMIT {}, 50".format(page)
        try:
            self.taobao_cur.execute(date_sql)
        except Exception as E:
            print("查询总页码失败：", E)

        return self.taobao_cur.fetchall()


