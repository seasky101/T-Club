from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """
    定义公告的显示方式
    """
    list_display = ('title', 'create_at')