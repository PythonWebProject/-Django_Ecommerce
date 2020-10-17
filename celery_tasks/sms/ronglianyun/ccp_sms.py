import json

from ronglian_sms_sdk import SmsSDK

accId = '8a216da874af5fff0174fbf69e2818f1'
accToken = 'b2ffad0c9bc44d68ac2fa577ddb3ee1a'
appId = '8a216da874af5fff0174fbf69f1318f8'


class CCP(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.sdk = SmsSDK(accId, accToken, appId)
        return cls._instance

    def send_message(self, mobile, datas, tid):
        resp = self._instance.sdk.sendMessage(tid, mobile, datas)
        resp = json.loads(resp)
        if resp['statusCode'] == '000000':
            return 0
        else:
            return -1


if __name__ == '__main__':
    ccp = CCP()
    tid = '1'
    mobile = '173xxxxxxxx'
    datas = ('111111', 5)
    res = ccp.send_message(mobile, datas, tid)
    print(res)
