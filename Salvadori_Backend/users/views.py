from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from django.views.generic.base import TemplateView

from common.views import TitleMixin
from orders.models import CustomOrder
from products.models import ProductCategory
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, Users

# Create your views here.


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {
        'title': 'Авторизация',
        'form': form,
    }
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Поздравляем! Вы успешно зарегистрированы!.')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {
        'title': 'Регистрация',
        'form': form,
    }
    return render(request, 'users/register.html', context)


@login_required()
def profile(request):
    categories_with_count = ProductCategory.objects.annotate(product_count=Count('product'))
    categories = categories_with_count.filter(product_count__gt=0)

    products = CustomOrder.objects.filter(user=request.user).values_list('product', flat=True)
    if not products.exists():
        categories = categories.exclude(name='Индивидуальный заказ')

    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'title': 'Личный кабинет',
        'form': form,
        'categories': categories,
    }
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Salvadori - Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = Users.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories_with_count = ProductCategory.objects.annotate(product_count=Count('product'))
        categories = categories_with_count.filter(product_count__gt=0)
        products = CustomOrder.objects.filter(user=self.request.user).values_list('product', flat=True)
        if not products.exists():
            categories = categories.exclude(name='Индивидуальный заказ')
        context['categories'] = categories
        return context
