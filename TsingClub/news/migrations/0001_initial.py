# Generated by Django 3.1.2 on 2021-12-23 19:51

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='公告标题')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='公告内容')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '公告管理',
                'verbose_name_plural': '公告管理',
                'ordering': ('-create_at',),
            },
        ),
    ]
