1. 获取某一class标签的子元素值`children`

   ```
   #$('.show_price').children('em').text()
   <span class="show_price">¥<em>{{ sku.price }}</em></span>
   ```

2. 有value值，直接获取`val`并可以直接设置

   ```
   #$('.num_show').val()
   <input type="text" class="num_show fl" value="1">
   $('.num_show').val(value)
   ```

3. 数转化`parse`

   ```
   price = $('.show_price').children('em').text()
   price = parseFloat(price)
   count = parseInt(count)
   ```

4. 固定数值`toFixed`

   ```
   $('.show_price').children('em').text(value.toFixed(2))
   ```

5. click触发函数

   ```
   $('.button_class').click(function (){
   	    #TODO
   	}
   )
   ```

6. 输入框失去焦点时执行

   ```
   $('.class_name').blur(function(){
   	#todo
   })
   ```

7. 之前获取过类名，直接用this

   ```
   $('.class_name').blur(function(){
   	$(this).value
   })
   ```

8. 判断非数字

   ```
   isNaN(num), 非数字返回真
   ```

9. id调用

   ```
   $('#id_name')
   ```

10. 动态添加属性sku_id

    ```
    <a href="javascript:;" sku_id="{{ sku.id }}" class="add_cart" id="add_cart">加入购物车</a>
    #访问
    sku_id = $(this).attr('sku_id')
    ```

11. 调用post

    ```
    $.post('/cart/add', params, function (data) {
    	#todo
    }
    ```

12. post提交需要提交csrf_token

    ```
    csrf = $('input[name="csrfmiddlewaretoken"]').val()
    ```

13. 找到父辈类型

    ```
    $('.settlements').find(':checkbox').parents('ul')
    ```

14. 找到孙子的类型

    ```
    $('.settlements').find(':checkbox').change(function(){})
    
    <ul class="settlements">
            {% csrf_token %}
    		<li class="col01"><input type="checkbox" name="" checked=""></li> #the line
    		<li class="col02">全选</li>
    		<li class="col03">合计(不含运费)：<span>¥</span><em>{{ total_price }}</em><br>共计<b>{{ total_count }}</b>件商品</li>
    		<li class="col04"><input type="submit" value="去结算"></li>
    	</ul>
    ```

15. 获取属性值

    ```
    $(.this).prop('checked', false)#默认为true
    ```

16. 遍历

    ```
    $('.settlements').find(':checkbox').each(function(){})
    ```

17. 获取checkbox所有的条目

    ```
    $('.id').length
    ```

    