from django.contrib import admin

from products.models import Product,ProductCategory,Basket


admin.site.register(ProductCategory)
admin.site.register(Basket)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','quantity','category')
    fields = ('name','image','description','short_description',('price','quantity'),'category')
    # readonly_fields = ('name',)
    ordering = ('name',)


class BasketAdminInline(admin.TabularInline):
    model = Basket
    fields=('product','quantity',)
    readonly_fields = ('product',)
    extra = 0