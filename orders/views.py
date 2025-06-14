import stripe
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from orders.forms import OrderForm
from django.urls import reverse_lazy,reverse
from common.views import TitleMixin
from products.models import Basket
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from http import HTTPStatus
from django.http import HttpResponse
from django.conf import settings
from orders.models import Order
stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = 'whsec_98ee01104284452cbd2792ee3466075bbe45776f43cc85457ed2a02028a86949'


class SuccessTemplateView(TemplateView):
    template_name = 'orders/success.html'
    title = 'ElectroHub-Thanks for order!'

class OrdersListView(TitleMixin,ListView):
    template_name = 'orders/orders.html'
    title = 'ElectroHub-orders!'
    queryset = Order.objects.filter()
    ordering = ('-created')

    def get_queryset(self):
        queryset = super(OrdersListView,self).get_queryset()
        return queryset.filter(initiator=self.request.user)

class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView,self).get_context_data(**kwargs)
        context['title'] = f'ElectroHub Order #{self.object.id}'
        return context

class CancelTemplateView(TitleMixin,TemplateView):
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
        response = super().post(request, *args, **kwargs)

        baskets = Basket.objects.filter(user=self.request.user)
        line_items = [{
            'price': basket.product.stripe_product_price_id,
            'quantity': basket.quantity,
        } for basket in baskets]

        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            metadata={'order_id': str(self.object.id)},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )

        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        baskets = Basket.objects.filter(user = self.request.user)
        context['total_quantity'] = sum(b.quantity for b in baskets)
        context['total_sum'] = sum(b.sum() for b in baskets)
        return context

@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if (
            event['type'] == 'checkout.session.completed'
            or event['type'] == 'checkout.session.async_payment_succeeded'
    ):
        fulfill_order(session=event['data']['object'])

    return HttpResponse(status=200)

def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
