from django import forms

from .models import User

class RegisterForm(forms.Form):
    username = forms.CharField(min_length=5, max_length=20, error_messages={'min_length': '用户名过短', 'max_length': '用户名过长'})
    password = forms.CharField(min_length=8, max_length=20, error_messages={'min_length': '密码过短', 'max_length': '密码过长', 'required': '密码必填'})
    password2 = forms.CharField(min_length=8, max_length=20)
    allow = forms.BooleanField()
    mobile = forms.CharField(min_length=11, max_length=11, required=True, error_messages={'min_length': '手机号应为11位', 'max_length': '手机号应为11位', 'required': '手机号必填'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        username_exists = User.objects.filter(username=username).first()
        if username_exists:
            raise forms.ValidationError('用户名已经存在')
        return username

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        mobile_exists = User.objects.filter(mobile=mobile).first()
        if mobile_exists:
            raise forms.ValidationError('手机号已经存在')
        return mobile

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('两次密码不一致')
        return cleaned_data