# Create your models here.
from django.utils.translation import gettext_lazy as _

import django.utils.timezone
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core import validators
from django.db import models
from django import forms
from django.utils import timezone


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, first_name, last_name, phone, sex, lang, password, **extra_fields):
        values = [email, first_name, last_name, phone, sex, lang]
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

    def create_user(self, email, first_name, last_name, phone, sex, lang, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, first_name, last_name, phone, sex, lang, password, **extra_fields)

    def create_superuser(self, email, first_name, last_name, phone, sex, lang, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, first_name, last_name, phone, sex, lang, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=150, unique=True, verbose_name=_('Электронная почта'),
                              validators=[
                                  validators.EmailValidator(),
                              ]
                              )
    first_name = models.CharField(max_length=150, verbose_name=_('Имя'),
                                  validators=[
                                      validators.MaxLengthValidator(150),
                                      validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                                message='Имя должно начинаться с заглавной буквы'),
                                      validators.ProhibitNullCharactersValidator(),
                                  ]
                                  )
    last_name = models.CharField(max_length=150, verbose_name=_('Фамилия'),
                                 validators=[
                                     validators.MaxLengthValidator(150),
                                     validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                               message='Фамилия должна начинаться с заглавной буквы'),
                                     validators.ProhibitNullCharactersValidator(),
                                 ]
                                 )
    phone = models.CharField(max_length=19, verbose_name=_('Номер телефона'),
                             validators=[
                                 validators.MaxLengthValidator(19),
                                 validators.MinLengthValidator(19),
                                 validators.ProhibitNullCharactersValidator(),
                                 validators.RegexValidator('^\+38 \(\d{3}\) \d{3}-?\d{2}-?\d{2}$',
                                                           message='Неверно введён номер телефона.Пример ввода: +38 (098) 567-81-23')
                             ]
                             )
    address = models.CharField(max_length=50, verbose_name=_('Город'),
                               validators=[
                                   validators.MaxLengthValidator(50),
                                   validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                             message='Адрес должен начинаться с заглавной буквы'),
                                   validators.ProhibitNullCharactersValidator(),
                               ]
                               )
    SEX_CHOICE = (
        ('Мужской', _('Мужской')),
        ('Женский', _('Женский')),
    )
    LANG_CHOICE = (
        ('Английский', _('Английский')),
        ('Русский', _('Русский')),
    )
    sex = models.CharField(max_length=50, choices=SEX_CHOICE, default='Мужской', verbose_name=_('Пол'))
    lang = models.CharField(max_length=50, choices=LANG_CHOICE, default='Русский', verbose_name=_('Язык'))

    date_of_birth = models.DateField(blank=True, null=True, verbose_name=_('День рождения'))
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'sex', 'lang']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name.split()[0]
