from django.shortcuts import render
from django.views import View
from django.http import HttpResponse


class ImageCodeView(View):
    '''图形验证码'''

    def get(self, request, uuid):
        '''
        :param uuid: 表示图形验证码属于哪个用户
        :return: image/jpg
        '''
        return HttpResponse('图形验证码')