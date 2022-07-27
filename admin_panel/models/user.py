# Create your models here.
from django.db import models
from django import forms


class User(models.Model):
    first_name = models.CharField(max_length=40, verbose_name=' Имя')
    last_name = models.CharField(max_length=40, verbose_name=' Фамилия')
    nickname = models.CharField(max_length=40, unique=True, verbose_name=' Логин')
    creation_date = models.DateField(auto_now_add=True, null=True)
    email = models.EmailField(verbose_name='Электронная почта',unique=True)
    address = models.CharField(max_length=200, verbose_name=' Адрес')
    Sex_CHOICES = [
        ("Мужской", 'Мужской'),
        ("Женский", 'Женский'),

    ]
    sex = models.CharField(
        max_length=20,
        choices=Sex_CHOICES,
        default='Мужской', verbose_name='Пол'
    )
    LANG_CHOICES = [
        ("Русский", 'Русский'),
        ("Украинскийй", 'Украинский'),

    ]
    lang = models.CharField(
        max_length=20,
        choices=LANG_CHOICES,
        default='Русский', verbose_name='Язык'
    )
    phone_number = models.CharField(max_length=20,verbose_name='Номер телефона',unique=True)
    birthday = models.DateField(verbose_name='День Рождения')
    password = models.CharField(max_length=20, verbose_name=' Пароль')

    class Meta:
        db_table = "users"


class City(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "cities"
