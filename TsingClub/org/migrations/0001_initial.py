# Generated by Django 3.1.2 on 2021-12-23 19:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Org',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=128, unique=True, verbose_name='申请人邮箱')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='社团名称')),
                ('description', models.TextField(blank=True, null=True, verbose_name='社团描述')),
                ('apply_at', models.DateTimeField(auto_now_add=True, verbose_name='申请时间')),
                ('action_at', models.DateTimeField(auto_now=True, verbose_name='操作时间')),
                ('apply_file', models.FileField(upload_to='org_apply', verbose_name='申请成立书')),
                ('member_file', models.FileField(upload_to='org_apply', verbose_name='成员登记表')),
                ('manager_info_file', models.FileField(upload_to='org_apply', verbose_name='社团发起人情况')),
                ('constitution_file', models.FileField(upload_to='org_apply', verbose_name='社团章程')),
                ('teacher_confirm_file', models.FileField(upload_to='org_apply', verbose_name='教师确认指导书')),
                ('college_confirm_file', models.FileField(upload_to='org_apply', verbose_name='单位确认指导书')),
            ],
            options={
                'verbose_name': '社团申报管理',
                'verbose_name_plural': '社团申报管理',
                'ordering': ('-apply_at',),
            },
        ),
        migrations.CreateModel(
            name='YearApproveFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apply_file', models.FileField(upload_to='org_year_apply', verbose_name='材料')),
                ('remark', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
                ('status', models.CharField(choices=[('审核中', '审核中'), ('审批通过', '审批通过'), ('审批不通过', '审批不通过')], default='审核中', max_length=32, verbose_name='状态')),
                ('oponion', models.TextField(verbose_name='审核意见')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='提交时间')),
                ('action_at', models.DateTimeField(auto_now=True, verbose_name='操作时间')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='org.org', verbose_name='社团')),
            ],
            options={
                'verbose_name': '年审材料管理',
                'verbose_name_plural': '年审材料管理',
                'ordering': ('-create_at',),
            },
        ),
        migrations.CreateModel(
            name='Top10ApproveFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apply_file', models.FileField(upload_to='org_top10_apply', verbose_name='材料')),
                ('remark', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
                ('status', models.CharField(choices=[('审核中', '审核中'), ('审批通过', '审批通过'), ('审批不通过', '审批不通过')], default='审核中', max_length=32, verbose_name='状态')),
                ('oponion', models.TextField(verbose_name='审核意见')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='提交时间')),
                ('action_at', models.DateTimeField(auto_now=True, verbose_name='操作时间')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='org.org', verbose_name='社团')),
            ],
            options={
                'verbose_name': '十佳社团评审材料管理',
                'verbose_name_plural': '十佳社团评审材料管理',
                'ordering': ('-create_at',),
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('stu_no', models.CharField(max_length=32, verbose_name='学号')),
                ('_class', models.CharField(max_length=32, verbose_name='班级')),
                ('role', models.CharField(max_length=32, verbose_name='职务')),
                ('remark', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
                ('join_date', models.DateField(verbose_name='入会日期')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='org.org', verbose_name='社团')),
            ],
            options={
                'verbose_name': '社团成员管理',
                'verbose_name_plural': '社团成员管理',
                'ordering': ('-create_at',),
            },
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='系统添加时间')),
                ('org', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='org.org', verbose_name='社团')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
        ),
        migrations.CreateModel(
            name='Approve',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_at', models.DateTimeField(auto_now=True, verbose_name='操作时间')),
                ('reason', models.TextField(blank=True, null=True, verbose_name='原因(不通过则填写)')),
                ('status', models.CharField(choices=[('审核中', '审核中'), ('审批通过', '审批通过'), ('审批不通过', '审批不通过')], max_length=32, verbose_name='状态')),
                ('org', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='org.org', verbose_name='社团')),
            ],
            options={
                'verbose_name': '社团审批管理',
                'verbose_name_plural': '社团审批管理',
                'ordering': ('-action_at',),
            },
        ),
    ]
