'''
Celery入口
'''

from celery import Celery

# 创建celery实例
celery_app = Celery('cl')

# 加载配置文件
celery_app.config_from_object('celery_tasks.config')

# 自动注册celery任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])