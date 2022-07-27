from django.db import models
import django.forms as forms


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
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    card_img = models.ImageField(upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True,
                                 verbose_name="Картинка карточки")
    released = models.DateField(verbose_name="Дата выхода")
    trailer_link = models.URLField(max_length=100, verbose_name="Ссылка на трейлер")
    banner = models.ImageField(upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True,
                               verbose_name="Баннер")
    year = models.CharField(max_length=4, verbose_name="Год")
    countries = models.ManyToManyField(Country, verbose_name="Страны")
    genres = models.ManyToManyField(Genre, verbose_name="Жанры")
    producers = models.ManyToManyField(Producer, verbose_name="Продюсеры")
    editors = models.ManyToManyField(Editor, verbose_name="Режисёры")
    scriptwriters = models.ManyToManyField(ScriptWriter, verbose_name="Сценаристы")
    operators = models.ManyToManyField(Operator, verbose_name="Операторы")
    budget = models.CharField(max_length=15, verbose_name="Бюджет")
    legal_age = models.PositiveIntegerField(verbose_name="Мин Возраст")
    duration = models.CharField(max_length=15, verbose_name="Длительность")
    technology_types = models.ManyToManyField('TechnologyType', verbose_name="Форматы")
    seo_block = models.OneToOneField('SeoBlock', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "films"


class TechnologyType(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'technology_type'

    def __str__(self):
        return self.name


class FilmImg(models.Model):
    img = models.ImageField(upload_to="photos/%Y/%m/%d/",max_length=100, unique=True, null=True, verbose_name='')
    film = models.ForeignKey(Film, on_delete=models.CASCADE)

    class Meta:
        db_table = 'film_imgs'


class SeoBlock(models.Model):
    url = models.URLField(max_length=150, verbose_name='Ссылка')
    title = models.CharField(max_length=50, verbose_name='Название')
    seo_description = models.TextField(verbose_name='Описание', null=True)
    keywords = models.CharField(verbose_name='Ключевые слова', max_length=255)

    class Meta:
        db_table = 'seo_block'
