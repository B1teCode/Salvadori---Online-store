from django import forms

from orders.models import CustomOrder, Order


class OrderForm(forms.ModelForm):
    fio = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4 rounded-pill',
        'placeholder': 'Введите ФИО'
    }), required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control rounded-pill',
        'placeholder': 'you@example.com'
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control rounded-pill',
        'placeholder': 'Россия, Москва, ул. Мира, дом 6',
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control rounded-pill',
        'placeholder': 'Введите свой номер телефона'
    }))
    is_cdek_delivery = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False,
        label='Доставка СДЭК'
    )
    is_boxberry_delivery = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False,
        label='Доставка Boxberry'
    )

    class Meta:
        model = Order
        fields = ('fio', 'email', 'address', 'phone', 'is_cdek_delivery', 'is_boxberry_delivery')


class CustomOrderForm(forms.ModelForm):
    product_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control rounded-pill',
        'placeholder': 'Название продукта'
    }))
    product_description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Описание продукта'
    }))
    product_photo = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-file-input',  # Используйте форму для загрузки файлов для изображений
    }))
    product_size = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control rounded-pill',
        'placeholder': 'Размер продукта'
    }))

    class Meta:
        model = CustomOrder  # Исправлено с Order на CustomOrder
        fields = ('product_name', 'product_description', 'product_photo', 'product_size')
