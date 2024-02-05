from django import forms


from orders.models import Order, CustomOrder


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control rounded-pill',
        'placeholder': 'Иван'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control rounded-pill',
        'placeholder': 'Иван'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control rounded-pill',
        'placeholder': 'you@example.com'
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control rounded-pill',
        'placeholder': 'Россия, Москва, ул. Мира, дом 6',
        # 'value': Users.objects.get(id)
    }))



    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address')

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
        'class': 'form-control-file',  # Используйте форму для загрузки файлов для изображений
    }))
    product_size = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control rounded-pill',
        'placeholder': 'Размер продукта'
    }))

    class Meta:
        model = CustomOrder  # Исправлено с Order на CustomOrder
        fields = ('product_name', 'product_description', 'product_photo', 'product_size')
