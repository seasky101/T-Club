from django.urls import path
from .views import *

app_name = 'user'

urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', register, name='register'), # 注册
    path('logout/', logout, name='logout'), # 退出
    path('change_profile/', change_password, name='change_profile'), # 修改密码
]
