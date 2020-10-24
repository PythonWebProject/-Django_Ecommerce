import re

from django.contrib.auth.backends import ModelBackend

from .models import User


def get_user_by_account(account):
    '''
    获取用户对象
    :param account: 用户名或手机号
    :return: user
    '''
    try:
        if re.match(r'1[3-9]\d{9}', account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    except:
        return None
    else:
        return user

class UsernameMobileBackend(ModelBackend):
    '''自定义用户认证后端'''
    def authenticate(self, request, username=None, password=None, **kwargs):
        '''
        重写认证方法
        :param username: 用户名或手机号
        :param password: 密码明文
        :param kwargs: 额外参数
        :return: user
        '''
        user = get_user_by_account(username)
        if user and user.check_password(password):
            return user
        else:
            return None
