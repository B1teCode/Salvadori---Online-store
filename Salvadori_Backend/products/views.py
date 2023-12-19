from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'title': 'Salvadori',
        'products': {
            'Обувь': [
                {'name': 'NEW BALANCE 2002R GREY BROWN POUCH',
                 'price': '39900 ₽',
                 'image': '/static/vendor/img/sneakers1.png',
                 'in_stock': True},

                {'name': 'NEW BALANCE 2002R GREY BROWN POUCH',
                 'price': '39900 ₽',
                 'image': '/static/vendor/img/sneakers2.png',
                 'in_stock': False},

                {'name': 'NEW BALANCE 2002R GREY BROWN POUCH',
                 'price': '39900 ₽',
                 'image': '/static/vendor/img/sneakers3.png',
                 'in_stock': True},

                {'name': 'NEW BALANCE 2002R GREY BROWN POUCH',
                 'price': '39900 ₽',
                 'image': '/static/vendor/img/sneakers4.png',
                 'in_stock': False}
            ],
            'Одежда': [
                {'name': 'TRAVIS SCOTT NEW SIGHT ZIP UP HOODIE OLIVE (SS22)',
                 'price': '39900 ₽',
                 'image': 'https://pngimg.com/uploads/hoodie/hoodie_PNG22.png',
                 'in_stock': False},

                {'name': 'TRAVIS SCOTT NEW SIGHT ZIP UP HOODIE OLIVE (SS22)',
                 'price': '39900 ₽',
                 'image': 'https://pngimg.com/uploads/hoodie/hoodie_PNG24.png',
                 'in_stock': True},

                {'name': 'TRAVIS SCOTT NEW SIGHT ZIP UP HOODIE OLIVE (SS22)',
                 'price': '39900 ₽',
                 'image': 'https://www.pngarts.com/files/11/Sweatshirt-Hoodie-PNG-High-Quality-Image.png',
                 'in_stock': True},

                {'name': 'TRAVIS SCOTT NEW SIGHT ZIP UP HOODIE OLIVE (SS22)',
                 'price': '39900 ₽',
                 'image': 'https://pngimg.com/uploads/hoodie/hoodie_PNG29.png',
                 'in_stock': False},
            ],
            'Аксессуары': [
                {'name': 'Товар5', 'price': 500, 'image': 'image5.jpg'},
                {'name': 'Товар6', 'price': 600, 'image': 'image6.jpg'},
                {'name': 'Товар7', 'price': 700, 'image': 'image7.jpg'},
                {'name': 'Товар8', 'price': 800, 'image': 'image8.jpg'}
            ],
            'Коллекции': [
                {'name': 'Товар5', 'price': 500, 'image': 'image5.jpg'},
                {'name': 'Товар6', 'price': 600, 'image': 'image6.jpg'},
                {'name': 'Товар7', 'price': 700, 'image': 'image7.jpg'},
                {'name': 'Товар8', 'price': 800, 'image': 'image8.jpg'}
            ]
        }
    }
    return render(request, 'products/index.html', context)

def product(request):
    context = {
        'title': 'Product | ---'
    }
    return render(request, 'products/product.html', context)