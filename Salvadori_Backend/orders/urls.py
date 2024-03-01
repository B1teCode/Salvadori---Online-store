from django.urls import path

from orders.views import (CanceledTemplateView, CustomOrderCreateView,
                          OrderCreateView, OrderDetailView, OrderListView,
                          SuccessTemplateView, PaymentView)

app_name = 'orders'

urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order_creator'),
    path('custom-order/', CustomOrderCreateView.as_view(), name='custom_order'),
    path('', OrderListView.as_view(), name='orders_list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order'),
    path('order-success/', SuccessTemplateView.as_view(), name='order_success'),
    path('order-canceled/', CanceledTemplateView.as_view(), name='order_canceled'),
    path('payment/', PaymentView.as_view(), name='payment'),
]
