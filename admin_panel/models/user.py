# Create your models here.

import django.utils.timezone
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django import forms
from django.utils import timezone


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, first_name,last_name, phone,sex,lang ,password, **extra_fields):
        values = [email, first_name,last_name, phone,sex,lang]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            sex=sex,
            lang=lang,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name,last_name, phone, sex,lang,password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, first_name,last_name, phone,sex,lang ,password, **extra_fields)

    def create_superuser(self, email, first_name,last_name, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, first_name,last_name, phone, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=150,unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    SEX_CHOICE = (
        ('Мужской', 'Мужской'),
        ('Женский', 'Женский'),
    )
    LANG_CHOICE = (
        ('Английский', 'Английский'),
        ('Русский', 'Русский'),
    )
    sex = models.CharField(max_length=50,choices=SEX_CHOICE)
    lang = models.CharField(max_length=50,choices=LANG_CHOICE)

    date_of_birth = models.DateField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone','sex','lang']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name.split()[0]
