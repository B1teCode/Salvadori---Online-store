from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from products.models import Basket, Product, ProductCategory, ExternalImage
from orders.models import CustomOrder

def index(request, category_id=None, page_number=1):
    try:
        categories_with_count = ProductCategory.objects.annotate(product_count=Count('product'))
        categories = categories_with_count.filter(product_count__gt=0)
        selected_category = None
        products_paginator = None

        if request.user.is_authenticated:
            if category_id:
                selected_category = ProductCategory.objects.get(id=category_id)
                if selected_category.name == 'Индивидуальный заказ':
                    # Фильтруем продукты, связанные с заказами Индивидуального заказа текущего пользователя
                    products = CustomOrder.objects.filter(user=request.user).values_list('product', flat=True)
                    products = Product.objects.filter(id__in=products)
                else:
                    products = Product.objects.filter(category=selected_category)
                per_page = 12
                paginator = Paginator(products, per_page)
                products_paginator = paginator.page(page_number)
            else:
                categories = categories.exclude(name='Индивидуальный заказ')
                # Выводим все продукты для каждой категории
                products = {category: Product.objects.filter(category=category).order_by(
                    '-created_at')[:4] if category.name != 'Индивидуальный заказ' else [] for category in categories}

                # Проверяем наличие у пользователя заявок на индивидуальный заказ
                user_custom_orders = CustomOrder.objects.filter(user=request.user)
                if user_custom_orders.exists():
                    # Если есть, добавляем категорию "Индивидуальный заказ" и соответствующие продукты
                    categories |= ProductCategory.objects.filter(name='Индивидуальный заказ')
                    user_custom_order_products = user_custom_orders.values_list('product', flat=True)
                    products['Индивидуальный заказ'] = Product.objects.filter(id__in=user_custom_order_products)

        else:
            # Если пользователь не аутентифицирован, показываем все категории, кроме "Индивидуальный заказ"
            if category_id:
                selected_category = ProductCategory.objects.get(id=category_id)
                categories = categories.exclude(name='Индивидуальный заказ')
                products = Product.objects.filter(category=selected_category)
                per_page = 12
                paginator = Paginator(products, per_page)
                products_paginator = paginator.page(page_number)
            else:
                categories = categories.exclude(name='Индивидуальный заказ')
                products = {category: Product.objects.filter(category=category).order_by('-created_at')[:4] for category in categories}

        # Получение объектов ExternalImage
        external_images = ExternalImage.objects.all()

        context = {
            'title': 'Salvadori',
            'categories': categories,
            'selected_category': selected_category,
            'products': products,
            'products_paginator': products_paginator,
            'external_images': external_images,
        }
        return render(request, 'products/index.html', context)
    except ProductCategory.DoesNotExist:
        raise Http404("Категория не найдена")

def product(request, product_id):
    categories_with_count = ProductCategory.objects.annotate(product_count=Count('product'))
    categories = categories_with_count.filter(product_count__gt=0)

    products = CustomOrder.objects.filter(user=request.user).values_list('product', flat=True)
    if not products.exists():
        categories = categories.exclude(name='Индивидуальный заказ')
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
