from django.contrib import admin

from products.models import Product,ProductCategory,Basket


admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Basket)