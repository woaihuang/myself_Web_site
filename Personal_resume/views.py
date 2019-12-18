from django.shortcuts import render, HttpResponse, HttpResponsePermanentRedirect, redirect

# Create your views here.
from myself_Web_site.config_file import Catalogue
import datetime, hashlib, time, pymysql, json
from django.http import HttpResponseRedirect
from django import views




taobao_con = pymysql.connect(
            host='120.27.147.99',
            user="root",
            password="Root_12root",
            database="python_taobao_demo",
            charset='utf8'
        )

taobao_cur = taobao_con.cursor()



def down_file1(request):
    with open("/data/wwwroot/New_Bi_Date/static/Excelfile/bigdata.xls", "rb") as model_excel:
        result = model_excel.read()
    response = HttpResponse(result)
    response['Content-Type'] = 'application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment; filename=bigdata.xls'
    return response




class login(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, "Personal_resume/login.html")

    def post(self, request, *args, **kwargs):

        loginUsername = request.POST.get("loginUsername", None)
        loginPassword = request.POST.get("loginPassword", None)

        usernamesgin = hashUser(loginUsername)
        t_token = hashUser(datetime.datetime.now().strftime("%Y-%m-%d"))
        response = HttpResponseRedirect('/my_personel_resume/')

        response.set_cookie('loginUsername', loginUsername)
        response.set_cookie('loginPassword', loginPassword)
        response.set_cookie('sgin', usernamesgin)
        response.set_cookie('t', int(time.time()*1000), max_age=60000)
        response.set_cookie('t_token', t_token)

        return response



def hashUser(username):
    a = hashlib.md5()
    c = username + datetime.datetime.now().strftime("%Y-%m-%d")
    a.update(c.encode(encoding='utf-8'))
    return a.hexdigest()



class homepage(views.View):
    def get(self, request, *args, **kwargs):

        return render(request, "Personal_resume/homepage.html")



class chart(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, "Personal_resume/charts.html")


#personalBlog

class Get_catalogue(views.View):
    def get(self, request, *args, **kwargs):
        channel = request.GET.get("channel", None)

        pageNum = Catalogue.xiaoshuoxiazai().GetPageNum(channel)
        dateList = Catalogue.xiaoshuoxiazai().Get_date(channel, 0)
        jsonDate = {}
        DateList = []
        for i in dateList:
            datedict = {}
            datedict['bookName'] = i[0]
            datedict['bookUrl'] = i[1]
            datedict['author'] = i[2]
            datedict['update'] = i[3]
            datedict['latestChapter'] = i[4]
            datedict['ChapterUrl'] = i[5]
            DateList.append(datedict)
        jsonDate['autopageNum'] = str(pageNum[0][1])
        jsonDate['autoNum'] = str(pageNum[0][0])
        jsonDate['DateList'] = DateList
        jsonList = []
        jsonList.append(jsonDate)

        return HttpResponse(json.dumps(jsonList))



class pageination(views.View):
    def post(self, request, *args, **kwargs):
        pagenum = request.POST.get("page", None)
        channel = request.POST.get("channel", None)
        dateList = Catalogue.xiaoshuoxiazai().Get_date(channel, (int(pagenum) - 1) * 50)

        jsonDate = {}
        DateList = []
        for i in dateList:
            datedict = {}
            datedict['bookName'] = i[0]
            datedict['bookUrl'] = i[1]
            datedict['author'] = i[2]
            datedict['update'] = i[3]
            datedict['latestChapter'] = i[4]
            datedict['ChapterUrl'] = i[5]
            DateList.append(datedict)

        jsonDate['DateList'] = DateList
        jsonList = []
        jsonList.append(jsonDate)

        return HttpResponse(json.dumps(jsonList))



class BookCraw(views.View):
    def get(self, request, *args, **kwargs):
        channel = request.GET.get("channel", None)
        Catalogue.xiaoshuoxiazai().GetBookCatalogue(channel)
        return HttpResponse("ok")




class GetCatalogue(views.View):
    def post(self, request, *args, **kwargs):
        bookUrl = request.POST.get("bookUrl", None)
        bookname = request.POST.get("bookname", None)
        bookNum = bookUrl.split('/')[-2]
        BookData = Catalogue.xiaoshuoxiazai().selectbookdate(bookNum)

        jsonDate = {}
        DateList = []
        for i in BookData:
            datedict = {}
            datedict['bookName'] = i[0]
            datedict['bookUrl'] = i[1]
            DateList.append(datedict)

        jsonDate['DateList'] = DateList
        jsonList = []
        jsonList.append(bookname)
        jsonList.append(jsonDate)
        return HttpResponse(json.dumps(jsonList))



class Access_to_the_body(views.View):
    def post(self, request, *args, **kwargs):
        bookUrl = request.POST.get("bookUrl", None)
        bookname = request.POST.get("bookname", None)
        contentText = Catalogue.xiaoshuoxiazai().GetContent(bookUrl)
        contentlist=[]
        contentlist.append(str(bookname).split(" ")[1])
        contentlist.append(contentText)
        return HttpResponse(json.dumps(contentlist))




class cataloguepage(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, "Personal_resume/catalogue.html")

    def post(self, request, *args, **kwargs):
        bookUrl = request.POST.get("bookUrl", None)
        bookname = request.POST.get("bookname", None)

        Catalogue.xiaoshuoxiazai().catalogue(bookUrl)
        return HttpResponse(bookname)



class contentpage(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, "Personal_resume/contentpage.html")









