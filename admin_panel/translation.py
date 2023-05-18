from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(Stock)
class StockTranslationOptions(TranslationOptions):
    fields = ('name', 'short_description', 'description')


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('name', 'short_description', 'description')


@register(Contact)
class ContactTranslationOptions(TranslationOptions):
    fields = ('name', 'address')


@register(Cinema)
class CinemaTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'description2')


@register(Hall)
class HallTranslationOptions(TranslationOptions):
    fields = ('description',)


@register(CafeBarMenu)
class CafeBarMenuTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Operator)
class OperatorTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Editor)
class EditorTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(ScriptWriter)
class ScriptWriterTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Producer)
class ProducerTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(TechnologyType)
class TechnologyTypeTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Film)
class FilmTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(SeoBlock)
class SeoBlockTranslationOptions(TranslationOptions):
    fields = ('title', 'seo_description', 'keywords')


@register(TopCarousel)
class TopCarouselTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(MainPage)
class MainPageCarouselTranslationOptions(TranslationOptions):
    fields = ('seo_text',)
