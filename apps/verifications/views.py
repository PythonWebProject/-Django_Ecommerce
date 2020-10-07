import random

from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.views import View
from django_redis import get_redis_connection

from .libs.captcha.captcha import captcha
from .libs.ronglianyun.ccp_sms import CCP
from .constants import *
from utils.response_code import RETCODE, err_msg


class ImageCodeView(View):
    '''图形验证码'''

    def get(self, request, uuid):
        '''
        :param uuid: 表示图形验证码属于哪个用户
        :return: image/jpg
        '''
        # 生成图形验证码
        text, image = captcha.generate_captcha()
        # 保存到Redis
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex('img_%s' % uuid, IMAGE_CODE_REDIS_EXPIRES, text)
        # 响应
        return HttpResponse(image, content_type='image/jpg')


class SMSCodeView(View):
    '''短信验证码'''

    def get(self, request, mobile):
        '''
        :param mobile: 手机号
        :return: JSON
        '''
        # 接收查询字符串参数
        image_code_client = request.GET.get('image_code')
        uuid = request.GET.get('uuid')
        # 校验
        if not all([image_code_client, uuid]):
            return HttpResponseForbidden('缺少必传参数')
        # 提取和删除图形验证码
        redis_conn = get_redis_connection('verify_code')
        image_code_server = redis_conn.get('img_%s' % uuid).decode()
        redis_conn.delete('img_%s' % uuid)
        # 对比图形验证码
        if image_code_client.lower() != image_code_server.lower():
            return JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': err_msg.get(RETCODE.IMAGECODEERR)})
        # 生成6位短信验证码并保存
        sms_code = str(random.randint(100000, 999999))
        redis_conn.setex('sms_%s' % mobile, SMS_CODE_REDIS_EXPIRES, sms_code)
        # 发送短信验证码
        CCP().send_message(mobile, (sms_code, SMS_CODE_REDIS_EXPIRES//60), SEND_SMS_EMPLATE_ID)
        # 响应结果
        return JsonResponse({'code': RETCODE.OK, 'errmsg': err_msg.get(RETCODE.OK)})