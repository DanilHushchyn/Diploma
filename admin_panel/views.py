from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from admin_panel import forms as my_forms
from user import forms as user_forms
from django.forms import inlineformset_factory, modelformset_factory
# Create your views here.
from admin_panel.models import *
from datetime import date


def statistic(request):
    data = {'users_count': User.objects.count()}
    return render(request, 'admin_panel/statistic.html', context=data)


def clients(request):
    data = {'users': User.objects.all()
            }
    return render(request, 'admin_panel/clients.html', context=data)


def update_client(request, id):
    client = User.objects.get(id=id)
    if request.method == 'POST':
        client_form = user_forms.UserForm(request.POST, instance=client)
        if client_form.is_valid():
            client_form.save()
            return redirect('clients')
    client_form = user_forms.UserForm(instance=client)
    data = {'client_form': client_form, 'client_id': id}
    return render(request, 'admin_panel/update_client.html', context=data)


def delete_client(request, id):
    client = User.objects.get(id=id)
    client.delete()
    data = {'users': User.objects.all()
            }
    return render(request, 'admin_panel/clients.html', context=data)


# Create your views here.
# def films(request):
#     if request.method == 'POST':
#         filmImgFormSet = modelformset_factory(FilmImg, form=my_forms.FilmImgForm, extra=1, )
#         gallery_formset = filmImgFormSet(request.POST, request.FILES)
#         film_form = my_forms.FilmForm(request.POST, request.FILES)
#         seo_block = my_forms.SeoBlockForm(request.POST)
#         if seo_block.is_valid():
#             print('okKKKKKKKKKKK',film_form.is_valid(),gallery_formset.is_valid())
#             print('okKKKKKKKKKKK',film_form.errors)
#             seo_obj = seo_block.save()
#             if film_form.is_valid() and gallery_formset.is_valid():
#                 print('okKKKKKKKKKKK2222')
#
#                 film_obj = film_form.save()
#                 film_obj.seo_block_id = seo_obj.id
#                 film_obj.save()
#                 for form in gallery_formset.cleaned_data:
#                     if form:
#                         print('okKKKKKKKKKKK33333')
#
#                         FilmImg.objects.create(img=form['img'], film_id=film_obj.id)
#
#     films = Film.objects.all()
#
#     data = {'films': films, 'title': 'Фильмы'}
#     return render(request, 'admin_panel/films2.html', context=data)

def films(request):
    if request.method == 'POST':
        filmImgForm = my_forms.FilmImgForm(request.POST, request.FILES)
        film_form = my_forms.FilmForm(request.POST, request.FILES)
        seo_block = my_forms.SeoBlockForm(request.POST)
        if seo_block.is_valid():
            seo_obj = seo_block.save()
            if film_form.is_valid() and filmImgForm.is_valid():
                film_obj = film_form.save()
                film_obj.seo_block_id = seo_obj.id
                film_obj.save()
                for file in request.FILES.getlist('img'):
                    FilmImg.objects.create(img=file, film_id=film_obj.id)
    start_date = date.today()
    released_films = Film.objects.filter(released__lte=start_date)
    unreleased_films = Film.objects.filter(released__gte=start_date)
    data = {
        'films': {
            'released_films': released_films,
            'unreleased_films': unreleased_films,
        },
        'title': 'Фильмы'
    }
    return render(request, 'admin_panel/films2.html', context=data)


def cinemas(request):
    if request.method == "POST":
        hall_form = my_forms.HallForm(request.POST, request.FILES)
        seo_form = my_forms.SeoBlockForm(request.POST)
        hall_gallery_form = my_forms.HallImgForm(request.POST, request.FILES)
        if seo_form.is_valid():
            seo_obj = seo_form.save()
            if hall_form.is_valid() and hall_gallery_form.is_valid():
                hall_obj = hall_form.save()
                hall_obj.seo_block_id = seo_obj.id
                hall_obj.cinema_id = 1
                hall_obj.save()
                for file in request.FILES.getlist('img'):
                    if file:
                        HallImg.objects.create(img=file, hall_id=hall_obj.id)

    cinemas = Cinema.objects.all()
    data = {'cinemas': cinemas}
    return render(request, 'admin_panel/cinemas.html', context=data)


def choose_client(request):
    return render(request, 'admin_panel/choose_client.html')


def mailing(request):
    return render(request, 'admin_panel/mailing.html')


def stocks(request):
    if request.method == "POST":
        stock_form = my_forms.StockForm(request.POST, request.FILES)
        seo_form = my_forms.SeoBlockForm(request.POST)
        gallery_stock_form = my_forms.StockImgForm(request.POST, request.FILES)
        if seo_form.is_valid():
            seo_obj = seo_form.save()
            if stock_form.is_valid() and gallery_stock_form.is_valid():
                stock_obj = stock_form.save()
                stock_obj.seo_block_id = seo_obj.id
                stock_obj.save()
                for file in request.FILES.getlist('img'):
                    if file:
                        StockImg.objects.create(img=file, stock_id=stock_obj.id)

    stocks = Stock.objects.all()
    data = {'stocks': stocks}
    return render(request, 'admin_panel/stocks2.html', context=data)


def get_stock_form(request):
    stockImgs_form = my_forms.StockImgForm()
    stock_form = my_forms.StockForm()
    seo_form = my_forms.SeoBlockForm()

    data = {'stock_form': stock_form, 'stockImgs_form': stockImgs_form, 'seo_form': seo_form}
    return render(request, 'admin_panel/stock_form.html', context=data)


def update_stock(request, id):
    stock = Stock.objects.get(id=id)
    if request.method == 'POST':
        stock_form = my_forms.StockForm(request.POST, request.FILES, instance=stock)
        seo_obj = SeoBlock.objects.get(id=stock.seo_block.id)
        seo_form = my_forms.SeoBlockForm(request.POST, instance=seo_obj)
        if stock_form.is_valid() and seo_form.is_valid():
            stock_form.save()
            seo_form.save()
            return redirect('stocks_table')

    stock_form = my_forms.StockForm(instance=stock)
    seo_obj = SeoBlock.objects.get(id=stock.seo_block.id)
    seo_form = my_forms.SeoBlockForm(instance=seo_obj)
    data = {'stock_form': stock_form, 'stock_id': stock.id, 'seo_form': seo_form}
    return render(request, 'admin_panel/stock_update2.html', context=data)


def delete_stock(request, id):
    stock = Stock.objects.get(id=id)
    seo_block = SeoBlock.objects.get(id=stock.seo_block.id)
    seo_block.delete()
    stock.delete()

    return redirect('stocks_table')


def news(request):
    if request.method == "POST":
        news_form = my_forms.NewsForm(request.POST, request.FILES)
        seo_form = my_forms.SeoBlockForm(request.POST)
        newsImgFormSet = modelformset_factory(NewsImg, form=my_forms.NewsImgForm, extra=1, )
        gallery_formset = newsImgFormSet(request.POST, request.FILES)

        if seo_form.is_valid():

            seo_obj = seo_form.save()
            if news_form.is_valid() and gallery_formset.is_valid():

                news_obj = news_form.save()
                news_obj.seo_block_id = seo_obj.id
                news_obj.save()
                for form in gallery_formset.cleaned_data:
                    if form:
                        NewsImg.objects.create(img=form['img'], news_id=news_obj.id)

    news_list = News.objects.all()
    data = {'news_list': news_list}
    return render(request, 'admin_panel/news2.html', context=data)


def get_news_form(request):
    newsImgs_form = my_forms.NewsImgForm()
    news_form = my_forms.NewsForm()
    seo_form = my_forms.SeoBlockForm()

    data = {'news_form': news_form, 'newsImgs_form': newsImgs_form, 'seo_form': seo_form}
    return render(request, 'admin_panel/news_form.html', context=data)


def update_news(request, id):
    news = News.objects.get(id=id)
    if request.method == 'POST':
        news_form = my_forms.NewsForm(request.POST, request.FILES, instance=news)
        seo_obj = SeoBlock.objects.get(id=news.seo_block.id)
        seo_form = my_forms.SeoBlockForm(request.POST, instance=seo_obj)
        if news_form.is_valid() and seo_form.is_valid():
            news_form.save()
            seo_form.save()
            return redirect('news_table')

    news_form = my_forms.NewsForm(instance=news)
    seo_obj = SeoBlock.objects.get(id=news.seo_block.id)
    seo_form = my_forms.SeoBlockForm(instance=seo_obj)
    data = {'news_form': news_form, 'news_id': news.id, 'seo_form': seo_form}
    return render(request, 'admin_panel/news_update2.html', context=data)


def delete_news(request, id):
    news = News.objects.get(id=id)
    seo_block = SeoBlock.objects.get(id=news.seo_block.id)
    seo_block.delete()
    news.delete()

    return redirect('news_table')


# def get_film_form(request):
#     filmImgFormSet = modelformset_factory(FilmImg, form=my_forms.FilmImgForm, extra=1)
#     filmImg_form = filmImgFormSet(queryset=FilmImg.objects.none())
#
#     film_form = my_forms.FilmForm()
#     seo = my_forms.SeoBlockForm()
#
#     data = {'form': film_form, 'filmImg_form': filmImg_form, 'seo_form': seo}
#     return render(request, 'admin_panel/film_form.html', context=data)
def get_film_form(request):
    filmImgForm = my_forms.FilmImgForm()

    film_form = my_forms.FilmForm()
    seo = my_forms.SeoBlockForm()
    data = {'form': film_form, 'filmImg_form': filmImgForm, 'seo_form': seo}
    return render(request, 'admin_panel/film_form.html', context=data)


def cinema_card(request, name):
    cinema = Cinema.objects.get(name=name)
    if request.method == 'POST':
        cinema_form = my_forms.CinemaForm(request.POST, request.FILES, instance=cinema)
        seo_obj = SeoBlock.objects.get(id=cinema.seo_block.id)
        seo_form = my_forms.SeoBlockForm(request.POST, instance=seo_obj)
        if cinema_form.is_valid() and seo_form.is_valid():
            cinema_form.save()
            seo_form.save()
            return redirect('admin_cinemas')
        else:
            cinema_form = my_forms.CinemaForm(instance=cinema)
            seo_obj = SeoBlock(id=cinema.seo_block.id)
            seo_form = my_forms.SeoBlockForm(instance=seo_obj)
            data = {'form': cinema_form, 'cinema_name': cinema.name, 'seo_form': seo_form}
            return render(request, 'admin_panel/cinema_card.html', context=data)
    seo_obj = SeoBlock.objects.get(id=cinema.seo_block.id)
    seo_form = my_forms.SeoBlockForm(instance=seo_obj)
    halls = Hall.objects.filter(cinema_id=cinema.id)
    cinema_form = my_forms.CinemaForm(instance=cinema)
    data = {'form': cinema_form, 'cinema_name': cinema.name, 'seo_form': seo_form, 'halls': halls}
    return render(request, 'admin_panel/cinema_update.html', context=data)


def get_hall_form(request):
    hallImgs_form = my_forms.HallImgForm()
    hall_form = my_forms.HallForm()
    seo_form = my_forms.SeoBlockForm()

    data = {'hall_form': hall_form, 'hallImgs_form': hallImgs_form, 'seo_form': seo_form}
    return render(request, 'admin_panel/hall_form.html', context=data)


def banners_sliders(request):
    TopCarouselFormset = modelformset_factory(TopCarousel, form=my_forms.TopCarouselForm, extra=0, can_delete=True)
    top_carousel_formset = TopCarouselFormset(queryset=TopCarousel.objects.all(), prefix='top_carousel')
    top_carousel_model = TopCarousel.objects.all()

    BottomCarouselFormset = modelformset_factory(BottomCarousel, form=my_forms.BottomCarouselForm, extra=0,
                                                 can_delete=True)
    bottom_carousel_formset = BottomCarouselFormset(queryset=BottomCarousel.objects.all(), prefix='bottom_carousel')
    bottom_carousel_model = BottomCarousel.objects.all()

    interval = my_forms.FormInterval()

    back_img_form = my_forms.BackImgForm()
    data = {
        'top_carousel': zip(top_carousel_model, top_carousel_formset),
        'bottom_carousel': zip(bottom_carousel_model, bottom_carousel_formset),

        'top_carousel_formset': top_carousel_formset,
        'bottom_carousel_formset': bottom_carousel_formset,

        'back_img_form': back_img_form,
        'interval': interval,
    }
    return render(request, 'admin_panel/banners_sliders2.html', context=data)


def top_carousel(request):
    TopCarouselFormSet = modelformset_factory(TopCarousel, form=my_forms.TopCarouselForm, extra=0, can_delete=True)
    top_carousel_formset = TopCarouselFormSet(request.POST, request.FILES, prefix='top_carousel')

    interval = my_forms.FormInterval(request.POST)

    if top_carousel_formset.is_valid() and interval.is_valid():
        TopCarousel.interval = interval.cleaned_data['interval']
        top_carousel_formset.save()

    return redirect('banners_sliders')


def bottom_carousel(request):
    BottomCarouselFormSet = modelformset_factory(BottomCarousel, form=my_forms.BottomCarouselForm, extra=0,
                                                 can_delete=True)
    bottom_carousel_formset = BottomCarouselFormSet(request.POST, request.FILES, prefix='bottom_carousel')

    interval = my_forms.FormInterval(request.POST)

    if bottom_carousel_formset.is_valid() and interval.is_valid():
        BottomCarousel.interval = interval.cleaned_data['interval']
        bottom_carousel_formset.save()

    return redirect('banners_sliders')


def back_img(request):
    back_img_form = my_forms.BackImgForm(request.POST, request.FILES)
    if back_img_form.is_valid():
        BackImg.objects.all().delete()
        back_img_form.save()

    return redirect('banners_sliders')


def pages(request):
    if request.method == "POST":
        page_form = my_forms.PageForm(request.POST, request.FILES)
        seo_form = my_forms.SeoBlockForm(request.POST)
        pageImgForm = my_forms.PageImgForm(request.POST, request.FILES)

        if seo_form.is_valid():

            seo_obj = seo_form.save()
            if page_form.is_valid() and pageImgForm.is_valid():

                page_obj = page_form.save()
                page_obj.seo_block_id = seo_obj.id
                page_obj.save()
                for file in request.FILES.getlist('img'):
                    if file:
                        PageImg.objects.create(img=file, page_id=page_obj.id)

    page_list = Page.objects.all()
    data = {'page_list': page_list}
    return render(request, 'admin_panel/pages2.html', context=data)


def get_page_form(request):
    pageImgs_form = my_forms.PageImgForm()
    page_form = my_forms.PageForm()
    seo_form = my_forms.SeoBlockForm()

    data = {'page_form': page_form, 'pageImgs_form': pageImgs_form, 'seo_form': seo_form}
    return render(request, 'admin_panel/page_form.html', context=data)


def update_page(request, id):
    page = Page.objects.get(id=id)

    if request.method == 'POST':

        page_form = my_forms.PageUpdateForm(request.POST, request.FILES, instance=page)
        seo_obj = SeoBlock.objects.get(id=page.seo_block.id)
        seo_form = my_forms.SeoBlockForm(request.POST, instance=seo_obj)
        if page_form.is_valid() and seo_form.is_valid():
            page_form.save()
            seo_form.save()
            return redirect('pages')

    page_form = my_forms.PageUpdateForm(instance=page)
    seo_obj = SeoBlock.objects.get(id=page.seo_block.id)
    seo_form = my_forms.SeoBlockForm(instance=seo_obj)

    data = {'page_form': page_form, 'page_id': page.id, 'seo_form': seo_form}
    if page.name == 'Кафе-Бар':
        menuFormset = modelformset_factory(can_delete=True, model=CafeBarMenu, form=my_forms.CafeBarMenuForm, extra=1)
        menu_formset = menuFormset(queryset=CafeBarMenu.objects.all())
        data['menu_formset'] = menu_formset
        data['labels'] = my_forms.CafeBarMenuForm
        return render(request, 'admin_panel/cafe_bar_update.html', context=data)
    return render(request, 'admin_panel/page_update2.html', context=data)


def delete_page(request, id):
    page = Page.objects.get(id=id)
    seo_block = SeoBlock.objects.get(id=page.seo_block.id)
    seo_block.delete()
    page.delete()

    return redirect('pages')


def update_film(request, name):
    film = Film.objects.get(name=name)
    if request.method == 'POST':

        film_form = my_forms.FilmForm(request.POST, request.FILES, instance=film)
        seo_obj = SeoBlock.objects.get(id=film.seo_block.id)
        seo_form = my_forms.SeoBlockForm(request.POST, instance=seo_obj)
        if film_form.is_valid() and seo_form.is_valid():
            film_form.save()
            seo_form.save()
            return redirect('films')

    film_form = my_forms.FilmForm(instance=film)
    film_form.fields['banner'].src = film.banner
    seo_obj = SeoBlock.objects.get(id=film.seo_block.id)
    seo_form = my_forms.SeoBlockForm(instance=seo_obj)
    data = {'form': film_form, 'film_name': film.name, 'seo_form': seo_form}
    return render(request, 'admin_panel/film_update.html', context=data)


def update_hall(request, number):
    hall = Hall.objects.get(number=number)
    if request.method == 'POST':

        hall_form = my_forms.HallForm(request.POST, request.FILES, instance=hall)
        seo_obj = SeoBlock.objects.get(id=hall.seo_block.id)
        seo_form = my_forms.SeoBlockForm(request.POST, instance=seo_obj)
        if hall_form.is_valid() and seo_form.is_valid():
            hall_form.save()
            seo_form.save()
            return redirect('cinemas')

    hall_form = my_forms.HallForm(instance=hall)
    seo_obj = SeoBlock.objects.get(id=hall.seo_block.id)
    seo_form = my_forms.SeoBlockForm(instance=seo_obj)
    data = {'hall_form': hall_form, 'hall_number': hall.number, 'seo_form': seo_form}
    return render(request, 'admin_panel/hall_update2.html', context=data)


def delete_hall(request, number):
    hall = Hall.objects.get(number=number)
    seo_block = SeoBlock.objects.get(id=hall.seo_block.id)
    seo_block.delete()
    hall.delete()

    return redirect('cinemas')


def update_main_page(request):
    main_page_obj = MainPage.objects.first()

    if request.method == 'POST':
        main_page_form = my_forms.MainPageForm(request.POST, instance=main_page_obj)
        seo_obj = SeoBlock.objects.get(id=main_page_obj.seo_block.id)
        seo_form = my_forms.SeoBlockForm(request.POST, instance=seo_obj)
        if main_page_form.is_valid() and seo_form.is_valid():
            main_page_form.save()
            seo_form.save()
            return redirect('pages')
    main_page_form = my_forms.MainPageForm(instance=main_page_obj)
    seo_obj = SeoBlock.objects.get(id=main_page_obj.seo_block.id)
    seo_form = my_forms.SeoBlockForm(instance=seo_obj)
    data = {'main_page_form': main_page_form, 'seo_form': seo_form}
    return render(request, 'admin_panel/main_page.html', context=data)


def update_contacts(request):
    contactFormset = modelformset_factory(can_delete=True, model=Contact, form=my_forms.ContactForm, extra=1)
    if request.method == 'POST':
        contacts_formset = contactFormset(request.POST, request.FILES)
        if contacts_formset.is_valid():
            contacts_formset.save()
            redirect("pages")
    contacts_formset = contactFormset(queryset=Contact.objects.all())
    data = {'contacts_formset': contacts_formset}
    return render(request, 'admin_panel/update_contacts.html', context=data)
