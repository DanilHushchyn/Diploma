import django.forms as forms
from admin_panel.models import *


class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Повторить пароль')

    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'nickname',
                  'email',
                  'address',
                  'sex',
                  'lang',
                  'phone_number',
                  'birthday',
                  'password'
                  ]

        widgets = {
            'sex': forms.RadioSelect(),
            'lang': forms.RadioSelect(),
            'password': forms.PasswordInput(),
            'birthday': forms.DateInput(),
            'email': forms.EmailInput(),
        }

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )
