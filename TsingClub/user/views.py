from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
import hashlib
from user.models import User
# Create your views here.

def re_home_view(request):
    return HttpResponseRedirect(reverse('user:home_view', current_app=request.resolver_match.namespace))
def re_login_view(request):
    return HttpResponseRedirect(reverse('user:login_view', current_app=request.resolver_match.namespace))
def login_view(request):
    #处理GET请求
    if request.method == 'GET':
        #1, 首先检查session，判断用户是否第一次登录，如果不是，则直接重定向到首页
        if 'username' in request.session:  #request.session 类字典对象
            return HttpResponseRedirect('/user/home')
        #2, 然后检查cookie，是否保存了用户登录信息
        if 'username' in request.COOKIES:
            #若存在则赋值回session，并重定向到首页
            request.session['username'] = request.COOKIES['username']
            return HttpResponseRedirect('/user/home')
        #不存在则重定向登录页，让用户登录
        return render(request, 'loginPage.html')
    # 处理POST请求
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        m = hashlib.md5()
        m.update(password.encode())
        password_m = m.hexdigest()
        #判断输入是否其中一项为空或者格式不正确
        if not username or not password:
            error = '用户名或密码错误不能为空 !'
            return render(request, 'loginPage.html', locals())
        #若输入没有问题则进入数据比对阶段，看看已经注册的用户中是否存在该用户
        users = User.objects.filter(username=username, password=password_m)
        # 由于使用了filter, 所以返回值user是一个数组，但是也要考虑其为空的状态，即没有查到该用户
        if not users:
            error = '用户不存在或用户密码输入错误!!'
            return render(request, 'loginPage.html', locals())
        # 返回值是个数组，并且用户名具备唯一索引，当前用户是该数组中第一个元素
        users = users[0]
        request.session['username'] = username
        response = HttpResponseRedirect('/user/home')
        #检查post 提交的所有键中是否存在 isSaved 键
        if 'isSaved' in request.POST.keys():
            #若存在则说明用户选择了记住用户名功能，执行以下语句设置cookie的过期时间
            response.set_cookie('username', username, 60*60*24*7)
        return response
def logout_view(request):
    #实现退出功能
    #删除session
    if 'username' in request.session:
        del request.session['username']
    resp = HttpResponseRedirect('/user/home')
    #删除cookie
    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    return resp
def home_view(request):
    if 'username' in request.session:
        return render(request, 'user_homePage.html')
    else:
        return HttpResponseRedirect('/user/login')