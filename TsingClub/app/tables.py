from django_tables2 import tables
from app.forms import YearApproveForm

from org.models import *
from django_tables2.utils import A

class OrgTable(tables.Table):
    
    class Meta:
        model = Org
        exclude = ('id', )
        attrs = {"class": "table table-striped table-bordered text-center"} # 自定义属性
        
class ActionColumn(tables.columns.Column):
    """
    编辑操作
    """
    def render(self, value):
        pass

class MemberTable(tables.Table):
    """
    定义Modeltable
    https://django-tables2.readthedocs.io/en/latest/pages/table-data.html#table-data
    """

    detail = tables.columns.LinkColumn('member_edit', args=[A('pk')], orderable=False, empty_values=(), verbose_name='编辑')

    def render_detail(self):
        return '编辑'
    
    del_col = tables.columns.LinkColumn('member_del', args=[A('pk')], orderable=False, empty_values=(), verbose_name='删除')

    def render_del_col(self):
        return '删除'

    class Meta:
        model = Member # 指定模型
        exclude = ('org', 'id')
        attrs = {"class": "table table-striped table-bordered text-center"} # 自定义属性

from django.utils.html import format_html


class FileColumn(tables.columns.Column):
    """
    自定义图片
    """
    def render(self, value):
        return format_html(
            '<a href="/media/{url}">下载<a/>',
            url=value
        )

class YearApproveTable(tables.Table):
    # 自定义链接
    apply_file = FileColumn()
    class Meta:
        model = YearApproveFile # 指定模型
        exclude = ('org', 'id')
        attrs = {"class": "table table-striped table-bordered text-center"} # 自定义属性

class Top10Table(tables.Table):
    # 自定义链接
    apply_file = FileColumn()
    class Meta:
        model = Top10ApproveFile # 指定模型
        exclude = ('org', 'id')
        attrs = {"class": "table table-striped table-bordered text-center"} # 自定义属性