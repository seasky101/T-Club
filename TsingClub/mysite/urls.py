from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from mysite import settings
from app.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('user.urls'), name='user'), # 用户
    url(r'^ckeditor/', include('ckeditor_uploader.urls')), # 引入ckeditor
    path('captcha/', include('captcha.urls')), # 验证码
    path('apply/', apply_org, name='apply'), # 申请
    path('index/', index, name='index'),
    path('member/add/', member_add, name='member_add'), # 成员添加
    path('member/list/', member_list, name='member_list'), # 成员列表
    path('member/edit/<int:mid>', member_edit, name='member_edit'), # 成员编辑
    path('member/del/<int:mid>', member_del, name='member_del'), # 成员删除
    path('', index), # 首页
    path('news/', include('news.urls'), name='news'), # 公告
    path('pingshen/add/<str:_type>/', pingshen_add, name='pingshen_add'),
    path('pingshen/list/', my_pingshen, name='my_pingshen')


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL) # 配置静态资源的路径