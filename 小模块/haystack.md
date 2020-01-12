1. 安装

   ```
   (venv) [ms@localhost ttsx_exercide]$ pip install django-haystack
   (venv) [ms@localhost ttsx_exercide]$ pip install whoosh
   ```

2. 注册应用

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi ttsx_exercide/settings.py 
   ```

   #settings.py

   ```
   INSTALLED_APPS = [
       ...
       'tinymce',
       'haystack',#add the line
   ]
   
   
   # 全文检索框架的配置
   HAYSTACK_CONNECTIONS = {
       'default': {
           # 使用whoosh引擎
           'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
           #'ENGINE': 'haystack.backends.whoosh_cn_backend.WhooshEngine',
           # 索引文件路径
           'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
       }
   }
   
   # 当添加、修改、删除数据时，自动生成索引
   HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
   
   # 指定搜索结果每页显示的条数
   HAYSTACK_SEARCH_RESULTS_PER_PAGE=1
   ```

3. 建立索引字段,以商品goods为例

   添加固定文件名

   ```
   (venv) [ms@localhost ttsx_exercide]$ touch apps/goods/search_indexes.py
   ```

   #search_indexes.py

   ```
   # 定义索引类
   from haystack import indexes
   # 导入模型类
   from goods.models import GoodsSKU
   
   # 指定对于某个类的某些数据建立索引
   # 索引类名格式:模型类名+Index
   class GoodsSKUIndex(indexes.SearchIndex, indexes.Indexable):
       # 索引字段 use_template=True指定根据表中的哪些字段建立索引文件的说明放在一个文件中
       text = indexes.CharField(document=True, use_template=True)
   
       def get_model(self):
           # 返回你的模型类
           return GoodsSKU
   
       # 建立索引的数据
       def index_queryset(self, using=None):
           return self.get_model().objects.all()
   ```

   指定列名搜索，建立固定名字文件夹和文件

   ```
   (venv) [ms@localhost ttsx_exercide]$ mkdir -p templates/search/indexes/goods/
   (venv) [ms@localhost ttsx_exercide]$ vi templates/search/indexes/goods/goodssku_text.txt
   ```

   #goodssku_text.txt

   ```
   # 指定根据表中的哪些字段建立索引数据
   {{ object.name }} # 根据商品的名称建立索引
   {{ object.desc }} # 根据商品的简介建立索引
   {{ object.goods.detail }} # 根据商品的详情建立索引
   ```

4. 根据关键列名建立索引

   ```
   (venv) [ms@localhost ttsx_exercide]$ python manage.py rebuild_index
   ```

5. 修改urls.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi ttsx_exercide/urls.py
   ```

   #urls.py

   ```
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('tinymce/', include('tinymce.urls')),
       path('search/', include('haystack.urls')), #add the line
       ...
   ]
   ```

6. 修改搜索前端页面，加入表单

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi templates/base.html 
   ```

   #base.html

   ```
   <form action='search/' method='get'>
                   <input type="text" class="input_text fl" name="q" placeholder="搜索商品">
                   <input type="submit" class="input_btn fr" name="" value="搜索">
               </form>
   ```

7. 修改search.html

   ```
   (venv) [ms@localhost ttsx_exercide]$ cp  templates/list.html template/search/search.html
   (venv) [ms@localhost ttsx_exercide]$vi template/search/search.html
   ```

   #search.html

   ```
   #主要修改那内容
   <ul class="goods_type_list clearfix">
               {% for item in page %}
               <li>
                   <a href="{% url 'goods:detail' item.object.id %}"><img src="{{ item.object.image.url }}"></a>
                   <h4><a href="{% url 'goods:detail' item.object.id %}">{{ item.object.name }}</a></h4>
                   <div class="operate">
                       <span class="prize">￥{{ item.object.price }}</span>
                       <span class="unit">{{ item.object.price}}/{{ item.object.unite }}</span>
                       <a href="#" class="add_goods" title="加入购物车"></a>
                   </div>
               </li>
               {% endfor %}
           </ul>
           <div class="pagenation">
                   {% if page.has_previous %}
   				<a href="/search?q={{ query }}&page={{ page.previous_page_number }}"><上一页</a>
                   {% endif %}
                   {% for pindex in paginator.page_range %}
                       {% if pindex == page.number %}
   				        <a href="/search?q={{ query }}&page={{ pindex }}" class="active">{{ pindex }}</a>
                       {% else %}
   				        <a href="/search?q={{ query }}&page={{ pindex }}">{{ pindex }}</a>
                       {% endif %}
   				{% endfor %}
                   {% if spage.has_next %}
   				<a href="/search?q={{ query }}&page={{ page.next_page_number }}">下一页></a>
                   {% endif %}
   			</div>
   ```

8. 测试

9. 修改解词包，用jieba分词代替，更好的中文支持

   ```
   (venv) [ms@localhost ttsx_exercide]$ pip install jieba
   ```

   进入虚拟环境haystack目录

   ```
   (venv) [ms@localhost backends]$ cd 
   /home/ms/Documents/venv/lib/python3.7/site-packages/haystack/backends
   ```

   创建中文解包类

   ```
   (venv) [ms@localhost backends]$ vi ChineseAnalyzer.py
   ```

   #ChineseAnalyzer.py

   ```
   import jieba
   from whoosh.analysis import Tokenizer, Token
   
   class ChineseTokenizer(Tokenizer):
       def __call__(self, value, positions=False, chars=False,
                    keeporiginal=False, removestops=True,
                    start_pos=0, start_char=0, mode='', **kwargs):
           t = Token(positions, chars, removestops=removestops, mode=mode, **kwargs)
           seglist = jieba.cut(value, cut_all=True)
           for w in seglist:
               t.original = t.text = w
               t.boost = 1.0
               if positions:
                   t.pos = start_pos + value.find(w)
               if chars:
                   t.startchar = start_char + value.find(w)
                   t.endchar = start_char + value.find(w) + len(w)
               yield t
   
   def ChineseAnalyzer():
       return ChineseTokenizer()
   ```

   拷贝whoosh_backend.py

   ```
   (venv) [ms@localhost backends]$ cp whoosh_backend.py whoosh_cn_backend.py
   ```

   打开whoosh_cn_backend.py

   ```
   (venv) [ms@localhost backends]$ vi whoosh_cn_backend.py 
   ```

   #whoosh_cn_backend.py

   ```
   from .ChineseAnalyzer import ChineseAnalyzer
   ```

   `analyzer=StemmingAnalyzer()`替换为`analyzer=ChineseAnalyzer()`

   修改settings.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi ttsx_exercide/settings.py
   ```

   #settings.py

   ```
   # 全文检索框架的配置
   HAYSTACK_CONNECTIONS = {
       'default': {
           # 使用whoosh引擎
           'ENGINE': 'haystack.backends.whoosh_cn_backend.WhooshEngine', #use whoosh_cn_backend
           # 索引文件路径
           'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
       }
   }
   ```

10. 重现创建索引数据

    ```
    (venv) [ms@localhost ttsx_exercide]$ python manage.py rebuild_index
    ```

    

