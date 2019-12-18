#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-



"""根据订单号获取订单信息"""

import requests, random, pymysql, re, json
from lxml import etree



class Get_order():
    def __init__(self, username, passworld, orderId):
        self.username = username
        self.passworld = passworld
        self.orderId = orderId

        self.tianmao_url = "https://trade.tmall.com/detail/orderDetail.htm?spm=a1z09.2.0.0.37a82e8dNYfgOp&bizOrderId={}".format(self.orderId)
        self.taobao_url = "https://trade.taobao.com/trade/detail/trade_order_detail.htm?biz_order_id={}".format(self.orderId)
        self.tradearchive_url = "https://tradearchive.taobao.com/trade/detail/trade_item_detail.htm?bizOrderId={}".format(self.orderId)


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

        select_sql = 'SELECT user_agent, cookie FROM cookie_table WHERE username="{}" AND pwd="{}"'.format(self.username, self.passworld)

        try:
            self.taobao_cur.execute(select_sql)
        except Exception as e:
            print(e)

        ua_date = self.taobao_cur.fetchall()

        self.cookies = ua_date[0][1]
        self.ua = ua_date[0][0]



    def Get_logistics(self, logistics_url):
        proxy = eval(random.choice(self.iplist))

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": self.cookies,
            "Host": "detail.i56.taobao.com",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self.ua
        }

        logistics_json = requests.get(logistics_url, headers=headers, proxies=proxy)
        jsomDate = eval(str(logistics_json.text).replace('false', 'False').replace("true", "True"))
        try:
            expressageDict = {}
            expressageDict['mailNo'] = jsomDate['detailList'][0]['mailNo']
            expressageDict['cpName'] = jsomDate['detailList'][0]['cpName']

            expressage_list = []
            for logis_list in jsomDate['detailList'][0]['detail']:
                logis_dict = {}
                logis_dict['time'] = logis_list['time']
                logis_dict['desc'] = logis_list['desc']
                expressage_list.append(logis_dict)

            expressageDict['expressage'] = expressage_list

            return expressageDict
        except:
            return {}



    def taobao_logic(self, logistics_url):
        proxy = eval(random.choice(self.iplist))
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": self.cookies,
            "Host": "detail.i56.taobao.com",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self.ua
        }

        logistics_json = requests.get(logistics_url, headers=headers, proxies=proxy)
        jsomDate = eval(str(logistics_json.text).replace('false', 'False').replace("true", "True"))
        try:
            expressageDict = {}
            expressageDict['mailNo'] = jsomDate['detailList'][0]['mailNo']
            expressageDict['cpName'] = jsomDate['detailList'][0]['cpName']

            expressage_list = []
            for logis_list in jsomDate['detailList'][0]['detail']:
                logis_dict = {}
                logis_dict['time'] = logis_list['time']
                logis_dict['desc'] = logis_list['desc']
                expressage_list.append(logis_dict)

            expressageDict['expressage'] = expressage_list

            return expressageDict
        except:
            return {}



    def taobao_json(self):
        proxy = eval(random.choice(self.iplist))

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": self.cookies,
            "Host": "trade.taobao.com",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self.ua
        }

        params = {
            "biz_order_id": self.orderId
        }

        reql_json = requests.get(self.taobao_url, headers=headers, params=params, proxies=proxy, allow_redirects=False)

        if reql_json.status_code == 200:
            json_date = eval(str(re.findall("JSON.parse\('(.*?)'\);", reql_json.text, re.S)[0]).strip().replace('false', 'False').replace("true", "True").replace('\\"', '"').replace('\\\\"', ''))
            takegoodsaddress = str(json_date['deliveryInfo']['address']).split('，')
            takegoodsname = takegoodsaddress[0]
            phoneNum = takegoodsaddress[1]
            address = takegoodsaddress[2]
            if "asyncLogisticsUrl" in json_date['deliveryInfo']:
                expressageDict = self.taobao_logic(str("https:"+json_date['deliveryInfo']['asyncLogisticsUrl']).replace("\\", ''))
            else:
                expressageDict = {}

            detail_url = "https:" + str(json_date['mainOrder']['subOrders'][0]['itemInfo']['auctionUrl']).replace("\\", '')
            productPic = "https:" + str(json_date['mainOrder']['subOrders'][0]['itemInfo']['pic']).replace("\\", '')
            title = json_date['mainOrder']['subOrders'][0]['itemInfo']['title']
            price = json_date['mainOrder']['subOrders'][0]['priceInfo']
            trading_status = json_date['mainOrder']['statusInfo']['text'].replace("当前订单状态：", "")

            insertSql = """INSERT INTO order_logis_table (username, passworld, orderId, takegoodsname, phoneNum, address, expressageDict, detail_url, productPic, title, price, trading_status) VALUES('{}', '{}', '{}', '{}', '{}', '{}', "{}", '{}', '{}', '{}', {}, '{}')""".format(self.username, self.passworld, self.orderId, takegoodsname, phoneNum, address, expressageDict, detail_url, productPic, title, price, trading_status)
            try:
                self.taobao_cur.execute(insertSql)
                self.taobao_con.commit()
            except Exception as E:
                updateSql = """UPDATE order_logis_table SET expressageDict="{}" WHERE orderId={}""".format(expressageDict, self.orderId)
                try:
                    self.taobao_cur.execute(updateSql)
                    self.taobao_con.commit()
                except Exception as F:
                    print("数据更改失败：", F)
            jsonDict = {}
            jsonDict['takegoodsname'], jsonDict['phoneNum'], jsonDict['address'], jsonDict['expressageDict'], jsonDict['detail_url'], jsonDict['productPic'], jsonDict['title'], jsonDict['price'], jsonDict['trading_status'] = takegoodsname, phoneNum, address, expressageDict, detail_url, productPic, title, price, trading_status
            return jsonDict
        else:
            return False





    def tianmao_json(self):
        proxy = eval(random.choice(self.iplist))

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": self.cookies,
            "Host": "trade.tmall.com",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self.ua
        }

        params = {
            "bizOrderId": self.orderId
        }

        reql_json = requests.get(self.tianmao_url, headers=headers, params=params, proxies=proxy, allow_redirects=False)
        if reql_json.status_code == 200:
            json_data = eval(str(re.findall("detailData = (.*?)</script>", reql_json.text, re.S)[0]).strip().replace('false', 'False').replace("true", "True"))
            takegoodsaddress = str(json_data['basic']['lists'][0]['content'][0]['text']).split(',')                                     #收货地址
            takegoodsname = takegoodsaddress[0]
            phoneNum = takegoodsaddress[1]
            address = takegoodsaddress[2]
            if "logistic" in json_data['orders']['list'][0]:
                expressageDict = self.Get_logistics("https:" + json_data['orders']['list'][0]['logistic']['content'][0]['url'])
            else:
                expressageDict = {}
            detail_url = "https:" + json_data['orders']['list'][0]['status'][0]['subOrders'][0]['itemInfo']['itemUrl']
            productPic = "https:" + json_data['orders']['list'][0]['status'][0]['subOrders'][0]['itemInfo']['pic']
            title = json_data['orders']['list'][0]['status'][0]['subOrders'][0]['itemInfo']['title']
            price = json_data['orders']['list'][0]['status'][0]['subOrders'][0]['priceInfo'][0]['text']
            trading_status = json_data['orders']['list'][0]['status'][0]['statusInfo'][0]['text']

            insertSql = """INSERT INTO order_logis_table (username, passworld, orderId, takegoodsname, phoneNum, address, expressageDict, detail_url, productPic, title, price, trading_status) VALUES('{}', '{}', '{}', '{}', '{}', '{}', "{}", '{}', '{}', '{}', {}, '{}')""".format(self.username, self.passworld, self.orderId, takegoodsname, phoneNum, address, expressageDict, detail_url, productPic, title, price, trading_status)
            try:
                self.taobao_cur.execute(insertSql)
                self.taobao_con.commit()
            except Exception as E:
                updateSql = """UPDATE order_logis_table SET expressageDict="{}" WHERE orderId={}""".format(
                    expressageDict, self.orderId)
                try:
                    self.taobao_cur.execute(updateSql)
                    self.taobao_con.commit()
                except Exception as F:
                    print("数据更改失败：", F)
            jsonDict = {}
            jsonDict['takegoodsname'], jsonDict['phoneNum'], jsonDict['address'], jsonDict['expressageDict'], jsonDict['detail_url'], jsonDict['productPic'], jsonDict['title'], jsonDict['price'], jsonDict['trading_status'] = takegoodsname, phoneNum, address, expressageDict, detail_url, productPic, title, price, trading_status
            return jsonDict
        else:
            return False




    def tradearchive_html(self):
        proxy = eval(random.choice(self.iplist))

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": self.cookies,
            "Host": "tradearchive.taobao.com",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self.ua
        }

        params = {
            "bizOrderId": self.orderId
        }

        reql_json = requests.get(self.tradearchive_url, headers=headers, params=params, proxies=proxy, allow_redirects=False)

        if reql_json.status_code == 200:
            html = etree.HTML(reql_json.text)
            takegoodsaddress = "".join(str(re.findall("收货地址：</td>(.*?)</tr>", reql_json.text, re.S)[0]).strip()).replace("<td>", "").replace("</td>", "").replace("\n\t\t\t\t\t\t\t\t\t\t\t", '').replace("\t\t\t\t\t\t", '').replace("\t\t\t\t\t\t", "").replace("\t\t\t\t\t\t", "").replace("\t\t\t\t\t\t\t\t\t\n", "").split("，")
            asdf = [i for i in takegoodsaddress if len(str(i).strip())>0]
            takegoodsname = asdf[0]
            phoneNum = asdf[1]
            address = asdf[2]
            expressageDict = {}
            detail_url = "https:" + html.xpath('//*[@id="J_TabView"]/div/div/div/table[1]/tbody[3]/tr[3]/td[1]/div[2]/div/span[1]/a//@href')[0]
            productPic = "https:" + html.xpath('//*[@id="J_TabView"]/div/div/div/table[1]/tbody[3]/tr[3]/td[1]/div[1]/div/a/img//@src')[0]
            title = html.xpath('//*[@id="J_TabView"]/div/div/div/table[1]/tbody[3]/tr[3]/td[1]/div[2]/div/span[1]/a//text()')[0]
            price = html.xpath('//*[@id="J_TabView"]/div/div/div/table[1]/tbody[3]/tr[3]/td[7]//text()')[0].strip()
            trading_status = "交易成功"
            insertSql = """INSERT INTO order_logis_table (username, passworld, orderId, takegoodsname, phoneNum, address, expressageDict, detail_url, productPic, title, price, trading_status) VALUES('{}', '{}', '{}', '{}', '{}', '{}', "{}", '{}', '{}', '{}', {}, '{}')""".format(self.username, self.passworld, self.orderId, takegoodsname, phoneNum, address, expressageDict, detail_url, productPic, title, price, trading_status)
            try:
                self.taobao_cur.execute(insertSql)
                self.taobao_con.commit()
            except Exception as E:
                updateSql = """UPDATE order_logis_table SET expressageDict="{}" WHERE orderId={}""".format(
                    expressageDict, self.orderId)
                try:
                    self.taobao_cur.execute(updateSql)
                    self.taobao_con.commit()
                except Exception as F:
                    print("数据更改失败：", F)
            jsonDict = {}
            jsonDict['takegoodsname'], jsonDict['phoneNum'], jsonDict['address'], jsonDict['expressageDict'], jsonDict['detail_url'], jsonDict['productPic'], jsonDict['title'], jsonDict['price'], jsonDict['trading_status'] = takegoodsname, phoneNum, address, expressageDict, detail_url, productPic, title, price, trading_status
            return jsonDict
        else:
            return False










def main(username, passworld, orderId):
    getorder = Get_order(username, passworld, orderId)
    jsonDict = getorder.tianmao_json()
    if jsonDict is False:
        jsonDict = getorder.taobao_json()
        if jsonDict is False:
            jsonDict = getorder.tradearchive_html()

    return jsonDict



if __name__ == '__main__':
    username = input("请输入用户名：")
    passworld = input("请输入密码：")
    orderId = input("请输入订单号：")
    main(username, passworld, orderId)









