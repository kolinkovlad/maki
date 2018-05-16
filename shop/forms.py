from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User

from shop.models import GoodsInOrder


class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def valid_password(self):
        valid = self.changed_data
        if valid['password'] != valid['confirm_password']:
            raise ValidationError('Паролі не співпадають')
        return valid['password']


class AddToBasketFromDetails(forms.ModelForm):
    class Meta:
        model = GoodsInOrder
        fields = ['quantity', 'order']
