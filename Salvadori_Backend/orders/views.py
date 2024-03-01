import stripe

from http import HTTPStatus
from django.conf import settings
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from orders.forms import CustomOrderForm, OrderForm
from orders.models import CustomOrder, Order
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
    success_url = reverse_lazy('orders:payment')
    title = 'SALVADORI - Оформление Заказа'

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
            user_fio = self.request.user.fio
            user_address = self.request.user.address
            user_email = self.request.user.email
            user_phone = self.request.user.phone
        else:
            user_address = None

        context['order_form'] = OrderForm(initial={
            'address': user_address,
            'phone': user_phone,
            'email': user_email,
            'fio': user_fio
        })
        return context


class PaymentView(TemplateView):
    template_name = 'orders/payment.html'  # Создайте шаблон для страницы оплаты

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
            user_fio = self.request.user.fio
            user_address = self.request.user.address
            user_email = self.request.user.email
            user_phone = self.request.user.phone
        else:
            user_address = None
            user_email = None
            user_fio = None
            user_phone = None

        context['order_form'] = OrderForm(initial={
            'address': user_address,
            'phone': user_phone,
            'email': user_email,
            'fio': user_fio
        })
        return context


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
