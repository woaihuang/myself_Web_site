#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-


import pymysql, re, random, requests, json, time
from bs4 import BeautifulSoup
from lxml import etree

from selenium import webdriver







class shoprank():
    def __init__(self, shopname, seacherkey):
        self.url = "https://s.taobao.com/search"

        self.shopnice = shopname
        self.seachkey = seacherkey

        self.taobao_con = pymysql.connect(
            host='120.27.147.99',
            user="root",
            password="Root_12root",
            database="python_taobao_demo",
            charset='utf8'
        )

        self.taobao_cur = self.taobao_con.cursor()

        proxy_sql = "SELECT proxy FROM `proxy_table`"
        try:
            self.taobao_cur.execute(proxy_sql)
        except Exception as E:
            print("查询错误！{}".format(E))

        aa = self.taobao_cur.fetchall()
        self.iplist = [i[0] for i in aa]


    def Get_html(self, cookies):
        proxy = eval(random.choice(self.iplist))

        ProductList = []
        Flag = True
        pagenum = 1
        breakNum = 0
        # while pagenum<3:
            # try:
        header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": cookies[0][0],
            "Host": "s.taobao.com",
            "Referer": "https://www.taobao.com/",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": cookies[0][1]
        }

        params = {
            "q": self.seachkey,
            "s": 44
        }

        reql = requests.get(self.url, headers=header, params=params, proxies=proxy)
        print(reql.text)
        productList = json.loads(str(re.findall("g_page_config = (.*?)g_srp_loadCss", reql.text, re.S)[0]).strip()[:-1])

        auctions = productList['mods']['itemlist']['data']['auctions']

        flag = False
        ranking = 1
        for j in auctions:
            print(str(j['nick']).strip())
            if self.shopnice == str(j['nick']).strip():
                rankingList = []
                flag = True
                Flag = False
                rankingList.append(pagenum)
                rankingList.append(ranking)
                ProductList.append(rankingList)
                break
            ranking += 1
        # if flag:
        #     break
        # pagenum += 1

            # except Exception as VC:
            #     print(VC)
            #     if breakNum == 3:
            #         print(breakNum)
            #         break
            #     breakNum += 1

        if Flag:
            return [["未查到您的店铺"]]

        return ProductList




    def main(self):
        select_sql = "SELECT cookie, user_agent FROM `cookie_table` WHERE `status`=1 and username='金骆驿' and pwd='jly1314yy1207'"
        try:
            self.taobao_cur.execute(select_sql)
        except Exception as E:
            print("查询错误！{}".format(E))

        cookie = self.taobao_cur.fetchall()

        productList = self.Get_html(cookie)

        return productList




def main(shopname, seacherkey):
    shop_rank = shoprank(shopname, seacherkey)
    productList = shop_rank.main()

    return productList




# if __name__ == '__main__':
#     pagenum = "lovo官方旗舰店"
#     seachkey = "四件套"
    # main(username, passworld, pagenum, seachkey)