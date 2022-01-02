from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import News


def news_list(request):
    """
    公告列表
    :param request:
    :return:
    """
    news = News.objects.all().order_by('-create_at')
    return render(request, 'news/list.html', {'news_list': news})

def news_detail(request, nid):
    """
    新闻详情
    :param request:
    :param nid:
    :return:
    """
    news = get_object_or_404(News, id=nid)
    return render(request, 'news/detail.html', {'news': news})
