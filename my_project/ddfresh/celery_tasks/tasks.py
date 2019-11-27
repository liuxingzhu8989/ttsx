from celery import Celery
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.template import loader,RequestContext
from django.views.generic import View
from django_redis import get_redis_connection

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ddfresh.settings')
django.setup()

from goods.models import GoodsType, IndexGoodsBanner, IndexTypeGoodsBanner,IndexPromotionBanner
app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/0')

@app.task
def send_email_to_verify(email, username, token):
    subject='ttsx'
    message=''
    sender = settings.EMAIL_FROM
    receiver = [email]
    html_message = '<h1>%s</h1><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1/user/active/%s</a>'%(username,token,token)

    send_mail(subject, message, sender, receiver, html_message=html_message)

@app.task
def generate_index_page():
    types = GoodsType.objects.all()
    goods_banners = IndexGoodsBanner.objects.all()
    type_goods_banners = IndexTypeGoodsBanner.objects.all().order_by('index')
    promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

    context = {'types':types,
                'goods_banners': goods_banners,
                'type_goods_banners': type_goods_banners,
                'promotion_banners':promotion_banners,
              }

    temp = loader.get_template('static_index.html')
    index_static = temp.render(context)
    
    save_path = os.path.join(settings.BASE_DIR, 'static/index.html')    
    with open(save_path, "w") as f:
        f.write(index_static)
