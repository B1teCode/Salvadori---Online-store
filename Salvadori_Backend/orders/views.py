from http import HTTPStatus

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from orders.forms import OrderForm, CustomOrderForm
from orders.models import Order, CustomOrder
from products.models import Basket, ProductCategory

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'SALVADORI - Спасибо за покупку'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories_with_count = ProductCategory.objects.annotate(product_count=Count('product'))
        categories = categories_with_count.filter(product_count__gt=0)
        products = CustomOrder.objects.filter(user=self.request.user).values_list('product', flat=True)
        if not products.exists():
            categories = categories.exclude(name='Индивидуальный заказ')
        context['categories'] = categories
        return context


class CanceledTemplateView(TemplateView):
    template_name = 'orders/canceled.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories_with_count = ProductCategory.objects.annotate(product_count=Count('product'))
        categories = categories_with_count.filter(product_count__gt=0)
        products = CustomOrder.objects.filter(user=self.request.user).values_list('product', flat=True)
        if not products.exists():
            categories = categories.exclude(name='Индивидуальный заказ')
        context['categories'] = categories
        return context


class OrderListView(TitleMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'SALVADORI - Заказы'
    queryset = Order.objects.all()
    ordering = ('-created')

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories_with_count = ProductCategory.objects.annotate(product_count=Count('product'))
        categories = categories_with_count.filter(product_count__gt=0)
        products = CustomOrder.objects.filter(user=self.request.user).values_list('product', flat=True)
        if not products.exists():
            categories = categories.exclude(name='Индивидуальный заказ')
        context['categories'] = categories
        return context


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'SALVADORI - Заказ #{self.object.id}'
        categories_with_count = ProductCategory.objects.annotate(product_count=Count('product'))
        categories = categories_with_count.filter(product_count__gt=0)
        products = CustomOrder.objects.filter(user=self.request.user).values_list('product', flat=True)
        if not products.exists():
            categories = categories.exclude(name='Индивидуальный заказ')
        context['categories'] = categories
        return context


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_creator')
    title = 'SALVADORI - Оформление Заказа'

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories_with_count = ProductCategory.objects.annotate(product_count=Count('product'))
        categories = categories_with_count.filter(product_count__gt=0)
        products = CustomOrder.objects.filter(user=self.request.user).values_list('product', flat=True)
        if not products.exists():
            categories = categories.exclude(name='Индивидуальный заказ')
        context['categories'] = categories

        # Добавляем форму с начальным значением address
        if self.request.user.is_authenticated:
            user_address = self.request.user.address
        else:
            user_address = None

        context['order_form'] = OrderForm(initial={'address': user_address})
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

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = event['data']['object']

        # Fulfill the purchase...
        fulfill_order(session)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()


class CustomOrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/custom_order.html'
    form_class = CustomOrderForm
    success_url = reverse_lazy('index')
    title = 'SALVADORI - Оформление Индивидуального заказа'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CustomOrderCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories_with_count = ProductCategory.objects.annotate(product_count=Count('product'))
        categories = categories_with_count.filter(product_count__gt=0)
        products = CustomOrder.objects.filter(user=self.request.user).values_list('product', flat=True)
        if not products.exists():
            categories = categories.exclude(name='Индивидуальный заказ')
        context['categories'] = categories
        return context