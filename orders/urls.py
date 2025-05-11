from django.urls import path
from orders.views import orders


app_name = 'orders'

urlpatterns = [
    path('orders/', orders, name='orders'),
]