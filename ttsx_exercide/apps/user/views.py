from django.shortcuts import render, redirect
from django.urls import reverse

from util.mixin import LoginRequiredMixin

#html_page_str
 #RegisterView,LoginView
register_html = "register.html"
login_html = "login.html"
index_html = "index.html"

 #InfoView, OrderView, SiteView
user_info  = 'user_center_info.html'
user_order = 'user_center_order.html'
user_site  = 'user_center_site.html'

#RegisterView
from django.views.generic import View
from user.models import User, Address

#LoginView, LogOutView
from django.contrib.auth import authenticate, login, logout

#Redis as cache
from django_redis import get_redis_connection

class RegisterView(View):
    def get(self, request):
        return render(request, register_html)

    def post(self,request):
        #1.获取数据
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")
        email    = request.POST.geet("email")

        #2.校验数据
        if not all((username, password, email)):
            return render(request, register_html, {'errsg':'username/passwd/email is missing'})

        #3.业务处理
        try:
            user = User.objects.get(username = username) #user可能拿不到数据
        except User.DoesNotExist:
            user = None

        if not user:
            user = User.objects.create_user(username, email, password)
            user.save()

        #发送激活邮件
        #TODO 

        return render(request, login_html)

class LoginView(View):
    def get(self, request):
            if 'username' in request.COOKIES:
                username =  request.COOKIES.get('username')
                checked  = "checked"
            else:
                username = ""
                checked  = ""
    
            return render(request, login_html, {"username":username, "checked":checked})

    def post(self, request):
        #1.获取数据
        username = request.POST.get("username")
        password = request.POST.get("pwd")

        #2.校验数据
        if not all((username, password)):
            return render(request, login_html, {'errmsg':'username/passwd should not be none'})

        user = authenticate(username=username, password = password)
        if user:
            if user.is_active:
                login(request, user)
                remember = request.POST.get('remember') #add all 7 lines
                next_url = request.GET.get('next', reverse("goods:index"))
                res = redirect(next_url) 
                if remember == 'on':
                    res.set_cookie('username', username, 7*24*3600)
                else:
                    res.delete_cookie('username')
                return res
            else:
                return render(request, login_html)
        else:
            return render(request, login_html)

class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse("goods:index"))

#/user/info
class InfoView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        address = Address.objects.get_default_address(user)

        con = get_redis_connection("default")
        history_key = 'history_user%d'%user.id
        sku_ids = con.lrange(history_key, 0, 4)
        
        goods_li = []
        for id in sku_ids:
            goods = GoodsSKU.objects.get(id=id)
            goods_li.append(goods)
        
        return render(request, user_info, {'page':'info', 'address':address, 'good_li':goods_li})
    
#/user/order
class OrderView(LoginRequiredMixin,View):
    def get(self, request):
        return render(request, user_order, {'page':'order'})

#/user/address
class SiteView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        address = Address.objects.get_default_address(user)
        return render(request, user_site, {'page':'site', 'address':address})

    def post(self, request):
        #1.接收数据
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        phone = request.POST.get('phone')
        zip_code = request.POST.get('zip_code')
        
        #2.校验
        if not all((receiver, addr, phone)):
            return render(request, user_site, {'errmsg': '数据不完整'})

        #手机号
        #if not re.match(r'^1[3|4|5|6]\d{9}', phone):
        #    return render(request, user_site, {'errmsg': '手机格式不对'})

        #3.业务处理
        user = request.user
        address = Address.objects.get_default_address(user)

        if address:
            is_default = False
        else:
            is_default = True
           
        Address.objects.create(user = user, receiver = receiver, addr = addr, phone_number = phone, zip_code = zip_code, is_default = is_default) 
        return redirect(reverse("user:site"))
