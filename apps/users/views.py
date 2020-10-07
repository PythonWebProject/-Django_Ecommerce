from django.shortcuts import render, redirect, reverse
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login

from .forms import RegisterForm
from .models import User
from utils.response_code import RETCODE, err_msg

class RegisterView(View):
    '''用户注册'''
    def get(self, request):
        '''提供用户注册页面'''
        return render(request, 'register.html')

    def post(self, request):
        '''提供用户注册逻辑'''
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            mobile = form.cleaned_data.get('mobile')
            try:
                user = User.objects.create_user(username=username, password=password, mobile=mobile)
            except:
                return render(request, 'register.html', {'register_error_message': '注册失败'})
            # 实现状态保持
            login(request, user)
            return redirect(reverse('contents:index'))
        else:
            print(form.errors.get_json_data())
            context = {
                'forms_errors': form.errors
            }
            return render(request, 'register.html', context=context)


class UsernameExists(View):
    '''判断用户名是否存在'''
    def get(self, request, username):
        '''
        :param username: 用户名
        :return: json
        '''
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': RETCODE.OK, 'errmsg': err_msg.get('OK'), 'count': count})


class MobileExists(View):
    '''判断手机号是否存在'''
    def get(self, request, mobile):
        '''
        :param username: 用户名
        :return: json
        '''
        count = User.objects.filter(mobile=mobile).count()
        return JsonResponse({'code': RETCODE.OK, 'errmsg': err_msg.get('OK'), 'count': count})