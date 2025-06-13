from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import HttpResponseRedirect, render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.contrib import messages
from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory


class IndexView(TitleMixin, TemplateView):
    template_name = "products/index.html"
    title = 'ElectroHub'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()

        return context


class ProductListView(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'object_list'
    paginate_by = 9

    def get_queryset(self):
        queryset = Product.objects.all()

        # Фильтр по категории
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Фильтр по цене
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        price_range = self.request.GET.get('price_range')

        # Обработка предустановленных диапазонов
        if price_range:
            if '-' in price_range:
                min_val, max_val = price_range.split('-')
                if min_val:
                    queryset = queryset.filter(price__gte=int(min_val))
                if max_val:
                    queryset = queryset.filter(price__lte=int(max_val))
            else:  # для случая "50000-" (от 50000)
                queryset = queryset.filter(price__gte=int(price_range.replace('-', '')))

        # Индивидуальные значения цены
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)

        # Фильтр по брендам (если есть поле brand в модели)
        brands = self.request.GET.getlist('brands')
        if brands:
            queryset = queryset.filter(brand_id__in=brands)

        # Фильтр по наличию
        if self.request.GET.get('in_stock'):
            queryset = queryset.filter(quantity__gt=0)  # предполагаем поле quantity

        # Фильтр по скидкам
        if self.request.GET.get('on_sale'):
            queryset = queryset.filter(discount__gt=0)  # предполагаем поле discount

        # Поиск по названию
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(short_description__icontains=search)
            )

        # Сортировка
        sort = self.request.GET.get('sort')
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort == 'name_asc':
            queryset = queryset.order_by('name')
        elif sort == 'name_desc':
            queryset = queryset.order_by('-name')
        elif sort == 'newest':
            queryset = queryset.order_by('-created_at')  # предполагаем поле created_at
        else:
            queryset = queryset.order_by('id')  # сортировка по умолчанию

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()

        # Добавляем бренды если есть
        # context['brands'] = Brand.objects.all()

        return context



@login_required
def basket_add(request, product_id):
    current_page = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
        messages.success(request, 'Product added to basket')
        return HttpResponseRedirect(current_page)
    else:
        basket = baskets.first()
        if basket.quantity < product.quantity:
            basket.quantity += 1
            messages.success(request, 'Product added to basket')
            basket.save()
        else: messages.error(request, 'Out of stock')
        return HttpResponseRedirect(current_page)
        


@login_required
def basket_delete(request, id):
    basket = Basket.objects.get(id=id)
    if basket.quantity > 1:
        basket.quantity -= 1
        basket.save()
    else:
        basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def description_product(request, id):
    context = {'product': Product.objects.get(id=id)}
    return render(request, 'products/description_product.html', context)

class SearchView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 6
    
    def get_queryset(self):
       return Product.objects.filter(name__icontains=self.request.GET.get('q'))
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q']=self.request.GET.get('q')  
        return context
   