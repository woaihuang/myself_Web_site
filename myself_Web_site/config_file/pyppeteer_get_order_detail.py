#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-


import pymysql
from lxml import etree
from bs4 import BeautifulSoup
import requests, json, re, random, time



class get_order_msg():
    def __init__(self, username, pwd, user_agent):

        self.username = username
        self.pwd = pwd
        self.user_agent = user_agent

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

        self.order_url = "https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm"




    def get_html(self, cookie, user_agent):
        proxy = eval(random.choice(self.iplist))

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Cookie": cookie,
            "Host": "buyertrade.taobao.com",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self.user_agent
        }

        logis_header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": cookie,
            "Host": "detail.i56.taobao.com",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self.user_agent
        }

        try:
            reql = requests.get(self.order_url, headers=headers, proxies=proxy)
            reql.encoding = 'utf-8'
            order_json_list = json.loads(eval(re.findall("JSON.parse(.*?);\n</script>", reql.text, re.S)[0]))

            for order in order_json_list["mainOrders"]:
                productid = order['subOrders'][0]['itemInfo']['id']
                order_num = order['id']
                createTime = order['orderInfo']['createTime']
                actualFee = order['payInfo']['actualFee']
                shop_name = order['seller']['nick']
                product_img = "https:" + order['subOrders'][0]['itemInfo']['pic']

                title = ""
                for subOrders in order['subOrders']:
                    title += subOrders['itemInfo']['title'] + "&"

                if "shopUrl" in order['seller']:
                    shopUrl = "https:" + order['seller']['shopUrl']
                else:
                    shopUrl = ""

                logistics_information, waybill_number, waybill_name = [], None, None
                for i in order['statusInfo']['operations']:
                    if i['text'] == '查看物流':
                        try:
                            trade_id = re.findall('trade_id=(.*?)&', i['url'])
                            seller_id = re.findall('seller_id=(.*)', i['url'])
                            logis_url = "https://detail.i56.taobao.com/trace/trace_detail.htm?tId={}&userId={}".format(trade_id[0], seller_id[0])
                            logistics_html = requests.get(logis_url, headers=logis_header, proxies=proxy, allow_redirects=False)

                            logistics_html.encoding = 'gbk'
                            logistics = logistics_html.text

                            soup = BeautifulSoup(logistics, features="html.parser")

                            li_tag = soup.select("ul[class='nav-package'] li a")

                            if li_tag:
                                logis_url_1 = "https:" + str(li_tag[0]["href"]).replace("¤t", "&current")
                                logistics_html_1 = requests.get(logis_url_1, headers=logis_header, proxies=proxy, allow_redirects=False)

                                logistics_html_1.encoding = 'gbk'
                                logistics = logistics_html_1.text
                            try:
                                waybill_number = re.findall('mailNo = "(.*?)\";', logistics, re.S)[0]
                                waybill_name = re.findall('cpName = "(.*?)\";', logistics, re.S)[0]
                            except Exception as fn3:
                                print(fn3)
                            for order_logis in eval(re.findall("var list = (.*?);", logistics.replace("&ldquo;", "").replace("&rdquo;", "").replace("&amp;", "&"), re.S)[0]):
                                logistics_information_dict = {}
                                logistics_information_dict['datatime'] = order_logis['date'] + ' ' + order_logis['time']
                                logistics_information_dict['text'] = order_logis["text2"]
                                logistics_information.append(logistics_information_dict)

                            break
                        except Exception as fn3:
                            print(order_num, "不支持查询")



                insert_sql = """INSERT INTO order_table (username, userpwd, order_num, product_name, order_creattime, actualFee, shop_name, product_img, shopUrl, 
                waybill_number, waybill_name, logistics_information, createtime, updatatime, productid) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', "{}", NOW(), NOW(), '{}')""".\
                    format(self.username, self.pwd, order_num, title.replace("保险服务&", '')[:-1], createTime, actualFee, shop_name, product_img, shopUrl, waybill_number, waybill_name, logistics_information, productid)

                try:
                    self.taobao_cur.execute(insert_sql)

                except Exception as E:
                    if "PRIMARY" in str(E):
                        updata_sql = """UPDATE order_table SET logistics_information="{}", updatatime=NOW() WHERE order_num='{}'""".format(str(logistics_information), order_num)
                        try:
                            self.taobao_cur.execute(updata_sql)
                        except Exception as fn:
                            print("更改数据错误：{}".format(fn))

        except Exception as fn1:
            print("更新cookie状态: {}".format(fn1))
            updata_cookie_sql = "UPDATE cookie_table SET status=2 WHERE username='{}' AND pwd='{}'".format(self.username, self.pwd)
            try:
                self.taobao_cur.execute(updata_cookie_sql)
            except Exception as fn2:
                print("更改cookie状态失败：{}".format(fn2))

        finally:
            self.taobao_con.commit()
            self.taobao_cur.close()
            self.taobao_con.close()



    def main(self):
        select_sql = "SELECT cookie FROM `cookie_table` WHERE username='{}' AND pwd='{}'".format(self.username, self.pwd)
        try:
            self.taobao_cur.execute(select_sql)
        except Exception as E:
            print("查询错误！{}".format(E))

        cookie = self.taobao_cur.fetchall()

        self.get_html(cookie[0][0])




def start_func(username, pwd, user_agent):
    get_ordermsg = get_order_msg(username, pwd, user_agent)
    get_ordermsg.main()





if __name__ == '__main__':
    username = "金骆驿"  # 淘宝用户名
    pwd = "jly1314yy1207"  # 密码
    print(username, pwd)
    start_func(username, pwd)


