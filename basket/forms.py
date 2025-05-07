from django import forms
from firstproject.models import Order
from .models import *

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

class BasketAddProductForm(forms.Form):
    count = forms.IntegerField(min_value=1, initial=1, label='Количество',
                               widget=forms.NumberInput(attrs={'class': 'form-contol'}))
    reload = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)