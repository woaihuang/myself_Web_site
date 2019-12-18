"""myself_Web_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from Personal_resume import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^down_file1/', views.down_file1),
    path('', views.login.as_view()),
    path('login/', views.login.as_view()),
    path('homepage/', views.homepage.as_view()),
    path('chart/', views.chart.as_view()),
    path('Get_catalogue/', views.Get_catalogue.as_view()),
    path('pageination/', views.pageination.as_view()),
    path('BookCraw/', views.BookCraw.as_view()),
    path('GetCatalogue/', views.GetCatalogue.as_view()),
    path('Access_to_the_body/', views.Access_to_the_body.as_view()),
    path('cataloguepage/', views.cataloguepage.as_view()),
    path('contentpage/', views.contentpage.as_view()),
]
