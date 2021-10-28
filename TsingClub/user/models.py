from django.db import models

# Create your models here.
class User(models.Model): #创建用户信息表
    username = models.CharField(max_length=24,verbose_name='用户')
    password = models.CharField(max_length=40,verbose_name='密码')
class Club(models.Model):
    clubname = models.CharField(max_length=24,verbose_name='社团')