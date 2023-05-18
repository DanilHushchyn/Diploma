from django.urls import path

import kino_app.views

urlpatterns = [
    path("base", kino_app.views.base, name='base'),


    path("", kino_app.views.main, name='main'),
    path("profile", kino_app.views.profile, name='profile'),

    path("cinemas", kino_app.views.cinemas, name='kino_app_cinemas'),
    path("soon", kino_app.views.Soon.as_view(), name='soon'),
    path("schedule", kino_app.views.schedule, name='schedule'),
    path("schedule_for_film/<int:id>", kino_app.views.schedule_for_film, name='schedule_for_film'),
    path("card_cinema/<str:name>", kino_app.views.card_cinema, name='card_cinema'),
    path("film_card/<int:id>", kino_app.views.film_card, name='film_card'),

    path("seance/<int:pk>", kino_app.views.SeanceDetail.as_view(), name='seance'),
    path("booking", kino_app.views.booking, name='booking'),
    path("get-booked-tickets/<int:seance_id>", kino_app.views.getBookedTickets, name='get-booked-tickets'),

    path("hall/<int:id>", kino_app.views.hall, name='hall'),
    path("mobile_apps", kino_app.views.mobile_apps, name='mobile_apps'),
    path("about_cinema", kino_app.views.aboutCinema, name='about_cinema'),
    path("contacts", kino_app.views.contacts, name='contacts'),

    path("news", kino_app.views.news, name='news'),
    path("page_news/<int:id>", kino_app.views.page_news, name='page_news'),

    path("stocks", kino_app.views.stocks, name='stocks'),
    path("page_stock/<int:id>", kino_app.views.page_stock, name='page_stock'),

    path("poster", kino_app.views.Poster.as_view(), name='poster'),
    path("poster_soon_ajax", kino_app.views.posterSoonAjax, name='poster_soon_ajax'),
    path("search", kino_app.views.search, name='search'),
    path("page/<int:page_id>", kino_app.views.page, name='page'),
    path("cabinet", kino_app.views.cabinet, name='cabinet'),


]
