from django.shortcuts import render,HttpResponseRedirect
from products.models import Product,ProductCategory,Basket
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from common.views import TitleMixin
from django.contrib.auth.decorators import login_required


class IndexView(TitleMixin,TemplateView):
    template_name ="products/index.html"
    title = 'ElectroHub'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()

        return context

class ProductsListView(TitleMixin,ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 6
    title = 'ElectroHub - Catalog'
    

    def get_queryset(self):
        queryset = super(ProductsListView,self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id= category_id) if category_id else queryset
        

    def get_context_data(self,object_list=None,**kwargs):
        context = super(ProductsListView,self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context



@login_required
def basket_add(request,product_id):
    current_page = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user,product = product)

    if not baskets.exists():
        Basket.objects.create(user = request.user, product = product,quantity=1)
        return HttpResponseRedirect(current_page)
    else:
        basket = baskets.first()
        if basket.quantity < product.quantity:
            basket.quantity +=1
            basket.save()
        return HttpResponseRedirect(current_page)
 
@login_required   
def basket_delete(request,id):
    basket = Basket.objects.get(id = id)
    if basket.quantity > 1:
        basket.quantity -= 1 
        basket.save()
    else:
        basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def description_product(request, id):
    context = {'product': Product.objects.get(id = id)}
    return render(request,'products/description_product.html',context)

    

