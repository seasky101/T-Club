from django.contrib.auth import login
from django.db.models import manager
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .tables import *


def index(request):
    return render(request, 'app/index.html')

# Create your views here.
def apply_org(request):
    if request.user.is_authenticated: # 已经登录，代表有账号了，此时跳转到个人详情页
        messages.error(request, '您已申请社团，不可重复申请!')
        # 社团详情
        org = Org.objects.filter(manager__user=request.user).first()
        # table = OrgTable()
        return render(request, 'app/my_apply.html', {'org': org})
        
    if request.method == 'GET':
        form = ApplyForm()
    else:
        form = ApplyForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.apply_user = request.user
            form.save()
            messages.success(request, '已提交申请，后续结果会通过邮件通知，请注意查收！')
            return redirect('/index/')
        else:
            pass
    return render(request, 'app/apply.html', {'user_form': form})

@login_required
def member_list(request):
    """
    成员管理
    """
    member = Member.objects.filter(org__manager__user=request.user)
    if request.GET.get('name', '-1') != '-1':
        member = member.filter(name__contains=request.GET.get('name'))
    
    table = MemberTable(member)

    return render(request, 'app/member/index.html', {'table': table})

@login_required
def member_add(request):
    """
    成员添加
    """
    if request.method == 'GET':
        user_form = MemberForm()
    else:
        user_form = MemberForm(request.POST)
        if user_form.is_valid():
            user_form.instance.org = request.user.manager.org
            user_form.save()
            messages.success(request, '添加成功!')
            return redirect('/member/list/')
    return render(request, 'app/member/add.html', {'user_form': user_form})

@login_required
def member_edit(request, mid):
    """
    成员编辑
    """
    member = get_object_or_404(Member, id=mid)
    user_form = MemberForm(instance=member)
    if request.method == 'GET':
        return render(request, 'app/member/edit.html', {'user_form': user_form})
    else:
        user_form = MemberForm(request.POST, instance=member) # 编辑操作
        if user_form.is_valid():
            user_form.save() # 保存
            messages.success(request, '编辑成功!')
            return redirect('/member/list/')
        else:
            return render(request, 'app/member/edit.html', {'user_form': user_form})

@login_required
def member_del(request, mid):
    member = get_object_or_404(Member, id=mid)
    member.delete()
    messages.success(request, '删除成功!')
    return redirect('/member/list/')

@login_required
def pingshen_add(request, _type='year'):
    """
    材料管理
    """
    title = ''
    if _type == 'year':
        _FORM = YearApproveForm
        user_form = YearApproveForm()
        title = '年审材料提交'
    elif _type == 'top10':
        _FORM = Top10Form
        user_form = Top10Form()
        title = '十佳社团材料提交'
    if request.method == 'GET':
        user_form = _FORM()
    else:
        user_form = _FORM(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.instance.org = request.user.manager.org
            user_form.save()
            messages.success(request, '申请成功，请等待通知!')
            return redirect('/')
    return render(request, 'app/pingshen/add.html', {'title': title, 'user_form': user_form})

@login_required
def my_pingshen(request):
    """
    我的评审
    """
    org = request.user.manager.org
    years = YearApproveFile.objects.filter(org=org)
    year_table = YearApproveTable(years)

    top10s = Top10ApproveFile.objects.filter(org=org)
    top10_table = Top10Table(top10s)
    return render(request, 'app/pingshen/list.html', {'year_table': year_table, 'top10_table': top10_table})