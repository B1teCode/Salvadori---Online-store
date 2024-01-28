from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Users, EmailVerification
from products.models import ProductCategory
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm

class UsersViewsTestCase(TestCase):
    def setUp(self):
        # Создаем тестового пользователя и категории продуктов для использования в тестах
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = ProductCategory.objects.create(name='TestCategory')

    def test_login_view(self):
        # Проверяем, что страница авторизации возвращает статус 200 при GET-запросе
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)

        # Проверяем, что пользователь может успешно авторизоваться с правильными учетными данными
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(reverse('users:login'), data)
        self.assertEqual(response.status_code, 302)  # Должно быть перенаправление

    def test_registration_view(self):
        # Проверяем, что страница регистрации возвращает статус 200 при GET-запросе
        response = self.client.get(reverse('users:registration'))
        self.assertEqual(response.status_code, 200)

        # Проверяем, что новый пользователь может быть успешно зарегистрирован
        data = {'username': 'newuser', 'password1': 'newpassword123', 'password2': 'newpassword123', 'email': 'newuser@example.com'}
        response = self.client.post(reverse('users:registration'), data)
        self.assertEqual(response.status_code, 302)  # Должно быть перенаправление

    def test_profile_view_authenticated_user(self):
        # Проверяем, что страница профиля возвращает статус 200 при GET-запросе
        self.client.force_login(self.user)
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)

        # Проверяем, что профиль пользователя может быть успешно изменен
        data = {'first_name': 'New', 'last_name': 'Name'}
        response = self.client.post(reverse('users:profile'), data)
        self.assertEqual(response.status_code, 302)  # Должно быть перенаправление

    def test_logout_view(self):
        # Проверяем, что выход пользователя работает
        self.client.force_login(self.user)
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)  # Должно быть перенаправление

    def test_email_verification_view(self):
        # Подготавливаем данные для подтверждения почты
        user = Users.objects.create(email='test@example.com')
        verification = EmailVerification.objects.create(user=user, code='testcode')

        # Проверяем, что подтверждение почты работает
        url = reverse('users:email_verification', kwargs={'email': 'test@example.com', 'code': 'testcode'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Проверяем, что после подтверждения, пользователь имеет подтвержденную почту
        user.refresh_from_db()
        self.assertTrue(user.is_verified_email)
