from django.shortcuts import render
from django.views import View

class RegisterView(View):
    '''用户注册'''
    def get(self, request):
        '''提供用户注册页面'''
        return render(request, 'register.html')

    def post(self, request):
        '''提供用户注册逻辑'''
        pass