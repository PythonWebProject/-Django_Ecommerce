'''
定义任务
'''

from ..main import celery_app
from .ronglianyun.ccp_sms import CCP
from .constants import *


@celery_app.task(name='send_sms_code')  # 保证celery可以识别任务
def send_sms_code(mobile, sms_code):
    '''
    发送短信验证码异步任务
    :param mobile: 手机号
    :param sms_code: 短信验证码
    :return: 成功返回0，失败返回-1
    '''
    result = CCP().send_message(mobile, (sms_code, SMS_CODE_REDIS_EXPIRES // 60), SEND_SMS_EMPLATE_ID)
    return result
