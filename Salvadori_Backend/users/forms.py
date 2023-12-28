from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from users.models import Users

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите имя пользователя'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Введите пароль'
    }))
    class Meta:
        model = Users
        fields = ('username', 'password')

class UserRegistrationForm(UserCreationForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Введите адресс электронной почты'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите имя пользователя'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Введите пароль'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Повторите пароль'
    }))
    class Meta:
        model = Users
        fields = ('email', 'username', 'password1', 'password2')

class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4 rounded-pill',
        'placeholder': 'Введите имя'
    }), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4 rounded-pill',
        'placeholder': 'Введите фамилию'
    }), required=False)
    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4 rounded-pill',
        'placeholder': 'Введите город'
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4 rounded-pill',
        'placeholder': 'Введите адрес СДЭК или Boxbery'
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4 rounded-pill',
        'placeholder': 'Введите свой номер телефона'
    }))
    telegram_account = forms.URLField(widget=forms.URLInput(attrs={
        'class': 'form-control py-4 rounded-pill',
        'placeholder': 'ССылка на WhatsApp или Telegram'
    }), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4 rounded-pill',
        'placeholder': 'Введите свой номер телефона',
        'readonly': True,
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4 rounded-pill',
        'placeholder': 'Введите адрес электронной почты',
        'readonly': True,
    }))
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-file-input'
    }), required=False)
    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'city', 'address', 'phone', 'telegram_account', 'username','email', 'image')