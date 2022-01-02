from django.core.mail import send_mail
from mysite.settings import *

def send_sm():
    subject = '哈哈哈哈'	#主题
    message = '我是内容'	#内容
    sender = EMAIL_FROM		#发送邮箱，已经在settings.py设置，直接导入
    receiver = ['1024749861@qq.com']	#目标邮箱 切记此处只能是列表或元祖
    html_message = '<h1>%s</h1>'%message		#发送html格式
    send_mail(subject,message,sender,receiver,html_message=html_message)