from django.test import TestCase

# Create your tests here.
from django.test import Client, TestCase, TransactionTestCase
import org.models as ORG
from django.contrib.auth.models import User
import user.forms as UserForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from news.models import News

class test_login(TestCase):
    """
    测试用户登录登出
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test123', email='1970611068@qq.com', password='test123')
        self.admin = User.objects.create_superuser(username='admin', email='780531272@qq.com', password='admin123')
        self.client = Client()

    def test_login(self):
        response = self.client.get('/account/login/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/member/list/')
        self.assertEqual(response.status_code, 302)  # 测试跳转
        # login_form=UserForm.LoginForm()
        # login_form.username='test123'
        # login_form.password='test123'
        # response = self.client.post(login_form)
        # response = self.client.login(username='test123', password='test123')
        # self.assertTrue(response)
        login_form = UserForm.LoginForm()
        login_form.username = 'test123'
        login_form.password = 'test123'
        # self.assertTrue(login_form.is_valid())
        response = self.client.post('/account/login/', {'username': '123', 'password': login_form.password})
        self.assertEqual(response.status_code, 200)  # 登录不成功继续保持
        response = self.client.post('/account/login/', {'username': login_form.username, 'password': login_form.password})
        self.assertEqual(response.status_code, 302)  # 登录成功后跳转
        response = self.client.get('/member/list/')
        self.assertEqual(response.status_code, 200)  # 登录后不跳转
        self.client.logout()
        response = self.client.get('/member/list/')
        self.assertEqual(response.status_code, 302)  # 再次登出后将跳转
        response = self.client.get('/admin/login/')
        self.assertEqual(response.status_code, 200)
        response = self.client.login(username='admin', password='admin123')  # 管理员登录
        self.assertTrue(response)

class test_apply(TestCase):
    """
    测试社团申请，社团审批
    """
    def setUp(self):
        # self.user = User.objects.create_user(username='test123', email='1970611068@qq.com', password='test123')
        self.admin = User.objects.create_superuser(username='admin', email='780531272@qq.com', password='admin123')
        self.client = Client()
        self.apply_f = {}


    def test_apply(self):
        response = self.client.get('/apply/')
        self.assertEqual(response.status_code, 200)
        # login_form=UserForm.LoginForm()
        # login_form.username='test123'
        # login_form.password='test123'
        # response = self.client.post(login_form)

        # with open('D:/L/test.txt') as doc:
        #     apply_f['email'] = '1970611068@qq.com'
        #     apply_f['name'] = 'cbx'
        #     apply_f['description'] = '0'
        #
        #     apply_f['apply_file'] = SimpleUploadedFile("D:/L/test.txt", b"file_content", content_type="txt")
        #     apply_f['member_file'] = doc
        #     apply_f['manager_info_file'] = doc
        #     apply_f['constitution_file'] = doc
        #     apply_f['teacher_confirm_file'] = doc
        #     apply_f['college_confirm_file'] = doc
        #
        #     response = self.client.post('/apply/', apply_f)
        #     self.assertEqual(response.status_code, 302)  # 申请提交后跳转页面
        self.apply_f['email'] = '1970611068@qq.com'
        self.apply_f['name'] = 'cbx'
        self.apply_f['description'] = '0'

        self.apply_f['apply_file'] = SimpleUploadedFile("D:/L/test.txt", b"file_content", content_type="txt")
        self.apply_f['apply_file'].file_name = 'apply_file'
        self.apply_f['member_file'] = SimpleUploadedFile("D:/L/test.txt", b"file_content", content_type="txt", )
        self.apply_f['member_file'].file_name = 'member_file'
        self.apply_f['manager_info_file'] = SimpleUploadedFile("D:/L/test.txt", b"file_content", content_type="txt", )
        self.apply_f['manager_info_file'].file_name = 'manager_info_file'
        self.apply_f['constitution_file'] = SimpleUploadedFile("D:/L/test.txt", b"file_content", content_type="txt", )
        self.apply_f['constitution_file'].file_name = 'constitution_file'
        self.apply_f['teacher_confirm_file'] = SimpleUploadedFile("D:/L/test.txt", b"file_content",
                                                                  content_type="txt", )
        self.apply_f['teacher_confirm_file'].file_name = 'teacher_confirm_file'
        self.apply_f['college_confirm_file'] = SimpleUploadedFile("D:/L/test.txt", b"file_content",
                                                                  content_type="txt", )
        self.apply_f['college_confirm_file'].file_name = 'college_confirm_file'
        response = self.client.post('/apply/', self.apply_f)
        self.assertEqual(response.status_code, 302)  # 申请提交后跳转页面
        # org = ORG.Org.objects.filter(name=self.apply_f['name'])
        pass

    def test_approval(self):
        self.test_apply()
        response = self.client.login(username='admin', password='admin123')  # 管理员登录
        self.assertTrue(response)
        orgs=ORG.Org.objects.filter(name=self.apply_f['name'])
        org=orgs[0]
        self.assertEqual(org.email, self.apply_f['email'])  # 验证申请邮箱
        STATUS_CHOICES = (
            ('审核中', '审核中'),
            ('审批通过', '审批通过'),
            ('审批不通过', '审批不通过'),
        )
        self.Approve = ORG.Approve.objects.create(org=org, reason='Good', status=STATUS_CHOICES[1])  # 创建审批
        Approves=ORG.Approve.objects.all()
        Approve = Approves[0]
        self.assertEqual(Approve.org, org)  # 验证审批

        pass

class test_year_apply(TestCase):
    """
    测试年审材料提交
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test123', email='1970611068@qq.com', password='test123')
       # self.admin = User.objects.create_superuser(username='admin', email='780531272@qq.com', password='admin123')
        self.client = Client()
        self.email = '1970611068@qq.com'
        self.name = 'cbx'
        self.description = '0'
        # self.apply_f['apply_file'] = SimpleUploadedFile("D:/L/test.txt", b"file_content", content_type="txt")
        # self.apply_f['apply_file'].file_name = 'apply_file'
        # self.apply_f['member_file'] = SimpleUploadedFile("D:/L/test.txt", b"file_content", content_type="txt", )
        # self.apply_f['member_file'].file_name = 'member_file'
        # self.apply_f['manager_info_file'] = SimpleUploadedFile("D:/L/test.txt", b"file_content", content_type="txt", )
        # self.apply_f['manager_info_file'].file_name = 'manager_info_file'
        # self.apply_f['constitution_file'] = SimpleUploadedFile("D:/L/test.txt", b"file_content", content_type="txt", )
        # self.apply_f['constitution_file'].file_name = 'constitution_file'
        # self.apply_f['teacher_confirm_file'] = SimpleUploadedFile("D:/L/test.txt", b"file_content",
        #                                                           content_type="txt", )
        # self.apply_f['teacher_confirm_file'].file_name = 'teacher_confirm_file'
        # self.apply_f['college_confirm_file'] = SimpleUploadedFile("D:/L/test.txt", b"file_content",
        #                                                           content_type="txt", )
        # self.apply_f['college_confirm_file'].file_name = 'college_confirm_file'
        self.org = ORG.Org.objects.create(name=self.name, email=self.email, description=self.description)
        self.Manager = ORG.Manager.objects.create(user=self.user, org=self.org)


    def test_year_apply(self):
        """
          测试提交功能
          """
        response = self.client.login(username='test123', password='test123')  # 登录
        self.assertTrue(response)
        response = self.client.get('/pingshen/add/year/')
        self.assertEqual(response.status_code, 200)
        # login_form=UserForm.LoginForm()
        # login_form.username='test123'
        # login_form.password='test123'
        # response = self.client.post(login_form)

        # with open('D:/L/test.txt') as doc:
        #     apply_f['email'] = '1970611068@qq.com'
        #     apply_f['name'] = 'cbx'
        #     apply_f['description'] = '0'
        #
        #     apply_f['apply_file'] = SimpleUploadedFile("D:/L/test.txt", b"file_content", content_type="txt")
        #     apply_f['member_file'] = doc
        #     apply_f['manager_info_file'] = doc
        #     apply_f['constitution_file'] = doc
        #     apply_f['teacher_confirm_file'] = doc
        #     apply_f['college_confirm_file'] = doc
        #
        #     response = self.client.post('/apply/', apply_f)
        #     self.assertEqual(response.status_code, 302)  # 申请提交后跳转页面

        self.apply_file = SimpleUploadedFile("D:/L/test.txt", b"file_content", content_type="txt")
        self.apply_file.file_name = 'year_apply_file'
        response = self.client.post('/pingshen/add/year/', {'apply_file':self.apply_file})
        self.assertEqual(response.status_code, 302)  # 申请提交后跳转页面
        # org = ORG.Org.objects.filter(name=self.apply_f['name'])
        """
        测试是否提交成功
        """
        YearApproveFile=ORG.YearApproveFile.objects.filter(org=self.org)[0]
        self.assertEqual(YearApproveFile.org, self.org)

        pass

class test_Top10Approve(TestCase):
    """
    测试十佳社团材料提交
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test123', email='1970611068@qq.com', password='test123')
       # self.admin = User.objects.create_superuser(username='admin', email='780531272@qq.com', password='admin123')
        self.client = Client()
        self.email = '1970611068@qq.com'
        self.name = 'cbx'
        self.description = '0'
        self.org = ORG.Org.objects.create(name=self.name, email=self.email, description=self.description)
        self.Manager = ORG.Manager.objects.create(user=self.user, org=self.org)


    def test_top10Approval(self):
        """
          测试提交功能
          """
        response = self.client.login(username='test123', password='test123')  # 登录
        self.assertTrue(response)
        response = self.client.get('/pingshen/add/top10/')
        self.assertEqual(response.status_code, 200)


        self.apply_file = SimpleUploadedFile("D:/L/test.txt", b"file_content", content_type="txt")
        self.apply_file.file_name = 'top10_file'
        response = self.client.post('/pingshen/add/top10/', {'apply_file':self.apply_file})
        self.assertEqual(response.status_code, 302)  # 申请提交后跳转页面
        # org = ORG.Org.objects.filter(name=self.apply_f['name'])
        """
        测试是否提交成功
        """
        top10ApproveFile=ORG.Top10ApproveFile.objects.filter(org=self.org)[0]
        self.assertEqual(top10ApproveFile.org, self.org)

        pass

class test_memberManage(TestCase):
    """
    测试成员管理
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test123', email='1970611068@qq.com', password='test123')
       # self.admin = User.objects.create_superuser(username='admin', email='780531272@qq.com', password='admin123')
        self.client = Client()
        self.email = '1970611068@qq.com'
        self.name = 'cbx'
        self.description = '0'
        # self.apply_f['apply_file'] = SimpleUploadedFile("D:/L/test.txt", b"file_content", content_type="txt")
        # self.apply_f['apply_file'].file_name = 'apply_file'
        # self.apply_f['member_file'] = SimpleUploadedFile("D:/L/test.txt", b"file_content", content_type="txt", )
        # self.apply_f['member_file'].file_name = 'member_file'
        # self.apply_f['manager_info_file'] = SimpleUploadedFile("D:/L/test.txt", b"file_content", content_type="txt", )
        # self.apply_f['manager_info_file'].file_name = 'manager_info_file'
        # self.apply_f['constitution_file'] = SimpleUploadedFile("D:/L/test.txt", b"file_content", content_type="txt", )
        # self.apply_f['constitution_file'].file_name = 'constitution_file'
        # self.apply_f['teacher_confirm_file'] = SimpleUploadedFile("D:/L/test.txt", b"file_content",
        #                                                           content_type="txt", )
        # self.apply_f['teacher_confirm_file'].file_name = 'teacher_confirm_file'
        # self.apply_f['college_confirm_file'] = SimpleUploadedFile("D:/L/test.txt", b"file_content",
        #                                                           content_type="txt", )
        # self.apply_f['college_confirm_file'].file_name = 'college_confirm_file'
        self.org = ORG.Org.objects.create(name=self.name, email=self.email, description=self.description)
        self.Manager = ORG.Manager.objects.create(user=self.user, org=self.org)

    def test_member_manager(self):
        """
          测试成员管理
          """
        response = self.client.login(username='test123', password='test123')  # 登录
        self.assertTrue(response)
        response = self.client.get('/member/add/')
        self.assertEqual(response.status_code, 200)
        # login_form=UserForm.LoginForm()
        # login_form.username='test123'
        # login_form.password='test123'
        # response = self.client.post(login_form)

        # with open('D:/L/test.txt') as doc:
        #     apply_f['email'] = '1970611068@qq.com'
        #     apply_f['name'] = 'cbx'
        #     apply_f['description'] = '0'
        #
        #     apply_f['apply_file'] = SimpleUploadedFile("D:/L/test.txt", b"file_content", content_type="txt")
        #     apply_f['member_file'] = doc
        #     apply_f['manager_info_file'] = doc
        #     apply_f['constitution_file'] = doc
        #     apply_f['teacher_confirm_file'] = doc
        #     apply_f['college_confirm_file'] = doc
        #
        #     response = self.client.post('/apply/', apply_f)
        #     self.assertEqual(response.status_code, 302)  # 申请提交后跳转页面
        self.add_form={}
        self.add_form['name']='cbx'
        self.add_form['stu_no'] = 984
        self.add_form['_class'] = 8
        self.add_form['role'] = 'member'
        self.add_form['remark'] = '无'
        self.add_form['join_date'] ='2021-12-24'
        response = self.client.post('/member/add/', self.add_form)
        self.assertEqual(response.status_code, 302)  # 申请提交后跳转页面
        # org = ORG.Org.objects.filter(name=self.apply_f['name'])
        """
        测试是否添加成功
        """
        Member=ORG.Member.objects.filter(org=self.org)[0]
        self.assertEqual(Member.name, self.add_form['name'])
        pass

class NewsTestCase(TestCase):
    def setUp(self):
        self.title = '清社圈测试304'
        self.content = '清社圈公告发布测试'
        self.create_at = timezone.now()
        self.admin = User.objects.create_superuser(username='admin', email='1053212017@qq.com', password='admin123')
        self.client = Client()

    def test_news(self):
        News.objects.create(title=self.title, content=self.content)
        news = News.objects.filter(title=self.title)
        news = news[0]
        self.assertEqual(news.title, self.title)
        response=self.client.get('/news/list/')
        self.assertEqual(response.status_code, 200)
        content=response.content.decode()
        self.assertTrue('清社圈测试304' in content)
        pass
