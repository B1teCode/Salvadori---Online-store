from django.urls import path

from users.views import (EmailVerificationView, login, logout, profile,
                         registration)

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('verify/<str:email>/<str:code>/', EmailVerificationView.as_view(), name='email_verification')
]
