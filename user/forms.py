from datetime import date

import django.forms as forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import Form

from admin_panel.models import *


class UserForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Account
        fields = ['first_name', 'last_name', 'address', 'email', 'sex', 'lang', 'date_of_birth',
                  'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form__elem', 'size': '10'}),
            'last_name': forms.TextInput(attrs={'class': 'form__elem', 'size': '10'}),
            'email': forms.EmailInput(attrs={'class': 'form__elem', 'size': '10'}),
            'sex': forms.RadioSelect(attrs={'class': 'form__elem form__elem_radio', 'size': '10'}),
            'lang': forms.RadioSelect(attrs={'class': 'form__elem form__elem_radio', 'size': '10'}),
            'date_of_birth': forms.SelectDateWidget(attrs={'class': 'form__elem form__elem_date',},
                                               years=range(1940,date.today().year),),
            'address': forms.TextInput(attrs={'class': 'form__elem', 'size': '10'}),
            'phone': forms.TextInput(attrs={'class': 'form__elem', 'size': '10'}),
        }

    password1 = forms.CharField(label=("Пароль"),
                                widget=forms.PasswordInput(attrs={'class': 'form__elem'}))
    password2 = forms.CharField(label=("Повторите пароль"),
                                widget=forms.PasswordInput(attrs={'class': 'form__elem'}),
                                help_text=("Введите пароль повторно"))

class SignInForm(forms.Form):
    email = forms.EmailField(label=("Электронная почта"),
                                widget=forms.EmailInput(attrs={'class': 'form__elem'}))
    password = forms.CharField(label=("Пароль"),
                                widget=forms.PasswordInput(attrs={'class': 'form__elem'}))
