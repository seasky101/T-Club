
from django import forms
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    """
    登录表单
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}), label='用户名')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label='密码')
    # captcha = CaptchaField(label='验证码') # 验证码

    class Meta:
        # model = User
        fields = ('username', 'password', )
    
    def clean_password(self):
        """
        验证密码
        """
        cd = self.cleaned_data
        user = authenticate(request=None, username = cd['username'], password=cd['password']) # 验证
        if user is not None:
            if not user.is_active:
                raise forms.ValidationError('user is not active')
            return cd['password']
        else:
            raise forms.ValidationError('username or password is valid')

class RegisterForm(forms.ModelForm):
    """
    注册
    """
    email = forms.EmailField(widget=forms.EmailInput(), label="邮箱")
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    repassword = forms.CharField(label='确认密码', widget=forms.PasswordInput)
    captcha = CaptchaField(label="验证码") # 验证码

    class Meta:
        model = User
        fields = ('username', 'email', 'password', )

    def clean_repassword(self):
        cd = self.cleaned_data
        if cd['password'] != cd['repassword']:
            raise forms.ValidationError('the two password are not the same')
        return cd['repassword']

class PasswordForm(forms.Form):
    """
    修改密码
    """
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    repassword = forms.CharField(label='Repassword', widget=forms.PasswordInput)
    captcha = CaptchaField() # 验证码

    def clean_repassword(self):
        cd = self.cleaned_data
        if cd['password'] != cd['repassword']:
            raise forms.ValidationError('the two password are not the same')
        return cd['repassword']
