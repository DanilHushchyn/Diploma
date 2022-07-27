import datetime

import django.utils.timezone
from django.db import models

from admin_panel.models.film import Film, TechnologyType, SeoBlock


class Contact(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    coordinate = models.TextField(max_length=10000)
    logo = models.ImageField(upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True)
    cinema = models.ForeignKey("Cinema", on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'contacts'


class Cinema(models.Model):
    name = models.CharField(verbose_name='Название',max_length=100, unique=True)
    description = models.TextField(verbose_name='Описание',)
    banner = models.ImageField(verbose_name='Баннер',upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True)
    logo = models.ImageField(verbose_name='Логотип',upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True)
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'cinema'


class MainPage(models.Model):
    number = models.CharField(max_length=100, unique=True)
    number2 = models.CharField(max_length=100, unique=True)
    seo_text = models.TextField(default='')
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'main_page'


class CinemaImg(models.Model):
    img = models.ImageField(upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True, )
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'cinema_imgs'


class Page(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, default=1)
    name = models.CharField(verbose_name="Название",max_length=100,unique=True)
    description = models.TextField(verbose_name="Описание",)
    banner = models.ImageField(verbose_name="Баннер",upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True, )
    first_pic = models.ImageField(verbose_name="Первая картинка",upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True, )
    second_pic = models.ImageField(verbose_name="Вторая картинка",upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True, )
    third_pic = models.ImageField(verbose_name="Третья картинка",upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True, )
    description2 = models.TextField(verbose_name="Второе описание",default='')
    turn_on = models.BooleanField(verbose_name="ВКЛ/ВЫКЛ",default=False)
    creation_date = models.DateField(verbose_name="Дата создания",auto_now_add=True, null=True)
    able_to_del = models.BooleanField(default=True)
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'pages'


class PageImg(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    img = models.ImageField(verbose_name="",upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True, )

    class Meta:
        db_table = 'pages_imgs'


class Hall(models.Model):
    number = models.PositiveSmallIntegerField(verbose_name="Номер зала",)
    banner = models.ImageField(verbose_name="Баннер",upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True, )
    description = models.TextField(verbose_name="Описание",default='')
    num_tickets = models.PositiveSmallIntegerField(verbose_name="Кол-во биллетов",)
    scheme = models.ImageField(verbose_name="Cхема зала",upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True, )
    creation_date = models.DateField(verbose_name="Дата создания",auto_now_add=True)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, default=1)
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'halls'


class HallImg(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    img = models.ImageField(verbose_name='',upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True, )

    class Meta:
        db_table = 'halls_imgs'


class Seance(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField('%H:%M')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, null=False)
    tech_type = models.ForeignKey(TechnologyType, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'seances'


class Ticket(models.Model):
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE, null=False)
    price = models.PositiveSmallIntegerField()
    row = models.PositiveSmallIntegerField()
    seat = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'tickets'


class Stock(models.Model):
    name = models.CharField(verbose_name="Название",max_length=30, null=False)
    short_description = models.TextField(verbose_name="Краткое описание",max_length=50, default='')
    description = models.TextField(verbose_name="Описание",default='')
    creation_date = models.DateField(verbose_name="Дата создания",auto_now_add=True, null=True)
    turn_on = models.BooleanField(verbose_name="ВКЛ/ВЫКЛ",default=False)
    video_link = models.URLField(verbose_name="Ссылка на видео",)
    banner = models.ImageField(verbose_name="Баннер",upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True, )
    card_img = models.ImageField(verbose_name="Картинка карточки",upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True,)
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'stocks'


class StockImg(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    img = models.ImageField(upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True, )

    class Meta:
        db_table = 'stock_imgs'


class News(models.Model):
    name = models.CharField(verbose_name="Название",max_length=30, null=False)
    short_description = models.TextField(verbose_name="Краткое описание",max_length=50, default='')
    description = models.TextField(verbose_name="Описание",default='')
    creation_date = models.DateField(verbose_name="Дата создания",auto_now_add=True, null=True)
    turn_on = models.BooleanField(verbose_name="ВКЛ/ВЫКЛ",default=False)
    video_link = models.URLField(verbose_name="Ссылка на видео",)
    banner = models.ImageField(verbose_name="Баннер",upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True, )
    card_img = models.ImageField(upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True,
                                 verbose_name="Картинка карточки")
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'news'


class NewsImg(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    img = models.ImageField(verbose_name='', upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True, )

    class Meta:
        db_table = 'news_imgs'


class CafeBarMenu(models.Model):
    name = models.CharField(max_length=150)
    weight = models.PositiveIntegerField(null=True, verbose_name='Вес(грамм)')
    price = models.PositiveIntegerField(null=True, verbose_name='Цена')

    class Meta:
        db_table = 'cafe_bar_menu'