1. 修改views.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi apps/goods/views.py 
   ```

   #views.py

   ```
   from django.shortcuts import render
   from django.views.generic import View
   from django_redis import get_redis_connection #add the line
   
   class IndexView(View):
       def get(self, request):
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
   	
           cart_count = 0
   
           conn = get_redis_connection('default')
           user = request.user
           if user.is_authenticated:
               cart_key = 'cart_%d'%user.id
               cart_count = conn.hlen(cart_key)
   
           context = {'types': types,
                      'goods_banners': goods_banners,
                      'promotion_banners': promotion_banners,
                      'cart_count':cart_count} #add cart_count
   
           return render(request, 'index.html', context)
   ```

2. 修改urls.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi apps/goods/urls.py 
   ```

   #urls.py

   ```
   from django.urls import path
   from goods.views import IndexView
   
   app_name = 'goods'
   urlpatterns = [
       path('index/', IndexView.as_view(), name ='index'),
   ```

3. 修改index.html

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi templates/index.html 
   ```

   #index.html

   ```
   {% extends 'base.html' %}
   {% load staticfiles %}
   {% block title %}天天生鲜-首页 {% endblock title %}
   {% block topfiles %}
   	<script type="text/javascript" src="{% static 'js/jquery-1.12.4.min.js' %}"></script>
   	<script type="text/javascript" src="{% static 'js/jquery-ui.min.js' %}"></script>
   	<script type="text/javascript" src="{% static 'js/slide.js' %}"></script>
   {% endblock topfiles %}
   {% block body %}
   	<div class="navbar_con">
   		<div class="navbar">
   			<h1 class="fl">全部商品分类</h1>
   			<ul class="navlist fl">
   				<li><a href="">首页</a></li>
   				<li class="interval">|</li>
   				<li><a href="">手机生鲜</a></li>
   				<li class="interval">|</li>
   				<li><a href="">抽奖</a></li>
   			</ul>
   		</div>
   	</div>
   
   	<div class="center_con clearfix">
   		<ul class="subnav fl">
               {% for type in types %}
   			<li><a href="#model0{{ forloop.counter }}" class="{{ type.logo }}">{{type.name }}</a></li>
               {% endfor %}
   		</ul>
   		<div class="slide fl">
   			<ul class="slide_pics">
                   {% for banner in goods_banners  %}
                       <li><a href="#"><img src="{{ banner.image.url }}" alt="{{ banner.image }}"></a></li>
                   {% endfor %}
   			</ul>
   			<div class="prev"></div>
   			<div class="next"></div>
   			<ul class="points"></ul>
   		</div>
   		<div class="adv fl">
               {% for banner in promotion_banners %}
                   <a href="{{ banner.url }}"><img src="{{ banner.image.url }}"></a>
               {% endfor %}
   		</div>
   	</div>
   
       {% for type in types %}
   	<div class="list_model">
   		<div class="list_title clearfix">
   			<h3 class="fl" id="model0{{forloop.counter}}">{{type.name}}</h3>
   			<div class="subtitle fl">
   				<span>|</span>
                   {% for banner in type.title_banners %}
                       <a href="#">{{ banner.sku.name }}</a>
                   {% endfor %}
   			</div>
   			<a href="#" class="goods_more fr" id="fruit_more">查看更多 ></a>
   		</div>
   
   		<div class="goods_con clearfix">
   			<div class="goods_banner fl"><img src="{{ type.image.url }}"></div>
   			<ul class="goods_list fl">
                   {% for banner in type.image_banners %}
                   <li>
                       <h4><a href="#">{{ banner.sku.name }}</a></h4>
                       <a href="#"><img src="{{ banner.sku.image.url }}"></a>
                       <div class="prize">¥ {{ banner.sku.price }}</div>
                   </li>
                   {% endfor %}
   			</ul>
   		</div>
   	</div>
       {% endfor %}
   {% endblock body %}
   ```
   
4. 测试

   1. mysql查看user table表，查看user_id
   2. 进入redis,用hmset cart_userid 1 1 2 2设置值
   3. 刷新index界面，观察购物车记录是否更改

