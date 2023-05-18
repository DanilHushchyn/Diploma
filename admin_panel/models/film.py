from django.core import validators
from django.db import models
import django.forms as forms
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "countries"

    def __str__(self):
        return self.name


class Operator(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "operators"


class Editor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "editors"


class Producer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "producers"


class ScriptWriter(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "scriptwriters"


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "genres"


class Film(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name=_('Название'), validators=[
        validators.MaxLengthValidator(20),
        validators.RegexValidator('^[A-ZА-Я]{1}.*', message='Название должно начинаться с заглавной буквы'),
        validators.ProhibitNullCharactersValidator(),
    ])
    description = models.TextField(verbose_name=_('Описание'),
                                   validators=[
                                       validators.MaxLengthValidator(10_000),
                                       validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                                 message='Описание должно начинаться с заглавной буквы.'),
                                       validators.ProhibitNullCharactersValidator(),

                                   ])
    card_img = models.ImageField(upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True,
                                 verbose_name=_('Картинка карточки'))
    released = models.DateField(verbose_name=_('Дата выхода'))
    trailer_link = models.URLField(verbose_name=_('Ссылка на трейлер'),
                                   validators=[
                                               validators.URLValidator(regex='https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}([-a-zA-Z0-9()@:%_\+.~#?&\/=]*)',message='XYZ'),
                                               ],
                                   )
    banner = models.ImageField(upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True,
                               verbose_name=_('Баннер'),)
    year = models.PositiveSmallIntegerField(verbose_name=_('Год'),
                                            validators=[
                                                validators.MaxValueValidator(2100),
                                                validators.MinValueValidator(1900),
                                            ])
    countries = models.ManyToManyField(Country, verbose_name=_('Страны'))
    genres = models.ManyToManyField(Genre, verbose_name=_('Жанры'))
    producers = models.ManyToManyField(Producer, verbose_name=_('Продюсеры'))
    editors = models.ManyToManyField(Editor, verbose_name=_('Режисёры'))
    scriptwriters = models.ManyToManyField(ScriptWriter, verbose_name=_('Сценаристы'))
    operators = models.ManyToManyField(Operator, verbose_name=_('Операторы'))
    budget = models.PositiveIntegerField(verbose_name=_('Бюджет'))
    legal_age = models.PositiveSmallIntegerField(verbose_name=_('Мин Возраст'),
                                                 validators=[
                                                     validators.MaxValueValidator(18),
                                                     validators.MinValueValidator(8),
                                                 ])
    duration = models.PositiveSmallIntegerField(verbose_name=_('Длительность'),
                                                validators=[
                                                    validators.MinValueValidator(10),
                                                ])
    technology_types = models.ManyToManyField('TechnologyType', verbose_name=_('Форматы'),)
    seo_block = models.OneToOneField('SeoBlock', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = "films"


class TechnologyType(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'technology_type'

    def __str__(self):
        return self.name


class FilmImg(models.Model):
    img = models.ImageField(upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True, verbose_name='',)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)

    class Meta:
        db_table = 'film_imgs'

class SeoBlock(models.Model):
    title = models.CharField(verbose_name=_('Название'), max_length=50,
                             validators=[
                                 validators.MaxLengthValidator(50, 'Название не более 20ти символов.'),
                                 validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                           'Название должно начинаться с заглавной буквы'),
                                 validators.ProhibitNullCharactersValidator(),
                             ]
                             )
    url = models.URLField(verbose_name=_('Ссылка'),
                          validators=[
                              validators.URLValidator(
                                  regex='https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}([-a-zA-Z0-9()@:%_\+.~#?&\/=]*)',
                                  message='XYZ'),

                          ],
                          )

    seo_description = models.TextField(verbose_name=_('Описание'), null=True,
                                       validators=[
                                           validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                                     message='Описание должно начинаться с заглавной буквы'),
                                           validators.ProhibitNullCharactersValidator(),
                                       ]
                                       )
    keywords = models.CharField(verbose_name=_('Ключевые слова'), max_length=255,
                                validators=[
                                    validators.MaxLengthValidator(255),
                                    validators.ProhibitNullCharactersValidator(),
                                ]
                                )

    class Meta:
        db_table = 'seo_block'
