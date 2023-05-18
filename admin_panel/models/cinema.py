import datetime
import os
import uuid
from django_google_maps import fields as map_fields
from django.utils.translation import gettext_lazy as _

import django.utils.timezone
from django.core import validators
from django.db import models

from admin_panel.models.film import Film, TechnologyType, SeoBlock
from admin_panel.models.user import Account


class Contact(models.Model):
    name = models.CharField(verbose_name=_('Название'), max_length=100, unique=True,
                            validators=[
                                validators.MaxLengthValidator(100, 'Длина названия должна быть не более 100 символов.'),
                                validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                          'Название должно начинаться с заглавной буквы'),
                                validators.ProhibitNullCharactersValidator(),
                            ]
                            )
    address = models.TextField(verbose_name=_('Адрес'), )
    coordinate = models.TextField()
    logo = models.ImageField(verbose_name=_('Логотип'), upload_to="photos/%Y/%m/%d/", max_length=100, unique=True,
                             null=True, )
    cinema = models.ForeignKey("Cinema", on_delete=models.CASCADE, default=1)

    def filename(self):
        return os.path.basename(self.logo.name)

    class Meta:
        db_table = 'contacts'


class Cinema(models.Model):
    name = models.CharField(verbose_name=_('Название'), max_length=100, unique=True,
                            validators=[
                                validators.MaxLengthValidator(100),
                                validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                          message='Название кинотеатра должно начинаться с заглавной буквы'),
                                validators.ProhibitNullCharactersValidator(),
                            ]
                            )
    description = models.TextField(verbose_name=_('Описание'), max_length=10_000,
                                   validators=[
                                       validators.MaxLengthValidator(10_000),
                                       validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                                 message='Описание должно начинаться с заглавной буквы.'),
                                       validators.ProhibitNullCharactersValidator(),

                                   ]
                                   )
    banner = models.ImageField(verbose_name=_('Баннер'), upload_to="photos/%Y/%m/%d/", max_length=100, unique=True,
                               null=True, )
    logo = models.ImageField(verbose_name=_('Логотип'), upload_to="photos/%Y/%m/%d/", unique=True,
                             null=True, )
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'cinema'


class CinemaImg(models.Model):
    img = models.ImageField(verbose_name='', upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True, )
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'cinema_imgs'


class Page(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, default=1)
    name = models.CharField(verbose_name=_("Название"), max_length=100, unique=True,
                            validators=[
                                validators.MaxLengthValidator(100,
                                                              'Длина названия страницы должна быть не более 100 символов.'),
                                validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                          'Название страницы должно начинаться с заглавной буквы'),
                                validators.ProhibitNullCharactersValidator(),
                            ]
                            )
    description = models.TextField(verbose_name=_("Описание"), max_length=10_000,
                                   validators=[
                                       validators.MaxLengthValidator(10_000),
                                       validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                                 message='Описание должно начинаться с заглавной буквы.'),
                                       validators.ProhibitNullCharactersValidator(),

                                   ]
                                   )
    banner = models.ImageField(verbose_name=_("Баннер"), upload_to="photos/%Y/%m/%d/", max_length=100, unique=True,
                               null=True, )
    first_pic = models.ImageField(verbose_name=_("Первая картинка"), upload_to="photos/%Y/%m/%d/", max_length=100,
                                  unique=True, null=True, )
    second_pic = models.ImageField(verbose_name=_("Вторая картинка"), upload_to="photos/%Y/%m/%d/", max_length=100,
                                   unique=True, null=True, )
    third_pic = models.ImageField(verbose_name=_("Третья картинка"), upload_to="photos/%Y/%m/%d/", max_length=100,
                                  unique=True, null=True, )
    description2 = models.TextField(verbose_name=_("Второе описание"), max_length=10_000,
                                    validators=[
                                        validators.MaxLengthValidator(10_000),
                                        validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                                  message='Описание должно начинаться с заглавной буквы.'),
                                        validators.ProhibitNullCharactersValidator(),

                                    ]
                                    )
    turn_on = models.BooleanField(verbose_name=_("ВКЛ/ВЫКЛ"), default=False)
    creation_date = models.DateField(verbose_name=_("Дата создания"), auto_now_add=True, null=True)
    able_to_del = models.BooleanField(default=True)
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'pages'
        ordering = ['id']


class PageImg(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    img = models.ImageField(verbose_name="", upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True, )

    class Meta:
        db_table = 'pages_imgs'


class Hall(models.Model):
    number = models.PositiveSmallIntegerField(verbose_name=_("Номер зала"), unique=True,
                                              validators=[
                                                  validators.MinValueValidator(0)
                                              ]
                                              )
    banner = models.ImageField(verbose_name=_("Баннер"), upload_to="photos/%Y/%m/%d/", max_length=100, unique=True,
                               null=True, )
    description = models.TextField(verbose_name=_("Описание"), max_length=10_000,
                                   validators=[
                                       validators.MaxLengthValidator(10_000),
                                       validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                                 message='Описание должно начинаться с заглавной буквы.'),
                                       validators.ProhibitNullCharactersValidator(),

                                   ]
                                   )
    num_tickets = models.PositiveSmallIntegerField(verbose_name=_("Кол-во биллетов"), )
    scheme = models.ImageField(verbose_name=_("Схема зала"), upload_to="photos/%Y/%m/%d/", max_length=100, unique=True,
                               null=True, )
    creation_date = models.DateField(verbose_name=_("Дата создания"), auto_now_add=True)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, default=1)
    scheme_html = models.TextField(null=False,default='')
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.number)

    class Meta:
        ordering = ['number']
        db_table = 'halls'


class HallImg(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    img = models.ImageField(verbose_name='', upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True, )

    class Meta:
        db_table = 'halls_imgs'


class Seance(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, verbose_name=_('Зал'))
    date = models.DateField(verbose_name=_('Дата'))
    price = models.PositiveSmallIntegerField(default=0, verbose_name=_('Цена'),
                                             validators=[validators.MinValueValidator(0)])
    time = models.TimeField(verbose_name=_('Время'))
    film = models.ForeignKey(Film, on_delete=models.CASCADE,null=False, verbose_name=_('Фильм'))
    tech_type = models.ForeignKey(TechnologyType, on_delete=models.CASCADE, null=True, verbose_name=_('Технология'))

    class Meta:
        db_table = 'seances'


class Ticket(models.Model):
    second_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False)
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE, null=False)
    row = models.PositiveSmallIntegerField()
    seat = models.PositiveSmallIntegerField()
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'tickets'


class Stock(models.Model):
    name = models.CharField(verbose_name=_("Название"), max_length=30, null=True,
                            validators=[
                                validators.MaxLengthValidator(30,
                                                              'Длина названия акции должна быть не более 30ти символов.'),
                                validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                          'Название акции должно начинаться с заглавной буквы'),
                                validators.ProhibitNullCharactersValidator(),
                            ]
                            )
    short_description = models.TextField(verbose_name=_("Краткое описание"),blank=True, max_length=250,
                                         validators=[
                                             validators.MaxLengthValidator(250),
                                             validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                                       message='Описание должно начинаться с заглавной буквы.'),
                                             validators.ProhibitNullCharactersValidator(),

                                         ]
                                         )
    description = models.TextField(verbose_name=_("Описание"),blank=True, max_length=10_000,
                                   validators=[
                                       validators.MaxLengthValidator(10_000),
                                       validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                                 message='Описание должно начинаться с заглавной буквы.'),
                                       validators.ProhibitNullCharactersValidator(),

                                   ]
                                   )

    creation_date = models.DateField(verbose_name=_("Дата создания"), auto_now_add=True, null=True)
    turn_on = models.BooleanField(verbose_name=_("ВКЛ/ВЫКЛ"), default=False)
    video_link = models.URLField(verbose_name=_("Ссылка на видео"),
                                 validators=[
                                     validators.URLValidator(
                                         regex='https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}([-a-zA-Z0-9()@:%_\+.~#?&\/=]*)',
                                         message='XYZ'),

                                 ],
                                 )
    banner = models.ImageField(verbose_name=_("Баннер"), upload_to="photos/%Y/%m/%d/", max_length=100, unique=True,
                               null=True, )
    card_img = models.ImageField(verbose_name=_("Картинка карточки"), upload_to="photos/%Y/%m/%d/", max_length=100,
                                 unique=True, null=True, )
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'stocks'


class StockImg(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    img = models.ImageField(upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True, )

    class Meta:
        db_table = 'stock_imgs'


class News(models.Model):
    name = models.CharField(verbose_name=_("Название"), max_length=30, null=False,
                            validators=[
                                validators.MaxLengthValidator(30,
                                                              'Длина названия новости должна быть не более 30ти символов.'),
                                validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                          'Название новости должно начинаться с заглавной буквы'),
                                validators.ProhibitNullCharactersValidator(),
                            ]
                            )
    short_description = models.TextField(verbose_name=_("Краткое описание"), max_length=250,
                                         validators=[
                                             validators.MaxLengthValidator(250),
                                             validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                                       message='Описание должно начинаться с заглавной буквы.'),
                                             validators.ProhibitNullCharactersValidator(),

                                         ]
                                         )
    description = models.TextField(verbose_name=_("Описание"), max_length=10_000,
                                   validators=[
                                       validators.MaxLengthValidator(10_000),
                                       validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                                 message='Описание должно начинаться с заглавной буквы.'),
                                       validators.ProhibitNullCharactersValidator(),

                                   ]
                                   )
    creation_date = models.DateField(verbose_name=_("Дата создания"), auto_now_add=True, null=True)
    turn_on = models.BooleanField(verbose_name=_("ВКЛ/ВЫКЛ"), default=False)
    video_link = models.URLField(verbose_name=_("Ссылка на видео"),
                                 validators=[
                                     validators.URLValidator(
                                         regex='https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}([-a-zA-Z0-9()@:%_\+.~#?&\/=]*)',
                                         message='XYZ'),

                                 ],
                                 )
    banner = models.ImageField(verbose_name=_("Баннер"), upload_to="photos/%Y/%m/%d/", max_length=100, unique=True,
                               null=True, )
    card_img = models.ImageField(upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True,
                                 verbose_name=_("Картинка карточки"), )
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'news'


class NewsImg(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    img = models.ImageField(verbose_name='', upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True, )

    class Meta:
        db_table = 'news_imgs'


class CafeBarMenu(models.Model):
    name = models.CharField(
                            verbose_name=_('Название'),
                            max_length=150,
                            validators=[
                                validators.MaxLengthValidator(150),
                                validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                          message='Название блюда должно начинаться с заглавной буквы'),
                                validators.ProhibitNullCharactersValidator(),
                            ]
                            )
    weight = models.PositiveSmallIntegerField(null=True, verbose_name=_('Вес(грамм)'),
                                              validators=[
                                                  validators.MinValueValidator(0)
                                              ]
                                              )
    price = models.FloatField(null=True, verbose_name=_('Цена'),
                              validators=[
                                  validators.MinValueValidator(0.0)
                              ]
                              )

    class Meta:
        db_table = 'cafe_bar_menu'
