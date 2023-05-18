from datetime import date
from django.utils.translation import gettext_lazy as _

import django.forms as forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
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
            'date_of_birth': forms.DateInput(attrs={'class': 'form__elem form__elem_date','type': 'date' },
                                                    format=('%Y-%m-%d'), ),
            'address': forms.TextInput(attrs={'class': 'form__elem', 'size': '10'}),
            'phone': forms.TextInput(attrs={'class': 'form__elem', 'size': '10','placeholder':'Телефон: +38 (098) 567-81-23'}),
        }

    password1 = forms.CharField(label=_("Пароль"),
                                widget=forms.PasswordInput(attrs={'class': 'form__elem'}))
    password2 = forms.CharField(label=_("Повторите пароль"),
                                widget=forms.PasswordInput(attrs={'class': 'form__elem'}),
                                help_text=_("Введите пароль повторно"))


class AdminUserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'address', 'email', 'sex', 'lang', 'date_of_birth',
                  'phone',]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form__elem', 'size': '10'}),
            'last_name': forms.TextInput(attrs={'class': 'form__elem', 'size': '10'}),
            'email': forms.EmailInput(attrs={'class': 'form__elem', 'size': '10'}),
            'sex': forms.RadioSelect(attrs={'class': 'form__elem form__elem_radio', 'size': '10'}),
            'lang': forms.RadioSelect(attrs={'class': 'form__elem form__elem_radio', 'size': '10'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form__elem form__elem_date', 'type':'date'},
                                                    format=('%Y-%m-%d')),
            'address': forms.TextInput(attrs={'class': 'form__elem', 'size': '10'}),
            'phone': forms.TextInput(attrs={'class': 'form__elem', 'size': '10'}),
        }

    password1 = forms.CharField(label=_("Пароль"),
                                widget=forms.PasswordInput(attrs={'class': 'form__elem'}))
    password2 = forms.CharField(label=_("Повторите пароль"),
                                widget=forms.PasswordInput(attrs={'class': 'form__elem'}),
                                help_text=_("Введите пароль повторно"))


class SignInForm(forms.Form):
    email = forms.EmailField(label=_("Электронная почта"),
                             widget=forms.EmailInput(attrs={'class': 'form__elem'}))
    password = forms.CharField(label=_("Пароль"),
                               widget=forms.PasswordInput(attrs={'class': 'form__elem'}))
