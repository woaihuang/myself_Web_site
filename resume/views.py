from django.shortcuts import render

# Create your views here.

from django import views



class my_personel_resume(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'resume/index.html')



class My_essays(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'resume/index1.html')
