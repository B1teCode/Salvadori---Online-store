from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from users.models import Users
from products.models import Product, ProductCategory, Size, Basket


def index(request):
    categories = ProductCategory.objects.all()
    products = {category: Product.objects.filter(category=category).order_by('-created_at')[:4] for category in categories}
    context = {
        'title': 'Salvadori',
        'products': products,
    }
    return render(request, 'products/index.html', context)


def product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'title': f'Product | {product.name}',
        'product': product,
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
