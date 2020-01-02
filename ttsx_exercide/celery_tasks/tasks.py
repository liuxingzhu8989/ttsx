from celery import Celery
from django.core.mail import send_mail
from django.conf import settings

#静态页面
from django.template import loader, RequestContext

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

@app.task
def generate_static_index():
        types = GoodsType.objects.all()
        # 获取首页轮播商品信息
        goods_banners = IndexGoodsBanner.objects.all()
        # 获取首页促销活动信息
        promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

        for type in types: # GoodsType
                # 获取type种类首页分类商品的图片展示信息
                image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
                # 获取type种类首页分类商品的文字展示信息
                title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')

                # 动态给type增加属性，分别保存首页分类商品的图片展示信息和文字展示信息
                type.image_banners = image_banners
                type.title_banners = title_banners

        context = {'types': types,
                   'goods_banners': goods_banners,
                   'promotion_banners': promotion_banners,}

        temp = loader.get_template('static_index.html')
        static_index_html = temp.render(context)
        save_path = os.path.join(settings.BASE_DIR, 'static/index.html')
        with open(save_path, 'w') as f:
            f.write(static_index_html)
