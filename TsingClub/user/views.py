from django.shortcuts import render
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as auth_logout, hashers
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

#reate your views here.
def user_login(request):
    """
    登录
    """
    if request.method == 'GET':
        user_form = LoginForm()
        return render(request, 'user/login.html', {'user_form': user_form})
    else:
        user_form = LoginForm(request.POST)
        if user_form.is_valid():
            cd = user_form.cleaned_data
            user = authenticate(request, username = cd['username'], password=cd['password']) # 验证
            login(request, user) # 登录
            messages.success(request, '登录成功!')
            next = request.GET.get('next', '')
            if next != '':
                return redirect(next)
            return redirect('/')
        else:
            return render(request, 'user/login.html', {'user_form': user_form})

def register(request):
    """
    注册
    """
    if request.method == 'GET':
        # 已经登录需要先退出登录
        if request.user is not None:
            auth_logout(request)
        user_form = RegisterForm()
        return render(request, 'user/register.html', {'user_form': user_form})
    else:
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            # 新建用户
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            
            messages.success(request, '注册成功! 请先登录!')
            return redirect('user:login')
        else:
            return render(request, 'user/register.html', {'user_form': user_form})

@login_required
def change_password(request):
    """
    修改密码
    """
    if request.method == 'GET':
        user_form = PasswordForm()
        return render(request, 'user/change_password.html', {'user_form': user_form})
    else:
        user_form = PasswordForm(request.POST)
        if user_form.is_valid():
            user = request.user
            password = user_form.cleaned_data['password']
            user.password = hashers.make_password(password)  # 正式修改密码，自动加密
            user.save()
            messages.success(request, '密码修改成功! 请先登录!')
            return redirect('user:login')
        else:
            return render(request, 'user/change_password.html', {'user_form': user_form})

def logout(request):
    """
    退出登录
    """
    auth_logout(request)
    messages.success(request, '注销成功!')
    return redirect('user:login')




