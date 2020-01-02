from celery import Celery
from django.core.mail import send_mail
from django.conf import settings

#设置django环境, 先设置，然后再导入models
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ttsx_exercide.settings')
django.setup()

from goods.models import GoodsType, IndexGoodsBanner, IndexTypeGoodsBanner,IndexPromotionBanner
app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/1')

@app.task
def send_email_to_verify(email, username, token):
    subject='ttsx'
    message=''
    sender = settings.EMAIL_FROM
    receiver = [email]
    html_message = '<h1>%s</h1><a href="http://127.0.0.1:9001/user/active/%s">http://127.0.0.1/user/active/%s</a>'%(username,token,token)

    send_mail(subject, message, sender, receiver, html_message=html_message)
