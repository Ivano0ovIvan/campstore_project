from django import forms
from .models import Product, Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'address', 'zipcode', 'city', 'phone_number')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'title', 'description', 'price', 'image',)
        widgets = {
            'category': forms.Select(attrs={
                'style': 'max-width: 300px',
                'placeholder': 'Category'
            }),
            'title': forms.TextInput(attrs={
                'style': 'max-width: 300px',
                'placeholder': 'Title'
            }),
            'description': forms.Textarea(attrs={
                'style': 'max-width: 300px',
                'placeholder': 'Description'
            }),
            'price': forms.NumberInput(attrs={
                'style': 'max-width: 300px',
                'placeholder': 'Price'
            }),
        }
