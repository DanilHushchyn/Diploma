import json

from celery.result import AsyncResult
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin.widgets import AdminFileWidget
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, DeleteView

from admin_panel import forms as my_forms
from admin_panel.tasks import send_email
from kino_app.views import is_ajax
from user import forms as user_forms
from django.forms import inlineformset_factory, modelformset_factory
# Create your views here.
from admin_panel.models import *
from datetime import date, timedelta
from django.db import connections

connections.close_all()

@login_required
@staff_member_required
def statistic(request):
    connections.close_all()
    mans_woman = [Account.objects.filter(sex='Мужской').count(), Account.objects.filter(sex='Женский').count()]

    tickets = Ticket.objects.all()
    films = Film.objects.all()
    top_films = []
    popular_films = []
    for film in films:
        top_films.append([tickets.filter(seance__film=film).count(), f'{film.name}'])
        popular_films.append([tickets.filter(seance__film=film).count(), film.id])
    top_films = (sorted(top_films)[-1:-4:-1])

    film_seances = []
    for count, film_id in sorted(popular_films)[-1:-6:-1]:
        seances_list = []
        for i in range(7):
            seances_list.append(Seance.objects.filter(film=film_id, date=(date.today() + timedelta(days=i))).count())

        film_seances.append([Film.objects.get(id=film_id), seances_list])

    seances_for_week = []
    week = []
    for i in range(7):
        seances_for_week.append(Seance.objects.filter(date=date.today() + timedelta(days=i)).count())
        week.append(date.today() + timedelta(days=i))

    data = {
        'users_count': Account.objects.count(),
        'mans_woman': mans_woman,
        'top_films': top_films,
        'seances_for_week': seances_for_week,
        'week': week,
        'film_seances': film_seances,
    }
    return render(request, 'admin_panel/statistic.html', context=data)


@login_required
@staff_member_required
def clients(request):
    data = {'users': Account.objects.all()}
    return render(request, 'admin_panel/clients.html', context=data)


@login_required
@staff_member_required
def update_client(request, id):
    client = Account.objects.get(id=id)
    if request.method == 'POST':
        client_form = user_forms.AdminUserForm(request.POST, instance=client)
        if client_form.is_valid():
            client_form.save()
            return redirect('clients')
        else:
            data = {'client_form': client_form, 'client_id': id}
            return render(request, 'admin_panel/update_client.html', context=data)
    client_form = user_forms.AdminUserForm(instance=client, )
    data = {'client_form': client_form, 'client_id': id}
    return render(request, 'admin_panel/update_client.html', context=data)


@login_required
@staff_member_required
def delete_client(request, id):
    return render(request, 'admin_panel/clients.html', )


@login_required
@staff_member_required
def films(request):
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
    if request.method == 'POST':
        FilmFormsetFactory = modelformset_factory(can_delete=True, model=FilmImg, form=my_forms.FilmImgForm,
                                                  extra=0)
        film_gallery = FilmFormsetFactory(request.POST, request.FILES)
        film_form = my_forms.FilmForm(request.POST, request.FILES)
        seo_block = my_forms.SeoBlockForm(request.POST)

        if seo_block.is_valid() and film_form.is_valid() and film_gallery.is_valid():
            seo_obj = seo_block.save()
            film_obj = film_form.save()
            film_obj.seo_block_id = seo_obj.id
            film_obj.save()
            instances = film_gallery.save(commit=False)
            for instance in instances:
                instance.film_id = film_obj.id
                instance.save()
        else:
            data = {
                'seo_form': seo_block,
                'form': film_form,
                'film_gallery': film_gallery,
            }
            return render(request, 'admin_panel/film_form.html', context=data)

    return render(request, 'admin_panel/films2.html', context=data)


@login_required
@staff_member_required
def cinemas(request):
    if request.method == "POST":
        hall_form = my_forms.HallForm(request.POST, request.FILES)
        seo_form = my_forms.SeoBlockForm(request.POST)

        HallFormsetFactory = modelformset_factory(can_delete=True, model=HallImg, form=my_forms.HallImgForm,
                                                  extra=0)
        hall_gallery = HallFormsetFactory(request.POST, request.FILES)
        if seo_form.is_valid() and hall_form.is_valid() and hall_gallery.is_valid():
            seo_obj = seo_form.save()
            hall_obj = hall_form.save()
            hall_obj.seo_block_id = seo_obj.id
            hall_obj.cinema_id = 1
            hall_obj.save()
            instances = hall_gallery.save(commit=False)
            for instance in instances:
                instance.hall_id = hall_obj.id
                instance.save()
        else:
            data = {'hall_form': hall_form, 'hall_gallery': hall_gallery, 'seo_form': seo_form}
            return render(request, 'admin_panel/hall_form.html', context=data)

    cinemas = Cinema.objects.all()
    data = {'cinemas': cinemas}
    return render(request, 'admin_panel/cinemas.html', context=data)


@login_required
@staff_member_required
def choose_client(request):
    users = Account.objects.all()
    data = {
        'users': users
    }
    return render(request, 'admin_panel/choose_client.html', context=data)


@login_required
@staff_member_required
def mailing(request):
    clients_filter = request.GET.getlist('clients_filter')
    if clients_filter:
        users = Account.objects.filter(id__in=clients_filter)
    else:
        users = Account.objects.all()

    if request.method == 'POST':
        templates_filter = request.POST.getlist('templates_filter')
        if templates_filter:
            obj = TemplateHtml.objects.get(id__in=templates_filter)
        else:
            form = my_forms.TemplateHtmlForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save()
            else:
                templates_html = TemplateHtml.objects.all()[:5]
                data = {
                    'file_form': form,
                    'templates_html': templates_html,
                }
                return render(request, 'admin_panel/mailing.html', context=data)
        import urllib.request
        html_content = urllib.request.urlopen(f'{obj.template_html.url}').read()
        html_content = html_content.decode()
        to = []
        for i in users:
            to.append(i.email)

        task = send_email.delay(html_content, to)
        total_time = len(to)
        data = {
            'task_id': task.id,
            'total_time': total_time
        }
        return render(request, 'admin_panel/mailing.html', context=data)

    templates_html = TemplateHtml.objects.all()[:5]
    file_form = my_forms.TemplateHtmlForm()
    data = {
        'file_form': file_form,
        'templates_html': templates_html,
    }
    return render(request, 'admin_panel/mailing.html', context=data)


@login_required
@staff_member_required
def get_task_info(request):
    task_id = request.GET.get('task_id', None)
    if task_id is not None:
        task = AsyncResult(task_id)
        data = {
            'state': task.state,
            'result': task.result,
        }
        # data = task.state or task.result

        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponse('No job id given.')


@login_required
@staff_member_required
def deleteHtmlTemplate(request, id):
    templates_html = TemplateHtml.objects.get(id=id)
    templates_html.delete()
    return redirect('mailing')


@login_required
@staff_member_required
def stocks(request):
    if request.method == "POST":
        stock_form = my_forms.StockForm(request.POST, request.FILES)
        seo_form = my_forms.SeoBlockForm(request.POST)
        StockFormsetFactory = modelformset_factory(can_delete=True, extra=0, model=StockImg, form=my_forms.StockImgForm)
        stock_gallery = StockFormsetFactory(request.POST, request.FILES)
        if seo_form.is_valid() and stock_form.is_valid() and stock_gallery.is_valid():
            seo_obj = seo_form.save()
            stock_obj = stock_form.save()
            stock_obj.seo_block_id = seo_obj.id
            stock_obj.save()
            instances = stock_gallery.save(commit=False)
            for instance in instances:
                instance.stock_id = stock_obj.id
                instance.save()

        else:
            data = {'stock_form': stock_form, 'stock_gallery': stock_gallery, 'seo_form': seo_form}
            return render(request, 'admin_panel/stock_form.html', context=data)

    stocks = Stock.objects.all()
    data = {'stocks': stocks}
    return render(request, 'admin_panel/stocks2.html', context=data)


@login_required
@staff_member_required
def get_stock_form(request):
    StockFormsetFactory = modelformset_factory(can_delete=True, model=StockImg, form=my_forms.StockImgForm, extra=0)
    stock_gallery = StockFormsetFactory(queryset=StockImg.objects.none())
    # stockImgs_form = my_forms.StockImgForm()
    stock_form = my_forms.StockForm()
    seo_form = my_forms.SeoBlockForm()

    data = {'stock_form': stock_form, 'stock_gallery': stock_gallery, 'seo_form': seo_form}
    return render(request, 'admin_panel/stock_form.html', context=data)


@login_required
@staff_member_required
def update_stock(request, id):
    stock = Stock.objects.get(id=id)
    StockFormsetFactory = modelformset_factory(can_delete=True, model=StockImg, form=my_forms.StockImgForm,
                                               extra=0)
    if request.method == 'POST':
        stock_gallery = StockFormsetFactory(request.POST, request.FILES)
        stock_form = my_forms.StockForm(request.POST, request.FILES, instance=stock)
        seo_obj = SeoBlock.objects.get(id=stock.seo_block.id)
        seo_form = my_forms.SeoBlockForm(request.POST, instance=seo_obj)
        if stock_form.is_valid() and seo_form.is_valid() and stock_gallery.is_valid():
            stock_obj = stock_form.save()
            seo_form.save()
            instances = stock_gallery.save(commit=False)
            for object in stock_gallery.deleted_objects:
                object.delete()
            for instance in instances:
                instance.stock_id = stock_obj.id
                instance.save()
            return redirect('stocks_table')
        else:

            data = {'stock_form': stock_form, 'stock_id': stock.id, 'seo_form': seo_form,
                    'stock_gallery': stock_gallery}
            return render(request, 'admin_panel/stock_update2.html', context=data)

    stock_gallery = StockFormsetFactory(queryset=StockImg.objects.filter(stock_id=stock.id))

    stock_form = my_forms.StockForm(instance=stock)
    seo_obj = SeoBlock.objects.get(id=stock.seo_block.id)
    seo_form = my_forms.SeoBlockForm(instance=seo_obj)
    data = {'stock_form': stock_form, 'stock_id': stock.id, 'seo_form': seo_form, 'stock_gallery': stock_gallery}
    return render(request, 'admin_panel/stock_update2.html', context=data)


@login_required
@staff_member_required
def delete_stock(request, id):
    stock = Stock.objects.get(id=id)
    seo_block = SeoBlock.objects.get(id=stock.seo_block.id)
    seo_block.delete()
    stock.delete()

    return redirect('stocks_table')


@login_required
@staff_member_required
def news(request):
    if request.method == "POST":
        news_form = my_forms.NewsForm(request.POST, request.FILES)
        seo_form = my_forms.SeoBlockForm(request.POST)
        NewsFormsetFactory = modelformset_factory(can_delete=True, model=NewsImg, form=my_forms.NewsImgForm,
                                                  extra=0)
        news_gallery = NewsFormsetFactory(request.POST, request.FILES)
        if seo_form.is_valid() and news_form.is_valid() and news_gallery.is_valid():
            seo_obj = seo_form.save()
            news_obj = news_form.save()
            news_obj.seo_block_id = seo_obj.id
            news_obj.save()
            instances = news_gallery.save(commit=False)
            for instance in instances:
                instance.news_id = news_obj.id
                instance.save()
        else:
            data = {'news_form': news_form, 'news_gallery': news_gallery, 'seo_form': seo_form}
            return render(request, 'admin_panel/news_form.html', context=data)

    news_list = News.objects.all()
    data = {'news_list': news_list}
    return render(request, 'admin_panel/news2.html', context=data)


@login_required
@staff_member_required
def get_news_form(request):
    NewsFormsetFactory = modelformset_factory(can_delete=True, model=NewsImg, form=my_forms.NewsImgForm, extra=0)
    news_gallery = NewsFormsetFactory(queryset=NewsImg.objects.none())
    # newsImgs_form = my_forms.NewsImgForm()
    news_form = my_forms.NewsForm()
    seo_form = my_forms.SeoBlockForm()

    data = {'news_form': news_form, 'news_gallery': news_gallery, 'seo_form': seo_form}
    return render(request, 'admin_panel/news_form.html', context=data)


@login_required
@staff_member_required
def update_news(request, id):
    PageFormsetFactory = modelformset_factory(can_delete=True, model=NewsImg, form=my_forms.NewsImgForm,
                                              extra=0)
    news = News.objects.get(id=id)
    if request.method == 'POST':
        news_gallery = PageFormsetFactory(request.POST, request.FILES)
        news_form = my_forms.NewsForm(request.POST, request.FILES, instance=news)
        seo_obj = SeoBlock.objects.get(id=news.seo_block.id)
        seo_form = my_forms.SeoBlockForm(request.POST, instance=seo_obj)
        if news_form.is_valid() and seo_form.is_valid() and news_gallery.is_valid():
            news_obj = news_form.save()
            seo_form.save()
            instances = news_gallery.save(commit=False)
            for object in news_gallery.deleted_objects:
                object.delete()
            for instance in instances:
                instance.news_id = news_obj.id
                instance.save()
            return redirect('news_table')
        data = {'news_form': news_form, 'news_id': news.id, 'seo_form': seo_form, 'news_gallery': news_gallery}
        return render(request, 'admin_panel/news_update2.html', context=data)

    news_gallery = PageFormsetFactory(queryset=NewsImg.objects.filter(news_id=news.id))

    news_form = my_forms.NewsForm(instance=news)
    seo_obj = SeoBlock.objects.get(id=news.seo_block.id)
    seo_form = my_forms.SeoBlockForm(instance=seo_obj)
    data = {'news_form': news_form, 'news_id': news.id, 'seo_form': seo_form, 'news_gallery': news_gallery}
    return render(request, 'admin_panel/news_update2.html', context=data)


@login_required
@staff_member_required
def delete_news(request, id):
    news = News.objects.get(id=id)
    seo_block = SeoBlock.objects.get(id=news.seo_block.id)
    seo_block.delete()
    news.delete()

    return redirect('news_table')


# def get_film_form(request):
#     filmImgForm = my_forms.FilmImgForm()
#
#     film_form = my_forms.FilmForm()
#     seo = my_forms.SeoBlockForm()
#     data = {'form': film_form, 'filmImg_form': filmImgForm, 'seo_form': seo}
#     return render(request, 'admin_panel/film_form.html', context=data)

@method_decorator([login_required, staff_member_required], name='dispatch')
class FilmForm(FormView):
    initial = {'name': 'Film name'}
    template_name = 'admin_panel/film_form.html'
    form_class = my_forms.FilmForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seo = my_forms.SeoBlockForm()
        context['seo_form'] = seo
        # filmImgForm = my_forms.FilmImgForm()
        FilmFormsetFactory = modelformset_factory(can_delete=True, model=FilmImg, form=my_forms.FilmImgForm, extra=0)
        film_gallery = FilmFormsetFactory(queryset=FilmImg.objects.none())
        context['film_gallery'] = film_gallery
        return context

    def get_success_url(self):
        return redirect('films')


@login_required
@staff_member_required
def cinema_card(request, id):
    cinema = Cinema.objects.get(id=id)
    CinemaFormsetFactory = modelformset_factory(can_delete=True, model=CinemaImg, form=my_forms.CinemaImgForm,
                                                extra=0)
    if request.method == 'POST':

        cinema_gallery = CinemaFormsetFactory(request.POST, request.FILES)
        cinema_form = my_forms.CinemaForm(request.POST, request.FILES, instance=cinema)
        seo_obj = SeoBlock.objects.get(id=cinema.seo_block.id)
        seo_form = my_forms.SeoBlockForm(request.POST, instance=seo_obj)
        if cinema_form.is_valid() and seo_form.is_valid() and cinema_gallery.is_valid():
            seo_form.save()
            cinema_form.save()
            instances = cinema_gallery.save(commit=False)
            for object in cinema_gallery.deleted_objects:
                object.delete()
            for instance in instances:
                instance.cinema_id = cinema.id
                instance.save()
            return redirect('admin_cinemas')
        else:
            halls = Hall.objects.filter(cinema_id=cinema.id)
            data = {'form': cinema_form, 'seo_form': seo_form, 'halls': halls,
                    'cinema_gallery': cinema_gallery}
            return render(request, 'admin_panel/cinema_update.html', context=data)

    cinema_form = my_forms.CinemaForm(instance=cinema)
    cinema_gallery = CinemaFormsetFactory(queryset=CinemaImg.objects.filter(cinema_id=1))

    seo_obj = SeoBlock.objects.get(id=cinema.seo_block.id)
    seo_form = my_forms.SeoBlockForm(instance=seo_obj)
    halls = Hall.objects.filter(cinema_id=cinema.id)
    data = {'form': cinema_form, 'cinema_name': cinema.name, 'seo_form': seo_form, 'halls': halls,
            'cinema_gallery': cinema_gallery}
    return render(request, 'admin_panel/cinema_update.html', context=data)


@login_required
@staff_member_required
def get_hall_form(request):
    # hallImgs_form = my_forms.HallImgForm()
    HallFormsetFactory = modelformset_factory(can_delete=True, model=HallImg, form=my_forms.HallImgForm, extra=0)
    hall_gallery = HallFormsetFactory(queryset=HallImg.objects.none())

    hall_form = my_forms.HallForm()
    seo_form = my_forms.SeoBlockForm()

    data = {'hall_form': hall_form, 'hall_gallery': hall_gallery, 'seo_form': seo_form}
    return render(request, 'admin_panel/hall_form.html', context=data)


@login_required
@staff_member_required
def banners_sliders(request):
    TopCarouselFormset = modelformset_factory(TopCarousel, form=my_forms.TopCarouselForm, extra=0, can_delete=True)
    top_carousel_formset = TopCarouselFormset(queryset=TopCarousel.objects.all(), prefix='top_carousel')

    BottomCarouselFormset = modelformset_factory(BottomCarousel, form=my_forms.BottomCarouselForm, extra=0,
                                                 can_delete=True)
    bottom_carousel_formset = BottomCarouselFormset(queryset=BottomCarousel.objects.all(), prefix='bottom_carousel')

    interval = my_forms.FormInterval()

    back_img_form = my_forms.BackImgForm(instance=BackImg.objects.first())
    data = {

        'top_carousel_formset': top_carousel_formset,
        'bottom_carousel_formset': bottom_carousel_formset,
        'back_img_form': back_img_form,
        'interval': interval,
    }
    return render(request, 'admin_panel/banners_sliders2.html', context=data)


@login_required
@staff_member_required
def top_carousel(request):
    TopCarouselFormSet = modelformset_factory(TopCarousel, form=my_forms.TopCarouselForm, extra=0, can_delete=True)
    top_carousel_formset = TopCarouselFormSet(request.POST, request.FILES, prefix='top_carousel')

    BottomCarouselFormset = modelformset_factory(BottomCarousel, form=my_forms.BottomCarouselForm, extra=0,
                                                 can_delete=True)
    bottom_carousel_formset = BottomCarouselFormset(queryset=BottomCarousel.objects.all(), prefix='bottom_carousel')

    interval = my_forms.FormInterval(request.POST)

    back_img_form = my_forms.BackImgForm(instance=BackImg.objects.first())
    if top_carousel_formset.is_valid() and interval.is_valid():
        TopCarousel.interval = interval.cleaned_data['interval']
        top_carousel_formset.save()
    else:
        data = {
            'top_carousel_formset': top_carousel_formset,
            'bottom_carousel_formset': bottom_carousel_formset,
            'back_img_form': back_img_form,
            'interval': interval,
        }
        return render(request, 'admin_panel/banners_sliders2.html', context=data)

    return redirect('banners_sliders')


@login_required
@staff_member_required
def bottom_carousel(request):
    BottomCarouselFormSet = modelformset_factory(BottomCarousel, form=my_forms.BottomCarouselForm, extra=0,
                                                 can_delete=True)
    bottom_carousel_formset = BottomCarouselFormSet(request.POST, request.FILES, prefix='bottom_carousel')

    TopCarouselFormset = modelformset_factory(TopCarousel, form=my_forms.TopCarouselForm, extra=0, can_delete=True)
    top_carousel_formset = TopCarouselFormset(queryset=TopCarousel.objects.all(), prefix='top_carousel')

    interval = my_forms.FormInterval(request.POST)
    back_img_form = my_forms.BackImgForm(instance=BackImg.objects.first())

    if bottom_carousel_formset.is_valid() and interval.is_valid():
        BottomCarousel.interval = interval.cleaned_data['interval']
        bottom_carousel_formset.save()

    else:
        data = {
            'top_carousel_formset': top_carousel_formset,
            'bottom_carousel_formset': bottom_carousel_formset,
            'back_img_form': back_img_form,
            'interval': interval,
        }
        return render(request, 'admin_panel/banners_sliders2.html', context=data)

    return redirect('banners_sliders')


@login_required
@staff_member_required
def back_img(request):
    back_img_form = my_forms.BackImgForm(request.POST, request.FILES)
    if back_img_form.is_valid():
        BackImg.objects.all().delete()
        back_img_form.save()

    return redirect('banners_sliders')


@login_required
@staff_member_required
def pages(request):
    if request.method == "POST":
        page_form = my_forms.PageForm(request.POST, request.FILES)
        seo_form = my_forms.SeoBlockForm(request.POST)
        PageFormsetFactory = modelformset_factory(can_delete=True, model=PageImg, form=my_forms.PageImgForm, extra=0)
        page_gallery = PageFormsetFactory(request.POST, request.FILES)
        if seo_form.is_valid() and page_form.is_valid() and page_gallery.is_valid():
            seo_obj = seo_form.save()
            page_obj = page_form.save()
            page_obj.seo_block_id = seo_obj.id
            page_obj.save()
            instances = page_gallery.save(commit=False)
            for instance in instances:
                instance.page_id = page_obj.id
                instance.save()
        else:
            data = {'page_form': page_form, 'page_gallery': page_gallery, 'seo_form': seo_form}
            return render(request, 'admin_panel/page_form.html', context=data)

    page_list = Page.objects.order_by('creation_date')
    data = {'page_list': page_list}
    return render(request, 'admin_panel/pages2.html', context=data)


@login_required
@staff_member_required
def get_page_form(request):
    # pageImgs_form = my_forms.PageImgForm()
    PageFormsetFactory = modelformset_factory(can_delete=True, model=PageImg, form=my_forms.PageImgForm, extra=0)
    page_gallery = PageFormsetFactory(queryset=PageImg.objects.none())
    page_form = my_forms.PageForm()
    seo_form = my_forms.SeoBlockForm()

    data = {'page_form': page_form, 'page_gallery': page_gallery, 'seo_form': seo_form}
    return render(request, 'admin_panel/page_form.html', context=data)


@login_required
@staff_member_required
def update_page(request, id):
    menuFormset = modelformset_factory(can_delete=True, model=CafeBarMenu, form=my_forms.CafeBarMenuForm, extra=0)
    PageFormsetFactory = modelformset_factory(can_delete=True, model=PageImg, form=my_forms.PageImgForm,
                                              extra=0)
    page = Page.objects.get(id=id)

    if request.method == 'POST':
        if page.name == 'Кафе-Бар':
            menu_formset = menuFormset(request.POST, prefix="menu")
            page_gallery = PageFormsetFactory(request.POST, request.FILES)

            page_form = my_forms.PageUpdateForm(request.POST, request.FILES, instance=page)
            seo_obj = SeoBlock.objects.get(id=page.seo_block.id)
            seo_form = my_forms.SeoBlockForm(request.POST, instance=seo_obj)

            if menu_formset.is_valid() and page_form.is_valid() and seo_form.is_valid() and page_gallery.is_valid():
                menu_formset.save()
                page_obj = page_form.save()
                seo_form.save()
                instances = page_gallery.save(commit=False)
                for object in page_gallery.deleted_objects:
                    object.delete()
                for instance in instances:
                    instance.page_id = page_obj.id
                    instance.save()

                return redirect('pages')
            else:
                data = {
                    'page_form': page_form,
                    'page_gallery': page_gallery,
                    'page_id': page.id,
                    'seo_form': seo_form,
                    'menu_formset': menu_formset,
                    'labels': my_forms.CafeBarMenuForm
                }
                return render(request, 'admin_panel/update_cafe-bar.html', context=data)
        page_gallery = PageFormsetFactory(request.POST, request.FILES)

        page_form = my_forms.PageUpdateForm(request.POST, request.FILES, instance=page)
        seo_obj = SeoBlock.objects.get(id=page.seo_block.id)
        seo_form = my_forms.SeoBlockForm(request.POST, instance=seo_obj)
        if page_form.is_valid() and seo_form.is_valid() and page_gallery.is_valid():
            page_obj = page_form.save()
            seo_form.save()
            instances = page_gallery.save(commit=False)
            for object in page_gallery.deleted_objects:
                object.delete()
            for instance in instances:
                instance.page_id = page_obj.id
                instance.save()
            return redirect('pages')
        else:
            data = {'page_form': page_form, 'page_id': page.id, 'seo_form': seo_form,
                    'page_gallery': page_gallery, }
            return render(request, 'admin_panel/page_update2.html', context=data)

    page_form = my_forms.PageUpdateForm(instance=page)
    seo_obj = SeoBlock.objects.get(id=page.seo_block.id)
    seo_form = my_forms.SeoBlockForm(instance=seo_obj)
    page_gallery = PageFormsetFactory(queryset=PageImg.objects.filter(page_id=page.id))
    data = {'page_form': page_form, 'page_id': page.id, 'seo_form': seo_form, 'page_gallery': page_gallery}
    if page.name == 'Кафе-Бар':
        menu_formset = menuFormset(queryset=CafeBarMenu.objects.all(), prefix="menu")
        data['menu_formset'] = menu_formset
        data['labels'] = my_forms.CafeBarMenuForm
        return render(request, 'admin_panel/update_cafe-bar.html', context=data)
    return render(request, 'admin_panel/page_update2.html', context=data)


@login_required
@staff_member_required
def delete_page(request, id):
    page = Page.objects.get(id=id)
    seo_block = SeoBlock.objects.get(id=page.seo_block.id)
    seo_block.delete()
    page.delete()

    return redirect('pages')


@login_required
@staff_member_required
def update_film(request, id):
    film = Film.objects.get(id=id)
    FilmFormsetFactory = modelformset_factory(can_delete=True, model=FilmImg, form=my_forms.FilmImgForm,
                                              extra=0)
    if request.method == 'POST':
        film_gallery = FilmFormsetFactory(request.POST, request.FILES)

        film_form = my_forms.FilmForm(request.POST, request.FILES, instance=film)
        seo_obj = SeoBlock.objects.get(id=film.seo_block.id)
        seo_form = my_forms.SeoBlockForm(request.POST, instance=seo_obj)
        if film_form.is_valid() and seo_form.is_valid() and film_gallery.is_valid():
            seo_form.save()
            film_obj = film_form.save()
            instances = film_gallery.save(commit=False)
            for object in film_gallery.deleted_objects:
                object.delete()
            for instance in instances:
                instance.film_id = film_obj.id
                instance.save()
            return redirect('films')
        else:
            data = {'form': film_form, 'film_name': film.name, 'film_gallery': film_gallery, 'seo_form': seo_form}
            return render(request, 'admin_panel/film_update.html', context=data)

    film_form = my_forms.FilmForm(instance=film)

    film_gallery = FilmFormsetFactory(queryset=FilmImg.objects.filter(film_id=film.id))

    seo_obj = SeoBlock.objects.get(id=film.seo_block.id)
    seo_form = my_forms.SeoBlockForm(instance=seo_obj)
    data = {'form': film_form, 'film_name': film.name, 'film_gallery': film_gallery, 'seo_form': seo_form}
    return render(request, 'admin_panel/film_update.html', context=data)


@login_required
@staff_member_required
def update_hall(request, number):
    hall = Hall.objects.get(number=number)
    HallFormsetFactory = modelformset_factory(can_delete=True, model=HallImg, form=my_forms.HallImgForm,
                                              extra=0)
    if request.method == 'POST':
        hall_gallery = HallFormsetFactory(request.POST, request.FILES, )
        hall_form = my_forms.HallForm(request.POST, request.FILES, instance=hall)
        seo_obj = SeoBlock.objects.get(id=hall.seo_block.id)
        seo_form = my_forms.SeoBlockForm(request.POST, instance=seo_obj)
        if hall_form.is_valid() and seo_form.is_valid() and hall_gallery.is_valid():
            hall_obj = hall_form.save()
            seo_form.save()
            instances = hall_gallery.save(commit=False)
            for object in hall_gallery.deleted_objects:
                object.delete()
            for instance in instances:
                instance.hall_id = hall_obj.id
                instance.save()
            return redirect('admin_cinemas')
        else:
            data = {'hall_form': hall_form, 'hall_number': hall.number, 'seo_form': seo_form,
                    'hall_gallery': hall_gallery}
            return render(request, 'admin_panel/hall_update2.html', context=data)

    hall_gallery = HallFormsetFactory(queryset=HallImg.objects.filter(hall_id=hall.id))

    hall_form = my_forms.HallForm(instance=hall)
    seo_obj = SeoBlock.objects.get(id=hall.seo_block.id)
    seo_form = my_forms.SeoBlockForm(instance=seo_obj)
    data = {'hall_form': hall_form, 'hall_number': hall.number, 'seo_form': seo_form, 'hall_gallery': hall_gallery}
    return render(request, 'admin_panel/hall_update2.html', context=data)


@login_required
@staff_member_required
def delete_hall(request, number):
    hall = Hall.objects.get(number=number)
    seo_block = SeoBlock.objects.get(id=hall.seo_block.id)
    seo_block.delete()
    hall.delete()

    return redirect('admin_cinemas')


@login_required
@staff_member_required
def update_main_page(request):
    main_page_obj = MainPage.objects.first()

    if request.method == 'POST':

        main_page_form = my_forms.MainPageForm(request.POST, instance=main_page_obj)
        seo_obj = SeoBlock.objects.get(id=main_page_obj.seo_block.id)
        seo_form = my_forms.SeoBlockForm(request.POST, instance=seo_obj)
        if main_page_form.is_valid() and seo_form.is_valid():
            seo_form.save()
            main_page_form.save()
            return redirect('pages')
        else:
            data = {'main_page_form': main_page_form, 'seo_form': seo_form}
            return render(request, 'admin_panel/main_page.html', context=data)

    main_page_form = my_forms.MainPageForm(instance=main_page_obj)
    seo_obj = SeoBlock.objects.get(id=main_page_obj.seo_block.id)
    seo_form = my_forms.SeoBlockForm(instance=seo_obj)
    data = {'main_page_form': main_page_form, 'seo_form': seo_form}
    return render(request, 'admin_panel/main_page.html', context=data)


@login_required
@staff_member_required
def update_contacts(request):
    contactFormset = modelformset_factory(can_delete=True, model=Contact, form=my_forms.ContactForm, extra=0, )
    if request.method == 'POST':
        contacts_formset = contactFormset(request.POST, request.FILES)
        if contacts_formset.is_valid():
            contacts_formset.save()
            return redirect("pages")
        else:
            data = {'contacts_formset': contacts_formset}
            return render(request, 'admin_panel/update_contacts.html', context=data)
    contacts_formset = contactFormset(queryset=Contact.objects.all())
    data = {'contacts_formset': contacts_formset}
    return render(request, 'admin_panel/update_contacts.html', context=data)


@login_required
@staff_member_required
def seances(request):
    template = '../templates/admin_panel/seances.html'
    Seance.objects.filter(date__lt=date.today()).delete()
    seances = Seance.objects.all()

    if is_ajax(request):
        template = '../templates/admin_panel/seances_items.html'
        date_filter = request.GET.get('period')
        halls_filter = request.GET.getlist('halls_filter')
        films_filter = request.GET.getlist('films_filter')
        techs_filter = request.GET.getlist('techs_filter')
        if date_filter:
            seances = seances.filter(date=date_filter)
        if halls_filter:
            seances = seances.filter(hall__number__in=halls_filter)
        if films_filter:
            seances = seances.filter(film_id__in=films_filter)
        if techs_filter:
            seances = seances.filter(tech_type__id__in=techs_filter)

    result = []
    for film_seance in seances.distinct('film_id'):
        film_seances = seances.filter(film_id=film_seance.film_id)
        date_film = []

        for date_seance in film_seances.distinct('date'):
            date_seances = film_seances.filter(date=date_seance.date)
            hall_film = []

            for hall_seance in date_seances.distinct('hall'):
                hall_seances = date_seances.filter(hall=hall_seance.hall)
                tech_film = []

                for tech_seance in hall_seances.distinct('tech_type'):
                    tech_seances = hall_seances.filter(tech_type=tech_seance.tech_type)
                    tech_film.append((tech_seance.tech_type.name, tech_seances))

                hall_film.append((hall_seance.hall, tech_film))

            date_film.append((date_seance.date, hall_film))
        result.append((film_seance.film, date_film))

    film_list = []
    today_date = date.today()
    for film in Film.objects.filter(released__lt=today_date).order_by('name'):
        film_list.append(('unchecked', film))
    tech_list = []
    for tech in TechnologyType.objects.order_by('id'):
        tech_list.append(('unchecked', tech))

    hall_list = []
    for hall in Hall.objects.order_by('number'):
        hall_list.append(('unchecked', hall))

    data = {
        "result": result,
        'hall_list': hall_list,
        'film_list': film_list,
        "tech_list": tech_list,
    }
    return render(request, template, context=data)


@login_required
@staff_member_required
def get_seance_form(request):
    if request.method == 'POST':
        seance_form = my_forms.SeanceForm(request.POST)
        if seance_form.is_valid():
            seance_form.save()
            return redirect('seances')
        else:
            data = {'seance_form': seance_form, }
            return render(request, 'admin_panel/seance_form.html', context=data)

    seance_form = my_forms.SeanceForm()
    seance_form.fields['film'].queryset = Film.objects.filter(released__lt=date.today())
    seo_form = my_forms.SeoBlockForm()

    data = {'seance_form': seance_form, 'seo_form': seo_form}
    return render(request, 'admin_panel/seance_form.html', context=data)


@login_required
@staff_member_required
def delete_seance(request, id):
    tickets = Ticket.objects.filter(seance_id=id)
    for ticket in tickets:
        ticket.delete()
    Seance.objects.get(id=id).delete()
    return redirect('seances')
