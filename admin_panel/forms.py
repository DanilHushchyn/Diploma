import django.forms as forms
from admin_panel.models import *


class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ('name',
                  'description',
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
                  'countries'

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

            'name': forms.TextInput(attrs={'size': 20, 'class': 'form__elem form__elem_text', }),
            'description': forms.Textarea(attrs={'size': 20, 'class': 'form__elem form__elem_textarea', }),
            'card_img': forms.FileInput(attrs={'size': 20, 'class': 'form__vertical-img', }),
            'released': forms.DateInput(attrs={'size': 20, 'class': 'form__elem form__elem_date', }),
            'trailer_link': forms.URLInput(attrs={'size': 20, 'class': 'form__elem form__elem_text', }),
            'banner': forms.FileInput(attrs={'size': 20, 'class': 'form__horizontal-img', }),
            'year': forms.TextInput(attrs={'size': 20, 'class': 'form__elem form__elem_text', }),
            'budget': forms.NumberInput(attrs={'size': 20, 'class': 'form__elem form__elem_number', }),
            'legal_age': forms.NumberInput(attrs={'size': 20, 'class': 'form__elem form__elem_number', }),
            'duration': forms.NumberInput(attrs={'size': 10, 'class': 'form__elem form__elem_number', }),
            'genres': forms.SelectMultiple(attrs={'class': 'form__elem'}),
            'editors': forms.SelectMultiple(attrs={'class': 'form__elem'}),
            'producers': forms.SelectMultiple(attrs={'type': 'checkbox', 'class': 'form__elem'}),
            'scriptwriters': forms.SelectMultiple(attrs={'type': 'checkbox', 'class': 'form__elem'}),
            'operators': forms.SelectMultiple(attrs={'type': 'checkbox', 'class': 'form__elem'}),
            'technology_types': forms.SelectMultiple(attrs={'type': 'checkbox', 'class': 'form__elem'}),
            'countries': forms.SelectMultiple(attrs={'type': 'checkbox', 'class': 'form__elem'}),
        }
        help_texts = {'name' : 'C большой буквы'}


class SeoBlockForm(forms.ModelForm):
    class Meta:
        model = SeoBlock
        fields = ('url', 'title', 'seo_description', 'keywords')

        widgets = {
            'url': forms.URLInput(attrs={'size': 20, 'class': 'form__elem', }),
            'title': forms.TextInput(attrs={'size': 20, 'class': 'form__elem', }),
            'seo_description': forms.Textarea(attrs={'size': 20, 'class': 'form__elem', }),
            'keywords': forms.TextInput(attrs={'size': 20, 'class': 'form__elem', }),
        }


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ('name', 'short_description', 'description', 'turn_on', 'video_link', 'banner', 'card_img')
        widgets = {

            'name': forms.TextInput(attrs={'size': 20, 'class': 'form__elem form__elem_text', }),
            'short_description': forms.Textarea(attrs={'size': 20, 'class': 'form__elem', }),
            'description': forms.Textarea(attrs={'size': 20, 'class': 'form__elem', }),
            'turn_on': forms.CheckboxInput(attrs={'size': 50, 'class': 'form__elem form__elem_switcher', }),
            'video_link': forms.URLInput(attrs={'size': 20, 'class': 'form__elem form__elem_text', }),
            'banner': forms.FileInput(attrs={'size': 20, 'class': 'form__horizontal-img', }),
            'card_img': forms.FileInput(attrs={'size': 20, 'class': 'form__vertical-img', }),

        }


class StockImgForm(forms.ModelForm):
    class Meta:
        model = StockImg
        fields = ('img',)
        widgets = {
            'img': forms.FileInput(attrs={
                'class': 'form__input-file-multi',
                'multiple': True,
            })
        }


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('name', 'banner', 'description', 'first_pic', 'second_pic', 'third_pic', 'description2', 'turn_on',)
        widgets = {

            'name': forms.TextInput(attrs={'size': 20, 'class': 'form__elem form__elem_text', }),
            'description': forms.Textarea(attrs={'size': 20, 'class': 'form__elem', }),
            'description2': forms.Textarea(attrs={'size': 20, 'class': 'form__elem', }),
            'turn_on': forms.CheckboxInput(attrs={'size': 20, 'class': 'form__elem form__elem_switcher', }),
            'banner': forms.FileInput(attrs={'size': 20, 'class': 'form__horizontal-img', }),
            'first_pic': forms.FileInput(attrs={'size': 20, 'class': 'form__horizontal-img_2', }),
            'second_pic': forms.FileInput(attrs={'size': 20, 'class': 'form__horizontal-img_3', }),
            'third_pic': forms.FileInput(attrs={'size': 20, 'class': 'form__horizontal-img_4', }),

        }


class PageUpdateForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('banner', 'description', 'first_pic', 'second_pic', 'third_pic', 'description2', 'turn_on',)
        widgets = {

            'description': forms.Textarea(attrs={'size': 20, 'class': 'form__elem', }),
            'description2': forms.Textarea(attrs={'size': 20, 'class': 'form__elem', }),
            'turn_on': forms.CheckboxInput(attrs={'size': 20, 'class': 'form__elem form__elem_switcher', }),
            'banner': forms.FileInput(attrs={'size': 20, 'class': 'form__horizontal-img', }),
            'first_pic': forms.FileInput(attrs={'size': 20, 'class': 'form__first-img', }),
            'second_pic': forms.FileInput(attrs={'size': 20, 'class': 'form__second-img', }),
            'third_pic': forms.FileInput(attrs={'size': 20, 'class': 'form__third-img', }),

        }


class PageImgForm(forms.ModelForm):
    class Meta:
        model = PageImg
        fields = ('img',)
        widgets = {
            'img': forms.FileInput(attrs={
                'class': 'form__input-file-multi',
                'multiple': True,
            })
        }


class MainPageForm(forms.ModelForm):
    class Meta:
        model = MainPage
        fields = ('number', 'number2', 'seo_text',)


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('name', 'short_description', 'description', 'turn_on', 'video_link', 'banner', 'card_img')
        widgets = {
            'name': forms.TextInput(attrs={'size': 20, 'class': 'form__elem form__elem_text', }),
            'description': forms.Textarea(attrs={'size': 20, 'class': 'form__elem', }),
            'short_description': forms.Textarea(attrs={'size': 20, 'class': 'form__elem', }),
            'turn_on': forms.CheckboxInput(attrs={'size': 20, 'class': 'form__elem form__elem_switcher', }),
            'banner': forms.FileInput(attrs={'size': 20, 'class': 'form__horizontal-img', }),
            'video_link': forms.URLInput(attrs={'size': 20, 'class': 'form__elem', }),
            'card_img': forms.FileInput(attrs={'size': 20, 'class': 'form__vertical-img', }),

        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'address', 'coordinate', 'logo',)


class NewsImgForm(forms.ModelForm):
    class Meta:
        model = NewsImg
        fields = ('img',)
        widgets = {
            'img': forms.FileInput(attrs={
                'class': 'form__input-file-multi',
                'multiple': True,
            })
        }


class HallForm(forms.ModelForm):
    class Meta:
        model = Hall
        fields = ('number', 'description', 'banner', 'num_tickets', 'scheme')
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form__elem'}),
            'description': forms.Textarea(attrs={'class': 'form__elem'}),
            'banner': forms.FileInput(attrs={'class': 'form__horizontal-img'}),
            'num_tickets': forms.NumberInput(attrs={'class': 'form__elem'}),
            'scheme': forms.FileInput(attrs={'class': 'form__horizontal-img_2'}),
        }


class HallImgForm(forms.ModelForm):
    class Meta:
        model = HallImg
        fields = ('img',)
        widgets = {
            'img': forms.FileInput(attrs={
                'class': 'form__input-file-multi',
                'multiple': True,
            }),
        }


class FilmImgForm(forms.ModelForm):
    class Meta:
        model = FilmImg
        fields = ('img',)
        widgets = {
            'img': forms.FileInput(attrs={'multiple': True, 'class': 'form__input-file-multi', })
        }


class CinemaImgForm(forms.ModelForm):
    class Meta:
        model = CinemaImg
        fields = ('img',)
        widgets = {
            'img': forms.FileInput(attrs={
                'class': 'form__input-file-multi',
                'multiple': True,
            })
        }


class CinemaForm(forms.ModelForm):
    class Meta:
        model = Cinema
        fields = ['name',
                  'description',
                  'banner',
                  'logo',
                  ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form__elem'}),
            'description': forms.Textarea(attrs={'class': 'form__elem'}),
            'banner': forms.FileInput(attrs={'class': 'form__horizontal-img'}),
            'logo': forms.FileInput(attrs={'class': 'form__horizontal-img_2'}),
        }


class CafeBarMenuForm(forms.ModelForm):
    class Meta:
        model = CafeBarMenu
        fields = ['name',
                  'weight',
                  'price',
                  ]


class TopCarouselForm(forms.ModelForm):
    class Meta:
        model = TopCarousel
        fields = [
            'img',
            'link',
            'title',
        ]
        widgets = {
            'img': forms.FileInput(attrs={'class': 'form__horizontal-img'}),
            'link': forms.URLInput(attrs={'class': 'form__elem', 'placeholder': 'Ссылка'}),
            'title': forms.TextInput(attrs={'class': 'form__elem', 'placeholder': 'Заголовок'}),
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
        (1, '1 сек'),
        (2, '2 сек'),
        (3, '3 сек'),
        (4, '4 сек'),
        (5, '5 сек'),
        (6, '6 сек'),
        (7, '7 сек'),
        (8, '8 сек'),
        (9, '9 сек'),
        (10, '10 сек'),
    )
    interval = forms.ChoiceField(choices=interval_choices,label='Скорость вращения')



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
