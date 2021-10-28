from django.urls import path
from user import views
app_name='user'
urlpatterns=[
path('login/',views.login_view,name='login_view'),
path('', views.re_home_view),
path('home/', views.home_view, name='home_view'),
path('logout/', views.logout_view),
]