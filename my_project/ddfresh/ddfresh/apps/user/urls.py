from django.urls import path,re_path
from django.contrib.auth.decorators import login_required
from user import views


app_name = 'user'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name = 'register'),
    path('login/',views.LoginView.as_view(), name = 'login'),
    re_path('active/(?P<token>.*)$', views.ActiveView.as_view(), name='active'),
    path('info/',views.UserInfoView.as_view(), name = 'user'),
    path('order/',views.UserOrderView.as_view(), name = 'order'),
    path('site/',views.UserSiteView.as_view(), name = 'site'),
]
