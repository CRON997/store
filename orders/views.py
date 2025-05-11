from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView

class OrderCreateView(TemplateView):
    template_name = 'orders/order-create.html'
