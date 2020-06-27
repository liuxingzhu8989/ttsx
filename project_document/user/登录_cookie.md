1. 修改app/user/urls.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi apps/user/urls.py
   ```

   #urls.py

   ```
   from django.urls import path
   from user.views import RegisterView, LoginView #add Login View
   
   app_name = 'user'
   urlpatterns = [
       path('register/', RegisterView.as_view(), name = 'register'),
       path('login/', LoginView.as_view(), name = 'login'), #add path
   ]
   ```

2. 修改app/user/views.py

   ```
   (venv) [ms@localhost ttsx_exercide]$ vi apps/user/views.py
   ```

   #views.py

   ```
   #LoginView
   from django.contrib.auth import authenticate, login
   
   class LoginView(View):
       def get(self, request):
           return render(request, login_html)
   
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
                   return render(request, index_html)
               else:
                   return render(request, login_html)
            else:
               return render(request, login_html)
   ```
   
3. 记住用户名(cookies)

   语法

   ```
   #set_cookie
   set_cookie(cookie_name_str, value, ttl)
   
   #del_cookie
   delete_cookie(cookie_name_str)
   
   #get_cookie
   COOKIES.get(cookie_name_str)
   ```

   添加cookies记住用户名

   ```
   #get
   def get(self, request):
   	if 'username' in request.COOKIES:
   		username =  request.COOKIES.get('username')
   		checked  = "checked"
   	else:
   		username = ""
   		checked  = ""
   	
   	return render(request, login_html, {"username":username, "checked":checked})
   
   #post
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
   ```

4. 测试

   用注册成功的账号，分别在记住用户名的勾去掉和勾选情况下，看登录成功后，再次访问是否已经记住了

