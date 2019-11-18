from django.shortcuts import render,redirect
from django.urls import reverse
from django.conf import settings
from django.views.generic import View
from user.models import User, Address
from django.http import HttpResponse
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from celery_tasks.tasks import send_email_to_verify
from django.contrib.auth import authenticate, login, logout
from utils.mixin import LoginRequiredMixin
import re

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
    def post(self, request):
        #接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        
        #校验数据
        if not all([username, password, email]):
            info = "data is not intact"
            return render(request, 'register.html', {'info':info})

        #业务处理
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if not user:
            user = User.objects.create_user(username, email, password)
            user.is_active = 0
            user.save()
        
        serialize = Serializer(settings.SECRET_KEY)
        confirm = {'confirm':user.id}
        token = serialize.dumps(confirm) 
        token = token.decode()

        #celery send email
        send_email_to_verify.delay(email, username, token)

        #返回页面
        return render(request, 'login.html')

class LoginView(View):
    def get(self, request):
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''

        return render(request, 'login.html', {'username':username, 'checked':checked})

    def post(self, request):
        #接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        
        #校验数据
        if not all((username, password)):
            return render(request, 'login.html', {'errmsg': '数据不完整'})

        #业务处理
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                #记录登录状态
                login(request, user)

                next_url = request.GET.get('next', reverse('goods:index'))
                res = redirect(next_url)
                
                remember = request.POST.get('jizhu')
                if remember == 'on':
                    res.set_cookie('username', username, 7*24*3600)
                else:
                    res.delete_cookie('username')
                return res
            else:
                return render(request, 'login.html', {'errmsg': '用户没激活'})
        else:
            return render(request, 'login.html', {'errmsg': 'username/password wrong'})

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect(reverse('goods:index'))

    def post(self, request):
        pass

class ActiveView(View):
    '''user active
    '''
    def get(self, request, token):
        '''用户激活
        '''
        print(token)
        serializer = Serializer(settings.SECRET_KEY, 3600) 
        try:
            data = serializer.loads(token)
        except SignatuureExpired as e:
            return HttpResponse('过期')

        print(data)
        user_id = data['confirm']
        user = User.objects.get(id=user_id)
        user.is_active = 1
        user.save()
        return render(request, 'login.html')

# /user
class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        page = 'info'
        user = request.user
        address = Address.objects.get_default_address(user)
        return render(request, 'user_center_info.html', {'page': page, 'address':address})
    def post(self, request):
        pass

#/user/order
class UserOrderView(LoginRequiredMixin,View):
    def get(self, request):
        page = 'order'
        return render(request, 'user_center_order.html', {'page':page})
    def post(self, request):
        pass

#/user/address
class UserAddressView(LoginRequiredMixin, View):
    def get(self, request):
        page = 'address'
        user = request.user
        address = Address.objects.get_default_address(user)
        return render(request, 'user_center_address.html', {'page': page, 'address': address})

    def post(self, request):
        #接收数据
        receiver = request.POST.get('receiver')
        detail_address = request.POST.get('detail_address')
        zip_code = request.POST.get('zip_code')
        phone_number = request.POST.get('phone_number')

        #数据校验
        if not all([receiver, detail_address, phone_number]):
            return render(request, 'user_center_address.html', {'errmsg': '数据不完整'})

        #业务处理
        user = request.user
        address = Address.objects.get_default_address(user)

        if address:
            is_default = False
        else:
            is_default = True
        
        address = Address.objects.create(user=user, receiver = receiver, 
                                        addr=detail_address, zip_code = zip_code,
                                        phone = phone_number, is_default = is_default)

        #返回页面
        return redirect(reverse("user:address"))
            
