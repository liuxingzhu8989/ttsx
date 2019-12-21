from django.shortcuts import render

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
from user.models import User

#LoginView, LogOutView
from django.contrib.auth import authenticate, login, logout

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
                res = render(request, index_html) #add, only res has set_cookie()
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
        return render(request, index_html)

#/user/info
class InfoView(View):
    def get(self, request):
        return render(request, user_info, {'page':'info'})
    
#/user/order
class OrderView(View):
    def get(self, request):
        return render(request, user_order, {'page':'order'})

#/user/site
class SiteView(View):
    def get(self, request):
        return render(request, user_site, {'page':'site'})
