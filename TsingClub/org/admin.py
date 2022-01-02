from django.contrib import admin
from .models import *
# Register your models here.

admin.site.site_header = '清社圈后台管理系统'
admin.site.site_title = '清社圈后台管理系统'

@admin.register(Org)
class OA(admin.ModelAdmin):
    # def get_actions(self, request):
    #     """
    #     禁用删除按钮
    #     """
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions
    
    def has_delete_permission(self, request, obj=None):
        # 编辑页面禁用删除按钮
        return False

    list_display  = (
        'name',
        'email',
        'show_apply_status',
        'description',
        'apply_at',
        'apply_file',
        'member_file',
        'manager_info_file',
        'constitution_file',
        'teacher_confirm_file',
        'college_confirm_file'
    )
    list_filter = ('approve__status', 'apply_at', ) # 过滤项
    # 自定义显示字段
    def show_apply_status(self, obj):
        """
        申请人
        """
        if obj.approve is not None:
            return obj.approve.status
        return '暂未处理'
    show_apply_status.short_description = '当前状态'



@admin.register(Approve)
class AA(admin.ModelAdmin):
    list_display = (
        'org',
        'status', 
        'reason',
        'action_at',
    )
    list_filter = ('org__name', )

    # 更改下拉列表
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'org': # 没有列表的
            qs=[]
            qs1 = Org.objects.filter(approve__isnull=True)
            for q in qs1:
                qs += [q.name]
            qs2 = Org.objects.filter(approve__isnull=False)
            for q in qs2:
                Ap=Approve.objects.filter(org=q)[0]
                if Ap.status != '审批通过':
                    qs+=[q.name]
            QS=Org.objects.filter(name__in=qs)
            kwargs['queryset'] = QS
            
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_delete_permission(self, request, obj=None):
        # 编辑页面禁用删除按钮
        return False

@admin.register(YearApproveFile)
class YAA(admin.ModelAdmin):
    list_display = (
        'org',
        'status',
        'oponion',
        'apply_file',
        'create_at',
        'action_at'
    )
    list_filter = ('org__name', )
    search_fields = ('create_at', )

@admin.register(Top10ApproveFile)
class Top10A(admin.ModelAdmin):
    list_display = (
        'org',
        'status',
        'oponion',
        'apply_file',
        'create_at',
        'action_at'
    )
    list_filter = ('create_at', )

@admin.register(Member)
class MA(admin.ModelAdmin):
    list_display = (
        'org',
        'name',
        'stu_no',
        '_class',
        'role',
        'remark',
        'join_date',
        'create_at'
    )

    list_filter = ('org__name', )
    search_fields = ('name', )
    list_filter = ('create_at', )