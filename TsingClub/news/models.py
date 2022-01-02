from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


# Create your models here.
class News(models.Model):
    """
    公告
    """
    
    title = models.CharField(max_length=64, verbose_name='公告标题')
    content = RichTextUploadingField(verbose_name='公告内容')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = "公告管理"
        verbose_name_plural = verbose_name
        ordering = ('-create_at',)

    def __str__(self):
        return self.title
