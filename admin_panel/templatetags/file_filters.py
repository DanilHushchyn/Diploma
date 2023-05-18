import json
import os

from django import template

register = template.Library()


@register.filter
def filename(value:str):

    return value.split('/')[-1]


@register.filter
def filesize(value):

    return 'os.path.getsize(value)'


