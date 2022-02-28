from django import forms
from django_summernote.fields import SummernoteTextFormField



class UserForm(forms.Form):
    user_id = forms.CharField(label='学工号', max_length=25, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                         'placeholder': 'Username', 'autofoucs': ''}))
    password = forms.CharField(label='密码', max_length=25, widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                            'placeholder': 'Password'}))
    # captcha = CaptchaField(label='验证码')


class RegisterForm(forms.Form):
    gender = (
        ('male', '男'),
        ('female', '女'),
    )
    identifies = (('student','学生'),('teacher','教师'),('admin','管理员'),)
    name = forms.CharField(label='姓名', max_length=25,widget=forms.TextInput(attrs={'class': 'form-control'}))
    user_id = forms.CharField(label='学工号', max_length=25, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='密码', max_length=25, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='确认密码', max_length=25, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='邮箱地址', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    grade = forms.CharField(label='年级',max_length=25,widget=forms.TextInput(attrs={'class': 'form-control'}))
    academy = forms.CharField(label='学院',max_length=25,widget=forms.TextInput(attrs={'class': 'form-control'}))
    specialty = forms.CharField(label='专业',max_length=25,widget=forms.TextInput(attrs={'class': 'form-control'}))
    identify = forms.ChoiceField(label='身份',choices=identifies,widget=forms.Select(attrs={'class': 'form-control'}))
    # captcha = CaptchaField(label='验证码',)



class PostForm(forms.Form):
    content = SummernoteTextFormField()