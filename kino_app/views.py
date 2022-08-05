import datetime

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from admin_panel.models.film import *
from admin_panel.models.cinema import *
from admin_panel.models.main_page import *
from datetime import date, timedelta


def getBanner():
    return BackImg.objects.first()


# Create your views here.
def page(request, page_id):
    page = Page.objects.get(pk=page_id)
    page_imgs = PageImg.objects.filter(page_id=page_id)

    data = {"page": page, 'page_imgs': page_imgs}
    if page.name == "Кафе-Бар":
        data['menu'] = CafeBarMenu.objects.all()
        return render(request, '../templates/kino_app/cafe_bar_page.html', context=data)
    return render(request, '../templates/kino_app/page.html', context=data)


# def main(request):
#     mainPage = MainPage.objects.last()
#     tops = TopCarousel.objects.all()
#     banners = BackImg.objects.all()
#     news_sales = BottomCarousel.objects.all()
#     banners_sliders = {"banner": banners, "tops": tops, "news_sales": news_sales}
#     date = datetime.datetime.today().date()
#     seances = Seance.objects.filter(date=date)
#     seances = seances.distinct("film")
#     pages=Page.objects.all()
#
#     data = {'mainPage': mainPage, 'seances': seances, 'banners_sliders': banners_sliders, 'pages': pages,
#             "date": date}
#     return render(request, '../templates/kino_app/main.html', context=data)
def main(request):
    top_carousel = TopCarousel.objects.all()
    bottom_carousel = BottomCarousel.objects.all()
    banners_sliders = {"top_carousel": top_carousel, "bottom_carousel": bottom_carousel}
    today_date = date.today()
    seances_today = Seance.objects.filter(date=today_date)
    seances_today = seances_today.distinct("film")

    unreleased_films = Film.objects.filter(released__gt=today_date)
    data = {'seances_today': seances_today, 'unreleased_films': unreleased_films, 'banners_sliders': banners_sliders,
            "today_date": today_date.today(), "banner": getBanner()}
    return render(request, '../templates/kino_app/main2.html', context=data)


def poster(request):
    today_date = date.today()
    unreleased_films = Film.objects.filter(released__gte=today_date)
    released_films = Film.objects.filter(released__lte=today_date)
    # films = Film.objects.all()
    # result = []
    # for film in films:
    #     result.append((film, (film.technology_types.all())))
    data = {
        'unreleased_films': unreleased_films,
        'released_films': released_films,
        "banner": getBanner(),
    }
    return render(request, '../templates/kino_app/poster2.html', context=data)


def cinemas(request):
    cinemas = Cinema.objects.all()
    data = {
        "cinemas": cinemas,
        "banner": getBanner(),
    }
    return render(request, '../templates/kino_app/cinemas2.html', context=data)


def soon(request):
    today_date = date.today()
    unreleased_films = Film.objects.filter(released__gte=today_date)
    released_films = Film.objects.filter(released__lte=today_date)
    # films = Film.objects.all()
    # result = []
    # for film in films:
    #     result.append((film, (film.technology_types.all())))
    data = {
        'unreleased_films': unreleased_films,
        'released_films': released_films,
        "banner": getBanner(),
    }
    return render(request, '../templates/kino_app/soon2.html', context=data)


# def func7(request):
#     films = Film.objects.filter(released=True)
#     seances = Seance.objects.all()
#     date_filter = request.GET.get('date_filter')
#     halls_filter = request.GET.getlist('halls_filter')
#     films_filter = request.GET.getlist('films_filter')
#     if date_filter:
#         new_date = datetime.datetime.strptime(date_filter, '%Y-%m-%d').strftime('%Y-%m-%d')
#         seances = seances.filter(date=new_date)
#     if halls_filter:
#         seances = seances.filter(hall__number__in=halls_filter)
#     if films_filter:
#         films = films.filter(id__in=films_filter)
#
#     result = []
#     for film in films:
#         film_seances = seances.filter(film_id=film.id)
#         date_film = []
#
#         for date_seance in film_seances.distinct('date'):
#             date_seances = film_seances.filter(date=date_seance.date)
#             hall_film = []
#
#             for hall_seance in date_seances.distinct('hall'):
#                 hall_seances = date_seances.filter(hall=hall_seance.hall)
#                 tech_film = []
#
#                 for tech_seance in hall_seances.distinct('tech_type'):
#                     tech_seances = hall_seances.filter(tech_type=tech_seance.tech_type)
#                     tech_film.append((tech_seance.tech_type.name, tech_seances))
#
#                 hall_film.append((hall_seance.hall.number, tech_film))
#
#             date_film.append((date_seance.date, hall_film))
#         result.append((film, date_film))
#
#     halls_filter = Hall.objects.order_by('number')
#     tech_types = TechnologyType.objects.order_by('name')
#     films_filter = Film.objects.filter(released=True).order_by('name')
#     data = {"result": result, 'halls_filter': halls_filter, 'films_filter': films_filter, "tech_types": tech_types}
#     return render(request, '../templates/kino_app/schedule.html', context=data)


def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'


def schedule(request):
    template = '../templates/kino_app/schedule2.html'
    seances = Seance.objects.all()
    if is_ajax(request):
        template = '../templates/kino_app/schedule_items.html'
        date_filter = request.GET.get('period')
        halls_filter = request.GET.getlist('halls_filter')
        films_filter = request.GET.getlist('films_filter')
        techs_filter = request.GET.getlist('techs_filter')
        if date_filter:
            if date_filter == 'tomorrow':
                seances = seances.filter(date=date.today() + timedelta(days=1))
            if date_filter == 'week':
                seances = seances.filter(date__lte=date.today() + timedelta(days=7), date__gte=date.today())
            if date_filter == 'today':
                seances = seances.filter(date=date.today())
            if date_filter == 'months':
                seances = seances.filter(date=date.today().month)

        if halls_filter:
            seances = seances.filter(hall__number__in=halls_filter)
        if films_filter:
            seances = seances.filter(film_id__in=films_filter)
        if techs_filter:
            seances = seances.filter(tech_type__name__in=techs_filter)

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

                hall_film.append((hall_seance.hall.number, tech_film))

            date_film.append((date_seance.date, hall_film))
        result.append((film_seance.film, date_film))

    film_list = []
    for film in Film.objects.order_by('name'):
        film_list.append(('unchecked', film))
    tech_list = []
    for tech in TechnologyType.objects.order_by('name'):
        tech_list.append(('unchecked', tech))

    hall_list = []
    for hall in Hall.objects.order_by('number'):
        hall_list.append(('unchecked', hall))

    data = {

        "result": result,
        "banner": getBanner(),
        'hall_list': hall_list,
        'film_list': film_list,
        "tech_list": tech_list,
    }
    return render(request, template, context=data)



def card_cinema(request, name):
    cinema = Cinema.objects.get(name=name)
    cinema_imgs = CinemaImg.objects.filter(cinema_id=cinema.id)
    halls = Hall.objects.filter(cinema_id=cinema.id)
    seances = Seance.objects.filter(date=date.today())

    data = {
        'cinema': cinema, "cinema_imgs": cinema_imgs,
        "halls": halls, "halls_num": halls.__len__(),
        'seances': seances,
        'banner': getBanner(),
    }
    return render(request, '../templates/kino_app/cinema_card2.html', context=data)


def film_card(request, name):
    seances = Seance.objects.filter(film__name=name)
    date_filter = request.GET.get('date_filter')
    halls_filter = request.GET.getlist('halls_filter')
    techs_filter = request.GET.getlist('techs_filter')
    if date_filter:
        new_date = datetime.datetime.strptime(date_filter, '%Y-%m-%d').strftime('%Y-%m-%d')
        seances = seances.filter(date=new_date)
    if halls_filter:
        seances = seances.filter(hall__number__in=halls_filter)
    if techs_filter:
        seances = seances.filter(tech_type__name__in=techs_filter)

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

                hall_film.append((hall_seance.hall.number, tech_film))

            date_film.append((date_seance.date, hall_film))
        result.append((film_seance.film, date_film))

    halls_filter = Hall.objects.order_by('number')
    tech_types = TechnologyType.objects.order_by('name')

    film = Film.objects.get(name=name)
    scriptwriter = film.scriptwriter.all()
    editor = film.editor.all()
    producer = film.producer.all()
    operator = film.operator.all()
    country = film.country.all()
    genres = film.genre.all()
    film_imgs = FilmImg.objects.filter(film=film)

    data = {
        "result": result,
        'halls_filter': halls_filter,
        "tech_types": tech_types,
        'film': film,
        'genres': genres,
        'scriptwriter': scriptwriter,
        'editor': editor,
        'producer': producer,
        'operator': operator,
        'film_imgs': film_imgs,
        'country': country,
        'title': film.name}
    return render(request, '../templates/kino_app/film_card.html', context=data)


def hall(request, id):
    hall = Hall.objects.get(pk=id)
    hall_imgs = HallImg.objects.filter(hall_id=hall.id)
    seances = Seance.objects.filter(hall=hall, date=date.today())
    data = {
        'hall': hall,
        'hall_imgs': hall_imgs,
        'banner': getBanner(),
        'seances': seances
    }

    return render(request, '../templates/kino_app/hall2.html', context=data)


def bar(request):
    return render(request, '../templates/kino_app/bar.html')


def vip_hall(request):
    return render(request, '../templates/kino_app/vip_hall.html')


def kids_room(request):
    return render(request, '../templates/kino_app/kids_room.html')


def ads(request):
    return render(request, '../templates/kino_app/ads.html')


def mobile_apps(request):
    return render(request, '../templates/kino_app/mobile_apps.html')


def contacts(request):
    contact = Contact.objects.all()
    data = {'contacts': contact}
    return render(request, '../templates/kino_app/contacts.html', context=data)


def news(request):
    news = News.objects.filter(turn_on=True).order_by('creation_date')
    paginator = Paginator(news, 3)

    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)

    data = {'news_list': page.object_list, 'page': page, }
    return render(request, '../templates/kino_app/news.html', context=data)


def stocks(request):
    stocks = Stock.objects.filter(turn_on=True).order_by('creation_date')
    paginator = Paginator(stocks, 3)

    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)

    data = {'stocks': page.object_list, 'page': page, }
    return render(request, '../templates/kino_app/stocks.html', context=data)


def page_stock(request):
    return render(request, '../templates/kino_app/page_stock.html')


def page_news(request):
    return render(request, '../templates/kino_app/page_news.html')


def search(request):
    film_name = request.GET['search_film']
    film = Film.objects.get(name=film_name)
    return film_card(request, film.name)
