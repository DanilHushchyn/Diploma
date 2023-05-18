from datetime import date

import django.forms as forms
from django.utils.translation import gettext_lazy as _

from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields
from modeltranslation.forms import TranslationModelForm

from admin_panel.models import *


class FilmForm(forms.ModelForm):
    """
        Эти два атрибута поддерживаются обеими разновидностями форм: и связанными с моделями, и не связанными с ними.
        required_css_class - имя стилевого класса, которым будут помечаться элементы управления,
        обязательные для заполнения;
        error_css_class - имя стилевого класса, которым будут помечаться элементы
        управления с некорректными данными.
    """
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = Film
        fields = (
            'name_ru',
            'name_en',
            'description_ru',
            'description_en',
            'card_img',
            'released',
            'trailer_link',
            'banner',
            'year',
            'budget',
            'legal_age',
            'duration',
            'genres',
            'producers',
            'editors',
            'scriptwriters',
            'operators',
            'technology_types',
            'countries',

        )

        genres = forms.ModelMultipleChoiceField(
            queryset=Genre.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )
        producers = forms.ModelMultipleChoiceField(
            queryset=Producer.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )
        scriptwriters = forms.ModelMultipleChoiceField(
            queryset=ScriptWriter.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )
        countries = forms.ModelMultipleChoiceField(
            queryset=Country.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )
        operators = forms.ModelMultipleChoiceField(
            queryset=Operator.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )
        technology_types = forms.ModelMultipleChoiceField(
            queryset=TechnologyType.objects.all(),
            widget=forms.CheckboxSelectMultiple,

        )
        widgets = {
            'name_ru': forms.TextInput(attrs={'size': 20, 'class': 'form__elem form__elem_text', }),
            'name_en': forms.TextInput(attrs={'size': 20, 'class': 'form__elem form__elem_text', }),
            'description_ru': forms.Textarea(
                attrs={'maxlength': 10_000, 'size': 20, 'class': 'form__elem form__elem_textarea', }),
            'description_en': forms.Textarea(
                attrs={'maxlength': 10_000, 'size': 20, 'class': 'form__elem form__elem_textarea', }),
            'card_img': forms.FileInput(attrs={'size': 20, 'id': 'card-img', }),
            'released': forms.DateInput(attrs={'size': 20, 'class': 'form__elem form__elem_date', 'type': 'date'},
                                        format=('%Y-%m-%d')),
            'trailer_link': forms.URLInput(attrs={'size': 20, 'class': 'form__elem form__elem_text', }),
            'banner': forms.FileInput(attrs={'size': 20, 'id': 'banner-img', }),
            'year': forms.TextInput(
                attrs={'size': 20, 'class': 'form__elem form__elem_number', 'type': 'number', 'min': 1900,
                       'max': 2100}, ),
            'budget': forms.NumberInput(attrs={'size': 20, 'class': 'form__elem form__elem_number', }),
            'legal_age': forms.NumberInput(attrs={'size': 20, 'class': 'form__elem form__elem_number', }),
            'duration': forms.NumberInput(
                attrs={'size': 10, 'class': 'form__elem form__elem_number', 'placeholder': 'В минутах'}),
            'genres': forms.SelectMultiple(attrs={'class': ''}),
            'editors': forms.SelectMultiple(attrs={'class': ''}),
            'producers': forms.SelectMultiple(attrs={'type': 'checkbox', 'class': ''}),
            'scriptwriters': forms.SelectMultiple(attrs={'type': 'checkbox', 'class': ''}),
            'operators': forms.SelectMultiple(attrs={'type': 'checkbox', 'class': ''}),
            'technology_types': forms.SelectMultiple(attrs={'type': 'checkbox', 'class': ''}),
            'countries': forms.SelectMultiple(attrs={'type': 'checkbox', 'class': ''}),
        }
        help_texts = {'name': 'C большой буквы'}


class SeoBlockForm(forms.ModelForm):
    class Meta:
        model = SeoBlock
        fields = (
        'url', 'title_ru', 'title_en', 'seo_description_ru', 'seo_description_en', 'keywords_ru', 'keywords_en',)

        widgets = {
            'url': forms.URLInput(attrs={'size': 20, 'class': 'form__elem', }),
            'title_ru': forms.TextInput(attrs={'size': 20, 'class': 'form__elem', }),
            'title_en': forms.TextInput(attrs={'size': 20, 'class': 'form__elem', }),
            'seo_description_ru': forms.Textarea(attrs={"maxlength": 10_000, 'size': 20, 'class': 'form__elem', }),
            'seo_description_en': forms.Textarea(attrs={"maxlength": 10_000, 'size': 20, 'class': 'form__elem', }),
            'keywords_ru': forms.TextInput(attrs={'size': 20, 'class': 'form__elem', }),
            'keywords_en': forms.TextInput(attrs={'size': 20, 'class': 'form__elem', }),
        }


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = (
        'name_ru', 'name_en', 'short_description_ru', 'short_description_en', 'description_ru', 'description_en',
        'turn_on', 'video_link', 'banner', 'card_img')
        widgets = {

            'name_en': forms.TextInput(attrs={'size': 20, 'class': 'form__elem form__elem_text', }),
            'name_ru': forms.TextInput(attrs={'size': 20, 'class': 'form__elem form__elem_text', }),
            'short_description_en': forms.Textarea(attrs={"maxlength": 250, 'size': 20, 'class': 'form__elem', }),
            'short_description_ru': forms.Textarea(attrs={"maxlength": 250, 'size': 20, 'class': 'form__elem', }),
            'description_en': forms.Textarea(attrs={"maxlength": 10_000, 'size': 20, 'class': 'form__elem', }),
            'description_ru': forms.Textarea(attrs={"maxlength": 10_000, 'size': 20, 'class': 'form__elem', }),
            'turn_on': forms.CheckboxInput(attrs={'size': 50, 'class': 'form__elem on_off', }),
            'video_link': forms.URLInput(attrs={'size': 20, 'class': 'form__elem form__elem_text', }),
            'banner': forms.FileInput(attrs={'size': 20, 'id': 'banner-img', 'class': 'form__horizontal-img', }),
            'card_img': forms.FileInput(attrs={'size': 20, 'id': 'card-img', 'class': 'form__vertical-img', }),

        }


class StockImgForm(forms.ModelForm):
    class Meta:
        model = StockImg
        fields = ('img',)
        widgets = {
            'img': forms.FileInput(attrs={
                'class': 'gallery d-none',
                'multiple': True,
            })
        }


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = (
        'name_ru', 'name_en', 'banner', 'description_ru', 'description_en', 'first_pic', 'second_pic', 'third_pic',
        'description2_ru', 'description2_en', 'turn_on',)
        widgets = {

            'name_en': forms.TextInput(attrs={'size': 20, 'class': 'form__elem form__elem_text', }),
            'name_ru': forms.TextInput(attrs={'size': 20, 'class': 'form__elem form__elem_text', }),
            'description_en': forms.Textarea(attrs={"maxlength": 10_000, 'size': 20, 'class': 'form__elem', }),
            'description_ru': forms.Textarea(attrs={"maxlength": 10_000, 'size': 20, 'class': 'form__elem', }),
            'description2_en': forms.Textarea(attrs={"maxlength": 10_000, 'size': 20, 'class': 'form__elem', }),
            'description2_ru': forms.Textarea(attrs={"maxlength": 10_000, 'size': 20, 'class': 'form__elem', }),
            'turn_on': forms.CheckboxInput(attrs={'size': 20, 'type': 'checkbox', 'class': 'on_off', }),
            'banner': forms.FileInput(attrs={'size': 20, 'id': 'banner-img', 'class': 'form__horizontal-img', }),
            'first_pic': forms.FileInput(attrs={'size': 20, 'id': 'pic1', 'class': 'form__horizontal-img_2', }),
            'second_pic': forms.FileInput(attrs={'size': 20, 'id': 'pic2', 'class': 'form__horizontal-img_3', }),
            'third_pic': forms.FileInput(attrs={'size': 20, 'id': 'pic3', 'class': 'form__horizontal-img_4', }),

        }


class PageUpdateForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = (
        'banner', 'description_ru', 'description_en', 'first_pic', 'second_pic', 'third_pic', 'description2_ru',
        'description2_en', 'turn_on',)
        widgets = {

            'description_en': forms.Textarea(attrs={"maxlength": 10_000, 'size': 20, 'class': 'form__elem', }),
            'description_ru': forms.Textarea(attrs={"maxlength": 10_000, 'size': 20, 'class': 'form__elem', }),
            'description2_en': forms.Textarea(attrs={"maxlength": 10_000, 'size': 20, 'class': 'form__elem', }),
            'description2_ru': forms.Textarea(attrs={"maxlength": 10_000, 'size': 20, 'class': 'form__elem', }),
            'turn_on': forms.CheckboxInput(attrs={'size': 20, 'class': 'on_off', }),
            'banner': forms.FileInput(attrs={'size': 20, 'id': 'banner-img', 'class': 'form__horizontal-img', }),
            'first_pic': forms.FileInput(
                attrs={'size': 20, 'id': 'pic1', 'class': 'form__first-img form__horizontal-img_2', }),
            'second_pic': forms.FileInput(
                attrs={'size': 20, 'id': 'pic2', 'class': 'form__second-img form__horizontal-img_3', }),
            'third_pic': forms.FileInput(
                attrs={'size': 20, 'id': 'pic3', 'class': 'form__third-img form__horizontal-img_4', }),

        }


class PageImgForm(forms.ModelForm):
    class Meta:
        model = PageImg
        fields = ('img',)
        widgets = {
            'img': forms.FileInput(attrs={
                'class': 'gallery d-none',
                'multiple': True,
            })
        }


class MainPageForm(forms.ModelForm):
    class Meta:
        model = MainPage
        fields = ('number', 'number2', 'seo_text_ru', 'seo_text_en',)


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = (
        'name_ru', 'name_en', 'short_description_ru', 'short_description_en', 'description_ru', 'description_en',
        'turn_on', 'video_link', 'banner', 'card_img')
        widgets = {
            'name_ru': forms.TextInput(attrs={'size': 20, 'class': 'form__elem form__elem_text', }),
            'name_en': forms.TextInput(attrs={'size': 20, 'class': 'form__elem form__elem_text', }),
            'description_ru': forms.Textarea(attrs={"maxlength": 10_000, 'size': 20, 'class': 'form__elem', }),
            'description_en': forms.Textarea(attrs={"maxlength": 10_000, 'size': 20, 'class': 'form__elem', }),
            'short_description_ru': forms.Textarea(attrs={"maxlength": 250, 'size': 20, 'class': 'form__elem', }),
            'short_description_en': forms.Textarea(attrs={"maxlength": 250, 'size': 20, 'class': 'form__elem', }),
            'turn_on': forms.CheckboxInput(attrs={'size': 20, 'class': 'form__elem on_off', }),
            'banner': forms.FileInput(attrs={'size': 20, 'id': 'banner-img', 'class': 'form__horizontal-img', }),
            'video_link': forms.URLInput(attrs={'size': 20, 'class': 'form__elem', }),
            'card_img': forms.FileInput(attrs={'size': 20, 'id': 'card-img', 'class': 'form__vertical-img', }),

        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name_ru', 'name_en', 'address_ru', 'address_en', 'coordinate', 'logo',)
        widgets = {
            'logo': forms.FileInput(attrs={'class': 'form__horizontal-img', }),
        }


class NewsImgForm(forms.ModelForm):
    class Meta:
        model = NewsImg
        fields = ('img',)
        widgets = {
            'img': forms.FileInput(attrs={
                'class': 'gallery d-none',
                'multiple': True,
            })
        }


class HallForm(forms.ModelForm):
    class Meta:
        model = Hall
        fields = ('number', 'description_ru', 'description_en', 'banner', 'num_tickets', 'scheme', 'scheme_html')
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form__elem'}),
            'description_ru': forms.Textarea(attrs={"maxlength": 10_000, 'class': 'form__elem'}),
            'description_en': forms.Textarea(attrs={"maxlength": 10_000, 'class': 'form__elem'}),
            'banner': forms.FileInput(attrs={'id': 'banner-img', 'class': 'form__horizontal-img'}),
            'num_tickets': forms.NumberInput(attrs={'class': 'form__elem'}),
            'scheme': forms.FileInput(attrs={'id': 'scheme-img', 'class': 'form__horizontal-img_2'}),
            'scheme_html': forms.Textarea(attrs={'class': 'form__elem scheme_html'}),
        }


class HallImgForm(forms.ModelForm):
    class Meta:
        model = HallImg
        fields = ('img',)
        widgets = {
            'img': forms.FileInput(attrs={
                'class': 'gallery d-none',
                'multiple': True,
            }),
        }


class FilmImgForm(forms.ModelForm):
    class Meta:
        model = FilmImg
        fields = ('img',)
        widgets = {
            'img': forms.FileInput(attrs={
                'multiple': True,
                'class': 'gallery d-none',
            })
        }


class CinemaImgForm(forms.ModelForm):
    class Meta:
        model = CinemaImg
        fields = ('img',)
        widgets = {
            'img': forms.FileInput(attrs={
                'class': 'gallery d-none',
                'multiple': True,
            }),
        }


class CinemaForm(forms.ModelForm):
    class Meta:
        model = Cinema
        fields = [
            'name_ru',
            'name_en',
            'description_ru',
            'description_en',
            'banner',
            'logo',
        ]
        widgets = {
            'name_en': forms.TextInput(attrs={'class': 'form__elem'}),
            'name_ru': forms.TextInput(attrs={'class': 'form__elem'}),
            'description_en': forms.Textarea(attrs={"maxlength": 10_000, 'class': 'form__elem'}),
            'description_ru': forms.Textarea(attrs={"maxlength": 10_000, 'class': 'form__elem'}),
            'banner': forms.FileInput(attrs={'class': 'banner-img', 'multiple': True}),
            'logo': forms.FileInput(attrs={'size': 20, 'class': 'logo-img'}),
        }


class CafeBarMenuForm(forms.ModelForm):
    class Meta:
        model = CafeBarMenu
        fields = [
            'name_ru',
            'name_en',
            'weight',
            'price',
        ]


class TopCarouselForm(forms.ModelForm):
    class Meta:
        model = TopCarousel
        fields = [
            'img',
            'link',
            'title_ru',
            'title_en',
        ]
        widgets = {
            'img': forms.FileInput(attrs={'class': 'form__horizontal-img'}),
            'link': forms.URLInput(attrs={'class': 'form__elem', 'placeholder': 'Ссылка'}),
            'title_en': forms.TextInput(attrs={'class': 'form__elem', 'placeholder': 'Заголовок'}),
            'title_ru': forms.TextInput(attrs={'class': 'form__elem', 'placeholder': 'Заголовок'}),
        }


class BottomCarouselForm(forms.ModelForm):
    class Meta:
        model = BottomCarousel
        fields = [
            'img',
            'link',
        ]
        widgets = {
            'img': forms.FileInput(attrs={'class': 'form__horizontal-img'}),
            'link': forms.URLInput(attrs={'class': 'form__elem', 'placeholder': 'Ссылка'}),
        }


class FormInterval(forms.Form):
    interval_choices = (
        (None, '---------'),
        (1, _('1 сек')),
        (2, _('2 сек')),
        (3, _('3 сек')),
        (4, _('4 сек')),
        (5, _('5 сек')),
        (6, _('6 сек')),
        (7, _('7 сек')),
        (8, _('8 сек')),
        (9, _('9 сек')),
        (10, _('10 сек')),

    )
    interval = forms.ChoiceField(choices=interval_choices, label=_('Скорость вращения'))


# class FormBottomCarouselInterval(forms.Form):
#     interval = forms.ChoiceField(choices=interval_choices)

# class FormBottomCarouselInterval(forms.Form):
#     interval = forms.ChoiceField(choices=interval_choices)

class BackImgForm(forms.ModelForm):
    class Meta:
        model = BackImg
        fields = [
            'img',
        ]
        widgets = {
            'img': forms.FileInput(attrs={'class': 'form__vertical-img'}),
        }


class BookingForm(forms.Form):
    booked = forms.BooleanField(label='', widget=forms.CheckboxInput())
    row = forms.IntegerField(label='', widget=forms.TextInput(attrs={'type': 'hidden'}))


today_date = date.today()
filmQuery = Film.objects.filter(released__lt=today_date)

class SeanceForm(forms.ModelForm):
    class Meta:
        model = Seance

        fields = (
            'hall',
            'price',
            'date',
            'time',
            'film',
            'tech_type',
        )
        hall = forms.ModelChoiceField(
            queryset=Hall.objects.all(),
            widget=forms.RadioSelect,

        )
        film = forms.ModelChoiceField(
            queryset=filmQuery,
            widget=forms.RadioSelect,

        )
        widgets = {
            'hall': forms.RadioSelect(attrs={'class': 'form__elem form__elem_radio'}),
            'price': forms.TextInput(attrs={'class': 'form__elem'}),
            'date': forms.DateInput(attrs={'class': 'form__elem','type':'date'}, format=('%Y-%m-%d')),
            'film': forms.RadioSelect(attrs={'class': 'form__elem form__elem_radio'}),
            'time': forms.TimeInput(attrs={'class': 'form__elem'}),
            'tech_type': forms.RadioSelect(attrs={'class': 'form__elem form__elem_radio', }),
        }


class TemplateHtmlForm(forms.ModelForm):
    class Meta:
        model = TemplateHtml
        fields = ('template_html',)
        widgets = {
            'template_html': forms.FileInput(attrs={'class': 'file-html', 'required': False})
        }
