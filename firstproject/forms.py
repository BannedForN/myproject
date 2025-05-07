from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *

class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        min_length=2
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        min_length=2
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'publisher': forms.Select(attrs={'class': 'form-select'}),
            'designers': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'release_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'min_players': 'Минимальное число игроков',
            'max_players': 'Максимальное число игроков',
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'status', 'shipping_address']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'shipping_address': forms.Textarea(attrs={'rows': 3}),
            'order_date': forms.HiddenInput(),
            'total_amount': forms.HiddenInput()
        }

OrderItemFormSet = forms.inlineformset_factory(
    Order,
    OrderItem,
    fields=('game', 'quantity', 'price'),
    extra=1,
    widgets={
        'game': forms.Select(attrs={
            'class': 'form-select',
            'data-live-search': 'true'
        }),
        'quantity': forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1
        }),
        'price': forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0.01'
        }),
    },
    can_delete=True,
    validate_min=True,
    min_num=1
)