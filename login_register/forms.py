from django import forms
from captcha.fields import CaptchaField, CaptchaTextInput


class Login_Form(forms.Form):
    captcha = CaptchaField(label='验证码', widget=CaptchaTextInput(attrs={'class': 'form-control'}))