from django.shortcuts import render
from products.models import Product, ProductCategory, Size

def index(request):
    categories = ProductCategory.objects.all()
    products = {category: Product.objects.filter(category=category)[:4] for category in categories}
    context = {
        'title': 'Salvadori',
        'products': products,
    }
    return render(request, 'products/index.html', context)

def product(request):
    context = {
        'title': 'Product | ---'
    }
    return render(request, 'products/product.html', context)