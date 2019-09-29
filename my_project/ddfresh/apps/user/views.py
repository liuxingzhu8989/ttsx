from django.shortcuts import render,redirect
from django.urls import reverse
from user.models import User
import re

# Create your views here.
def register(request):
    return render(request, 'register.html')

def register_handle(request):
    '''注册处理'''
    #接受数据
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')
    allow = request.POST.get('allow')
    
    #数据校验
    if not all((username, password, email)):
        #数据不完整
        return render(request, 'register.html',{'errmsg':'数据不完整'})
    
    pattern = re.compile(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$')
    if not pattern.match(email):
        #数据不完整
        return render(request, 'register.html',{'errmsg':'邮箱不对'})

    if allow != 'on':
        return render(request, 'register.html',{'errmsg':'请同意协议'})
        
    #业务校验
    user = User.objects.create_user(username, email, password)

    #返回应答
    return redirect(reverse('goods:index'))
    
