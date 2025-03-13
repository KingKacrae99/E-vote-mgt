from django import forms
from .models import *

class LoginForm(forms.Form):
    phone = forms.CharField(
        widget= forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number',
            }
        )
    )

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not Member.objects.filter(phone=phone).exists():
            raise ValueError('This number is not registered! ')
        return phone