# -*- coding: utf-8 -*-

"""用户相关的表单验证"""

import re

from django import forms
from django.contrib.auth.hashers import check_password

from user.models import User


class RegisterForm(forms.Form):
    """注册表单验证"""
    user_name = forms.CharField(max_length=20, min_length=5, required=True,
                                error_messages={'required': '用户名必填', 'max_length': '最长不能超过20个字符', 'min_length': '最少不能少于5个字符'})
    pwd = forms.CharField(max_length=20, min_length=8, required=True,
                                error_messages={'required': '密码必填', 'max_length': '最长不能超过20个字符', 'min_length': '最少不能少于8个字符'})
    allow = forms.BooleanField(required=True, error_messages={'required': '必须统一协议'})
    cpwd = forms.CharField(max_length=20, min_length=5, required=True,
                                error_messages={'required': '确认密码必填', 'max_length': '最长不能超过20个字', 'min_length': '最少不能少于8个字'})
    email = forms.CharField(required=True, error_messages={'required': '邮箱必填'})

    def clean_user_name(self):
        #  校验注册的账号是否已存在
        username = self.cleaned_data.get('user_name')
        user = User.objects.filter(username=username).first()
        if user:
            raise forms.ValidationError('该用户已注册')
        return self.cleaned_data['user_name']

    def clean(self):
        #   密码和确认密码的判断
        pwd = self.cleaned_data.get('pwd')
        cpwd = self.cleaned_data.get('cpwd')
        if pwd != cpwd:
            raise forms.ValidationError({'cpwd': '两次密码不一致'})
        return self.cleaned_data

    def clean_email(self):
        #  校验邮箱格式
        email_reg = '^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$'
        email = self.cleaned_data.get('email')
        if not re.match(email_reg, email):
            raise forms.ValidationError('邮箱格式错误')
        return self.cleaned_data['email']


class LoginForm(forms.Form):
    """登录表单验证"""
    username = forms.CharField(max_length=20, min_length=5, required=True,
                                error_messages={'required': '用户名必填', 'max_length': '最长不能超过20个字符', 'min_length':'最少不能少于5个字符'})
    pwd = forms.CharField(max_length=20, min_length=8, required=True,
                          error_messages={'required': '密码必填', 'max_length': '最长不能超过20个字符', 'min_length': '最少不能少于8个字符'})

    def clean(self):
        #  校验用户名是否注册,密码是否正确
        username = self.cleaned_data.get('username')
        if username:
            user = User.objects.filter(username=username).first()
            if not user:
                raise forms.ValidationError({'username': '亲，该账号没有注册哦'})
            password = self.cleaned_data.get('pwd')
            if not check_password(password, user.password):
                raise forms.ValidationError({'pwd': '密码错误'})
        return self.cleaned_data


class AddressForm(forms.Form):
    """编辑地址表单校验"""
    username = forms.CharField(max_length=10, min_length=2, required=True, error_messages={'required': '收件人必填',
                                                                           'max_length': '收件人姓名不超过5个字'})
    address = forms.CharField(required=True, error_messages={'required': '地址必填'})
    postcode = forms.CharField(required=True, error_messages={'required': '邮编必填'})
    mobile = forms.CharField(required=True, error_messages={'required': '手机必填'})

    # def clean(self):
    #     username = self.cleaned_data['username']
    #     address = self.cleaned_data['address']
    #     postcode = self.cleaned_data['postcode']
    #     mobile = self.cleaned_data['mobile']
    #     if username