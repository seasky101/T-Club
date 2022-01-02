from django.db import models
from django.contrib.auth.models import User
from django.db.models.expressions import OrderBy
from django.db import transaction
from xpinyin import Pinyin 
from faker import Faker
 

# Create your models here.

# 社团信息

class Org(models.Model):
    """
    社团信息
    """
    email = models.EmailField(verbose_name='申请人邮箱', max_length=128, unique=True)
    name = models.CharField(verbose_name='社团名称', max_length=128, unique=True)
    description = models.TextField(verbose_name='社团描述', null=True, blank=True)
    apply_at = models.DateTimeField(auto_now_add=True, verbose_name='申请时间')
    action_at = models.DateTimeField(auto_now=True, verbose_name='操作时间')
    # approve_at = models.DateTimeField(null=True, blank=True, verbose_name='同意时间')
    # STATUS_CHOICES = (
    #     ('审核中', '审核中'),
    #     ('审批通过', '审批通过'),
    #     ('审批不通过', '审批不通过'),
    # )
    # status = models.CharField(verbose_name='状态', max_length=32)

    apply_file = models.FileField(verbose_name='申请成立书', upload_to='org_apply')
    member_file = models.FileField(verbose_name='成员登记表', upload_to='org_apply')
    manager_info_file = models.FileField(verbose_name='社团发起人情况', upload_to='org_apply')
    constitution_file = models.FileField(verbose_name='社团章程', upload_to='org_apply')
    teacher_confirm_file = models.FileField(verbose_name='教师确认指导书', upload_to='org_apply')
    college_confirm_file = models.FileField(verbose_name='单位确认指导书', upload_to='org_apply')

    # manager = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='管理者', null=True, blank=True)
    # create_at = models.DateTimeField(auto_now_add=True, verbose_name='系统添加时间')

    def __str__(self) -> str:
        return self.name + self.email

    class Meta:
        verbose_name = "社团申报管理"
        verbose_name_plural = verbose_name
        ordering = ('-apply_at',)

class Approve(models.Model):
    """
    审批状态
    """
    org = models.OneToOneField(Org, verbose_name='社团', on_delete=models.CASCADE)
    action_at = models.DateTimeField(auto_now=True, verbose_name='操作时间')
    reason = models.TextField(verbose_name='原因(不通过则填写)', null=True, blank=True)

    STATUS_CHOICES = (
        ('审核中', '审核中'),
        ('审批通过', '审批通过'),
        ('审批不通过', '审批不通过'),
    )
    status = models.CharField(verbose_name='状态', max_length=32, choices=STATUS_CHOICES)

    class Meta:
        verbose_name = "社团审批管理"
        verbose_name_plural = verbose_name
        ordering = ('-action_at',)

    def __str__(self) -> str:
        return self.org.name + '-' + self.status

class Manager(models.Model):
    """
    社团管理员账号
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    org = models.OneToOneField(Org, on_delete=models.CASCADE, verbose_name='社团')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='系统添加时间')

    def __str__(self) -> str:
        return self.org.name + '-' + self.user.username



from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from mysite.settings import EMAIL_FROM
from django.contrib import messages

@transaction.atomic
@receiver(post_save, sender=Approve)
def send_email_to_apply_user(sender, instance, created, **kwargs):
    """
    发送邮件
    """
    # if created: # 新增一个审批
    email = instance.org.email # 申请人
    status = instance.status
    reason = instance.reason
    msg = ''
    if status == '审批通过':
        # 新建用户
        p = Pinyin() 
        fake = Faker()  
        username = p.get_pinyin(instance.org.name, '') # 汉字转拼音
        password = fake.password(length=10, special_chars=False, digits=True, upper_case=True, lower_case=True)
        
        new_user = User(username=username)
        new_user.email = email
        new_user.set_password(password)
        new_user.save()

        # 新增管理者
        manager = Manager(user=new_user)
        manager.org=instance.org
        manager.save()
        # if created: # 如果是新增的话
        #     instance.manager = new_user
        #     instance.save()

        # 新增社团与用户的
        msg = f'''
            恭喜你的社团审批已经通过，
            你可以使用以下账号来登录本系统:<br>
            账号： <span style="color:red">{username}</span><br>
            密码：<span style="color:red">{password}</span><br>
            你可以使用该系统进行成员管理与材料提交工作，谢谢！'''
        
    elif status == '审批不通过':
        msg = f'''
            很遗憾，你的社团审批未通过，原因如下:
            <br>
            <p style="color:red">
            {reason}
            </p>
            <br>
            请及时改正!以便重新提交！
        '''  
    
    if msg != '':
        # 发送邮件
        subject = '社团审核结果通知'	#主题
        message = '我是内容'	#内容
        sender = EMAIL_FROM		#发送邮箱，已经在settings.py设置，直接导入
        receiver = [email, ]	#目标邮箱 切记此处只能是列表或元祖
        html_message = msg
        try:
            send_mail(subject,message,sender,receiver,html_message=html_message)
            # messages.success(request, '已发送邮件到申请人!')
        except:
            # messages.error(request, '邮件发送失败！')      
            pass          



        


class Member(models.Model):
    """
    社团成员
    """
    org = models.ForeignKey(Org, on_delete=models.CASCADE, verbose_name='社团')
    name = models.CharField(verbose_name='姓名', max_length=32)
    stu_no = models.CharField(verbose_name='学号', max_length=32)
    _class = models.CharField(verbose_name='班级', max_length=32)
    role = models.CharField(verbose_name='职务', max_length=32)
    remark = models.CharField(verbose_name='备注', max_length=128, null=True, blank=True)
    join_date = models.DateField(verbose_name='入会日期')
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self) -> str:
        return self.org.name + '-' + self.name
    
    class Meta:
        verbose_name = "社团成员管理"
        verbose_name_plural = verbose_name
        ordering = ('-create_at',)

class YearApproveFile(models.Model):
    """
    年审材料
    """
    org = models.ForeignKey(Org, on_delete=models.CASCADE, verbose_name='社团')
    apply_file = models.FileField(verbose_name='材料', upload_to='org_year_apply')
    remark = models.CharField(verbose_name='备注', max_length=128, null=True, blank=True)
    STATUS_CHOICES = (
        ('审核中', '审核中'),
        ('审批通过', '审批通过'),
        ('审批不通过', '审批不通过'),
    )
    status = models.CharField(verbose_name='状态', max_length=32, choices=STATUS_CHOICES, default='审核中')
    oponion = models.TextField(verbose_name='审核意见')
    create_at = models.DateTimeField(verbose_name='提交时间', auto_now_add=True)
    action_at = models.DateTimeField(auto_now=True, verbose_name='操作时间')

    def __str__(self) -> str:
        return self.org.name + '-' + self.status
    
    class Meta:
        verbose_name = "年审材料管理"
        verbose_name_plural = verbose_name
        ordering = ('-create_at',)

class Top10ApproveFile(models.Model):
    """
    十佳评审材料
    """
    org = models.ForeignKey(Org, on_delete=models.CASCADE, verbose_name='社团')
    apply_file = models.FileField(verbose_name='材料', upload_to='org_top10_apply')
    remark = models.CharField(verbose_name='备注', max_length=128, null=True, blank=True)
    STATUS_CHOICES = (
        ('审核中', '审核中'),
        ('审批通过', '审批通过'),
        ('审批不通过', '审批不通过'),
    )
    status = models.CharField(verbose_name='状态', max_length=32, choices=STATUS_CHOICES, default='审核中')
    oponion = models.TextField(verbose_name='审核意见')
    create_at = models.DateTimeField(verbose_name='提交时间', auto_now_add=True)
    action_at = models.DateTimeField(auto_now=True, verbose_name='操作时间')

    def __str__(self) -> str:
        return self.org.name + '-' + self.status
    
    class Meta:
        verbose_name = "十佳社团评审材料管理"
        verbose_name_plural = verbose_name
        ordering = ('-create_at',)

