
from django.contrib import admin
from django.urls import include, path
from products.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index,name='index'),
    path('products/', products,name='products'),
    path('test-context/', test_context,name='test-context'),
]
