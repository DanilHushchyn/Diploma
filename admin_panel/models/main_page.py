from django.core import validators
from django.db import models
from django.db import models
from django.utils.translation import gettext_lazy as _

from admin_panel.models import SeoBlock


class TopCarousel(models.Model):
    img = models.ImageField(verbose_name='', upload_to='photos/%Y/%m/%d/', max_length=100, unique=True, null=True,)
    link = models.URLField(verbose_name='', default='',
                           validators=[
                               validators.URLValidator(
                                   regex='https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}([-a-zA-Z0-9()@:%_\+.~#?&\/=]*)',
                                   message='XYZ'),

                           ],
                           )
    title = models.CharField(verbose_name='', max_length=50, default='',
                             validators=[
                                 validators.MaxLengthValidator(50),
                                 validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                           message='Заголовок должен начинаться с заглавной буквы'),
                                 validators.ProhibitNullCharactersValidator(),
                             ]
                             )

    interval = 5

    class Meta:
        db_table = 'top_carousel'


class BackImg(models.Model):
    img = models.ImageField(verbose_name='', upload_to='photos/%Y/%m/%d/', max_length=100, unique=True, null=True,)

    class Meta:
        db_table = 'back_img'


class BottomCarousel(models.Model):
    img = models.ImageField(verbose_name='', upload_to='photos/%Y/%m/%d/', max_length=100, unique=True, null=True,)
    link = models.URLField(verbose_name='', default='',
                           validators=[
                               validators.URLValidator(
                                   regex='https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}([-a-zA-Z0-9()@:%_\+.~#?&\/=]*)',
                                   message='XYZ'),

                           ],
                           )

    interval = 5

    class Meta:
        db_table = 'bottom_carousel'


class MainPage(models.Model):
    number = models.CharField(verbose_name=_('Телефон 1'),max_length=19, unique=True,
                              validators=[
                                  validators.MaxLengthValidator(19),
                                  validators.MinLengthValidator(19),
                                  validators.ProhibitNullCharactersValidator(),
                                  validators.RegexValidator('^\+38 \(\d{3}\) \d{3}-?\d{2}-?\d{2}$',
                                                            message='Неверно введён номер телефона.Пример ввода: +38 (098) 567-81-23')
                              ]
                              )
    number2 = models.CharField(verbose_name=_('Телефон 2'),max_length=19, unique=True,
                               validators=[
                                   validators.MaxLengthValidator(19),
                                   validators.MinLengthValidator(19),
                                   validators.ProhibitNullCharactersValidator(),
                                   validators.RegexValidator('^\+38 \(\d{3}\) \d{3}-?\d{2}-?\d{2}$',
                                                             message='Неверно введён номер телефона.Пример ввода: +38 (098) 567-81-23')
                               ]
                               )
    seo_text = models.TextField(verbose_name=_('SEO текст'),max_length=500,
                                validators=[
                                    validators.MaxLengthValidator(500),
                                    validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                              message='Описание должно начинаться с заглавной буквы.'),
                                    validators.ProhibitNullCharactersValidator(),

                                ]
                                )
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'main_page'


