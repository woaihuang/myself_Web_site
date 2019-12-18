#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-


import asyncio, re
from pyppeteer.launcher import launch


async def cookie_log(url):

    browser = await launch({'headless': True})  # 启动pyppeteer 属于内存中实现交互的模拟器

    page = await browser.newPage()  # 启动个新的浏览器页面
    await page.goto(url)

    page_text = await page.content()

    infomation_dict = {}
    infomation_dict['realShopName'] = re.findall("&gt;(.*?)&lt", re.findall("href(.*)", re.findall("\"shopkeeper\"(.*?)/a", page_text)[0])[0])[0]

    infomation_dict['shopurl'] = "https:" + re.findall('enter-shop" href="(.*?)\"', page_text)[0]

    infomation_dict['goodstitle'] = re.findall(">(.*)", re.findall("alt</span>=\"<span(.*?)</span>", re.findall("J_ImgBooth(.*?)</tr>", page_text, re.S)[0], re.S)[0])[0]

    infomation_dict['dianpu'] = re.findall("strong&gt;</span>(.*?)<", re.findall("slogo-shopname(.*?)</tr>", page_text, re.S)[0], re.S)[0]

    infomation_dict['lastImgUrl'] = "https:" + re.findall("href=\"(.*?)\"", re.findall("J_ImgBooth(.*?)</tr>", page_text, re.S)[0], re.S)[0]

    return infomation_dict


def main(url):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    flag = loop.run_until_complete(cookie_log(url))

    return flag


if __name__ == '__main__':
    flag = main("view-source:https://detail.tmall.com/item.htm?id=602458095159")
    print(flag)