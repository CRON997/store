from django.template.context_processors import request
from django.views.generic.edit import CreateView
from orders.forms import OrderForm
from django.urls import reverse_lazy
from common.views import TitleMixin
from products.models import Basket
from users.models import User

class OrderCreateView(TitleMixin,CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'ElectroHub-Create-order'

    def form_valid(self, form):
        form.instance.initiator =self.request.user
        return super(OrderCreateView,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        baskets = Basket.objects.filter(user = self.request.user)
        context['total_quantity'] = sum(b.quantity for b in baskets)
        context['total_sum'] = sum(b.sum() for b in baskets)
        return context