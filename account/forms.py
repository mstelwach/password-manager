from django import forms
from django.contrib.auth.forms import UserCreationForm

from account.models import Account


class UserCreateForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'username']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email']
