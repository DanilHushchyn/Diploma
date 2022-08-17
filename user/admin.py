from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from admin_panel.models import Account


class AccountUserAdmin(UserAdmin):
    model = Account
    list_display = ['email', 'phone', 'first_name', 'last_name', 'is_staff']

admin.site.register(Account, AccountUserAdmin)