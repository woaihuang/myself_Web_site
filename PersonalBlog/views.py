from django.shortcuts import render, redirect, HttpResponse

# Create your views here.

from django import views



class index(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, "PersonalBlog/index.html")





class single(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, "PersonalBlog/single.html")




