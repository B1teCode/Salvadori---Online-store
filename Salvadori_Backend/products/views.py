from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from users.models import Users
from products.models import Product, ProductCategory, Size, Basket
from django.core.paginator import Paginator

def index(request, category_id=None, page_number=1):
    try:
        categories = ProductCategory.objects.all()
        selected_category = None
        products_paginator = None

        if category_id:
            selected_category = ProductCategory.objects.get(id=category_id)
            products = Product.objects.filter(category=selected_category)
            per_page = 12
            paginator = Paginator(products, per_page)
            products_paginator = paginator.page(page_number)
        else:
            products = {category: Product.objects.filter(category=category).order_by('-created_at')[:4] for category in categories}

        context = {
            'title': 'Salvadori',
            'categories': categories,
            'selected_category': selected_category,  # добавляем выбранную категорию в контекст
            'products': products,
            'products_paginator': products_paginator
        }
        return render(request, 'products/index.html', context)
    except ProductCategory.DoesNotExist:
        raise Http404("Категория не найдена")


def product(request, product_id):
    categories = ProductCategory.objects.all()
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'title': f'Product | {product.name}',
        'product': product,
        'categories': categories,
    }
    return render(request, 'products/product.html', context)

@login_required()
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    size_id = request.POST.get('size')  # Получаем выбранный размер из запроса

    # Проверка наличия корзины с данным продуктом и размером
    baskets = Basket.objects.filter(user=request.user, product=product, size__id=size_id)

    if not baskets.exists():
        # Создаем новую запись в корзине с выбранным размером
        Basket.objects.create(user=request.user, product=product, quantity=1, size_id=size_id)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required()
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
