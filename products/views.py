from django.shortcuts import render
from products.models import Product,ProductCategory
def index(request):
    context = {
        'title':'ElectroHub'
    }
    return render(request,"products/index.html",context)

def products(request):
    context = {
        'title':'ElectroHub',
        'categories':ProductCategory.objects.all(),
        'products':Product.objects.all()
    }
    return render(request,"products/products.html",context)

