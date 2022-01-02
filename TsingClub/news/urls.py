from django.contrib import admin
from django.urls import path, include
from .views import *
app_name = 'news'
urlpatterns = [
    path('detail/<int:nid>', news_detail, name='detail'), # 新闻详情
    path('list/', news_list, name='list'), # 公告列表
]