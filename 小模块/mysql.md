授权sql

```
mysql> grant all privileges on test.* to 'user'@ip_addr' identified by 'root' with grant option
```



### 用户表

#### 个人信息

>1. id（primary key)
>2. 用户名
>3. 密码
>4. 邮箱
>5. 是否激活
>6. 权限标识

#### 收件地址表

>1. id
>2. 收件人
>3. 邮编
>4. 地址
>5. 是否默认地址
>6. 用户id(foreign key)



<hr>

### 商品表

#### 商品SKU表

>1. id
>2. 名称
>3. 简介
>4. 详情
>5. 价格
>6. 单位
>7. 库存
>8. 图片(1)
>9. 评论
>10. 销量
>11. 状态标识
>12. 种类id(foreign key)
>13. SPU id(foreign key)

#### 商品SPU表

>1. id
>2. 名称
>3. 详情

#### 商品种类表

>1. id
>2. 名称
>3. 图片
>4. login

#### 商品图片表

>1. id
>2. url
>3. sku id(foreign key)

#### 首页分类商品表

>1. id
>2. image
>3. display_flag
>4. index
>5. 种类id(foreign key)

<hr>

#### 轮播表

> 1. id
> 2. inde
> 3. image
> 4. sku id(foreign key)

#### 促销活动表

> 1. id
> 2. image
> 3. url
> 4. index

<hr>

### 订单信息

#### 订单信息

>1. 订单id
>2. 地址id
>3. 支付方式
>4. 商品列表
>5. 运费
>6. ]总金额]
>7. 支付状态
>8. 创建时间

#### 订单商品表

>1. id
>2. 商品sku id
>3. 数量
>4. 下单价格
>5. 评论

#### 商品图片表

>1. id
>2. 商品sku id
>3. image



### 购物车

用redis实现，以及顾客最近浏览订单