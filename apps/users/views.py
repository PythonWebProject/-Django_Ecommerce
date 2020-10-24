from django.shortcuts import render, redirect, reverse
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django_redis import get_redis_connection

from .forms import RegisterForm, LoginForm
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
            sms_code_client = form.cleaned_data.get('sms_code')
            # 判断短信验证码是否正确
            redis_conn = get_redis_connection('verify_code')
            sms_code_server = redis_conn.get('sms_%s' % mobile)
            if sms_code_server is None:
                return render(request, 'register.html', {'sms_code_errmsg': '短信验证码已失效'})
            if sms_code_client != sms_code_server.decode():
                return render(request, 'register.html', {'sms_code_errmsg': '短信验证码有误'})
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


class LoginView(View):
    '''用户名登录'''

    def get(self, request):
        '''
        提供登录页面
        :return: 登录页面
        '''
        return render(request, 'login.html')

    def post(self, request):
        '''
        实现登录逻辑
        '''
        # 验证表单
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 接收参数
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            remembered = request.POST.get('remembered')
            # 认证登录用户
            user = authenticate(username=username, password=password)
            if user is None:
                # 用户名或密码输入错误
                return render(request, 'login.html', {'errmsg': '账号不存在或密码错误'})
            # 状态保持
            login(request, user)
            if remembered != 'on':
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(None)
            response = redirect(reverse('contents:index'))
            response.set_cookie('username', user.username, max_age=60*60*24*14)
            return response
        else:
            print(login_form.errors.get_json_data())
            context = {
                'forms_errors': login_form.errors
            }
            return render(request, 'login.html', context=context)
