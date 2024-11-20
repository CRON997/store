from django.urls import path

from products.views import products,basket_add,basket_delete

app_name = 'products'
urlpatterns = [
    path('',products,name='index'),
    path('basket-add/<int:product_id>/',basket_add,name='basket_add'),
    path('basket_delete/<int:id>/',basket_delete,name='basket_delete')
]