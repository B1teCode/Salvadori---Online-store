from django.urls import path
from users.views import login, registration, profile, logout, EmailVerificationView

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('verify/<str:email>/<str:code>/', EmailVerificationView.as_view(), name='email_verification')
]