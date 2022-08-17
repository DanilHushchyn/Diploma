from django.db import models
from django.db import models


class TopCarousel(models.Model):
    img = models.ImageField(verbose_name='', upload_to='photos/%Y/%m/%d/', max_length=100, unique=True, null=True)
    link = models.URLField(verbose_name='', default='')
    title = models.CharField(verbose_name='', max_length=50, default='')

    interval = 5

    class Meta:
        db_table = 'top_carousel'


class BackImg(models.Model):
    img = models.ImageField(verbose_name='', upload_to='photos/%Y/%m/%d/', max_length=100, unique=True, null=True)

    class Meta:
        db_table = 'back_img'


class BottomCarousel(models.Model):
    img = models.ImageField(verbose_name='', upload_to='photos/%Y/%m/%d/', max_length=100, unique=True, null=True)
    link = models.URLField(verbose_name='', default='')

    interval = 5

    class Meta:
        db_table = 'bottom_carousel'
