from org.models import *
from django import forms
from django.utils.html import format_html
class ApplyForm(forms.ModelForm):
    class Meta:
        model = Org
        exclude = ('manager', )
        labels = {
            'apply_file': format_html('申请成立书 <a href="/static/muban/材料1：清华大学学生社团成立申请书（范例）.docx">模板下载</a>'),
            'member_file': format_html('成员登记表 <a href="/static/muban/材料2：清华大学学生社团成立登记表.docx">模板下载</a>'),
            'manager_info_file': format_html('社团发起人情况 <a href="/static/muban/材料3：清华大学学生社团发起人情况.docx">模板下载</a>'),
            'constitution_file': format_html('社团章程 <a href="/static/muban/材料4：清华大学学生社团章程（模板）.docx">模板下载</a>'),
            'teacher_confirm_file': format_html('教师确认指导书 <a href="/static/muban/材料5：清华大学学生社团指导教师确认书.docx">模板下载</a>'),
            'college_confirm_file': format_html('单位确认指导书 <a href="/static/muban/材料6：清华大学学生社团业务指导单位确认书.docx">模板下载</a>'),
        }

class MemberForm(forms.ModelForm):
    join_date = forms.DateField(label='入会日期', widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'), input_formats=['%Y-%m-%d']) # 规定form控件显示日期的格式
    class Meta:
        model = Member
        exclude = ('org', )

class YearApproveForm(forms.ModelForm):
    class Meta:
        model = YearApproveFile
        fields = ('apply_file', 'remark')
        labels = {
            'apply_file': format_html('年审文件 <a href="/static/muban/年审文件.zip">模板下载</a>'),
        }

class Top10Form(forms.ModelForm):
    class Meta:
        model = Top10ApproveFile
        fields = ('apply_file', 'remark')
        labels = {
            'apply_file': format_html('年审文件 <a href="/static/muban/社团评优.zip">模板下载</a>'),
        }
