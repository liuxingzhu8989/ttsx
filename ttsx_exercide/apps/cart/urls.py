from django.urls import path
from cart.views import CartAddView, CartShowView, CartUpdateView

app_name = 'cart'
urlpatterns = [
    path('add', CartAddView.as_view(), name='add'),
    path('show', CartShowView.as_view(), name='show'),
    path('update', CartUpdateView.as_view(), name='update'),
]
