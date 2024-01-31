from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Basket, Product, ProductCategory


class ProductsTestCase(TestCase):
    def setUp(self):
        # Создаем тестовые данные
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = ProductCategory.objects.create(name='TestCategory')
        self.product = Product.objects.create(name='TestProduct', category=self.category)
        self.basket = Basket.objects.create(user=self.user, product=self.product, quantity=2)

    def test_index_view(self):
        # Проверяем, что главная страница возвращает статус 200
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_product_view(self):
        # Проверяем, что страница продукта возвращает статус 200
        response = self.client.get(reverse('product', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_basket_add_view_authenticated_user(self):
        # Проверяем, что добавление в корзину работает для аутентифицированного пользователя
        self.client.force_login(self.user)
        response = self.client.post(reverse('basket_add', args=[self.product.id]), {'size': 'M'})
        self.assertEqual(response.status_code, 302)  # Должно быть перенаправление
        self.assertEqual(self.user.basket_set.count(), 2)  # Должно быть две записи в корзине

    def test_basket_remove_view_authenticated_user(self):
        # Проверяем, что удаление из корзины работает для аутентифицированного пользователя
        self.client.force_login(self.user)
        response = self.client.post(reverse('basket_remove', args=[self.basket.id]))
        self.assertEqual(response.status_code, 302)  # Должно быть перенаправление
        self.assertEqual(self.user.basket_set.count(), 0)  # Должно быть ноль записей в корзине

    def test_basket_add_view_unauthenticated_user(self):
        # Проверяем, что добавление в корзину не работает для неаутентифицированного пользователя
        response = self.client.post(reverse('basket_add', args=[self.product.id]), {'size': 'M'})
        self.assertEqual(response.status_code, 302)  # Должно быть перенаправление
        self.assertEqual(self.user.basket_set.count(), 0)  # Не должно быть записей в корзине

    def test_basket_remove_view_unauthenticated_user(self):
        # Проверяем, что удаление из корзины не работает для неаутентифицированного пользователя
        response = self.client.post(reverse('basket_remove', args=[self.basket.id]))
        self.assertEqual(response.status_code, 302)  # Должно быть перенаправление
        self.assertEqual(self.user.basket_set.count(), 1)  # Должна остаться одна запись в корзине
