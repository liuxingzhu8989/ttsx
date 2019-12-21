from django.urls import path
from user.views import RegisterView, LoginView, LogOutView, InfoView, OrderView, SiteView

app_name = 'user'
urlpatterns = [
    path('register/', RegisterView.as_view(), name = 'register'),
    path('login/', LoginView.as_view(), name = 'login'), 
    path('logout/', LogOutView.as_view(), name = 'logout'), 
    path('info/', InfoView.as_view(), name = 'info'),  #add info
    path('order/', OrderView.as_view(), name = 'order'), #add order
    path('site/', SiteView.as_view(), name = 'site'), #add site
]
