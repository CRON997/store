import stripe
from django.views.generic.edit import CreateView
from orders.forms import OrderForm
from django.urls import reverse_lazy,reverse
from common.views import TitleMixin
from products.models import Basket
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from http import HTTPStatus
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY



class SuccessTemplateView(TemplateView):
    template_name = 'orders/success.html'
    title = 'ElectroHub-Thanks for order!'


class CancelTemplateView(TemplateView):
    template_name = 'orders/cancled.html'


class OrderCreateView(TitleMixin,CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'ElectroHub-Create-order'

    def form_valid(self, form):
        form.instance.initiator =self.request.user
        return super(OrderCreateView,self).form_valid(form)

    def post(self, request, *args, **kwargs):
        super(OrderCreateView,self).post(request,*args, **kwargs)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, price_1234) of the product you want to sell
                    'price': 'price_1RPVL2DFml6cmm37bxUnBxVh',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME,reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME,reverse('orders:order_canceled')),
        )
        return HttpResponseRedirect(checkout_session.url,status=HTTPStatus.SEE_OTHER)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        baskets = Basket.objects.filter(user = self.request.user)
        context['total_quantity'] = sum(b.quantity for b in baskets)
        context['total_sum'] = sum(b.sum() for b in baskets)
        return context