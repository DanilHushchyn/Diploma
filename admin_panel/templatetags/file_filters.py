import json
import os

import cloudinary
from django import template

register = template.Library()


@register.filter
def filename(value:str):

    return value.split('/')[-1]


@register.filter
def filesize(value):
    # print(cloudinary.CloudinaryImage(value).image().title())

    return 'os.path.getsize(value)'


