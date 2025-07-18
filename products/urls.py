from django.urls import path

from products.views import (ProductListView, basket_add, basket_delete,
                            description_product,SearchView)

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('category/<int:category_id>/', ProductListView.as_view(), name='category'),
    path('page/<int:page>/', ProductListView.as_view(), name='page'),
    path('basket-add/<int:product_id>/',basket_add,name='basket_add'),
    path('basket-delete/<int:id>/',basket_delete,name='basket_delete'),
    path('description/<int:id>/',description_product,name='description_product'),
    path('search/',SearchView.as_view(),name='search')
]