from django.urls import path
from cart.views import CartAddView

app_name = 'cart'
urlpatterns = [
    path('add', CartAddView.as_view(), name='add'),
]
