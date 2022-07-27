from django.urls import path

import kino_app.views

urlpatterns = [
    path("main", kino_app.views.main, name='main'),
    path("cinemas", kino_app.views.cinemas, name='cinemas'),
    path("soon", kino_app.views.soon, name='soon'),
    path("schedule", kino_app.views.schedule, name='schedule'),
    path("card_cinema/<str:name>", kino_app.views.card_cinema, name='card_cinema'),
    path("film_card/<str:name>", kino_app.views.film_card, name='film_card'),
    path("hall/<int:id>", kino_app.views.hall, name='hall'),
    path("mobile_apps", kino_app.views.mobile_apps, name='mobile_apps'),
    path("contacts", kino_app.views.contacts, name='contacts'),
    path("news", kino_app.views.news, name='news'),
    path("stocks", kino_app.views.stocks, name='stocks'),
    path("page_stock", kino_app.views.page_stock, name='page_stock'),
    path("page_news", kino_app.views.page_news, name='page_news'),
    path("poster", kino_app.views.poster, name='poster'),
    path("search", kino_app.views.search, name='search'),
    path("page/<int:page_id>", kino_app.views.page, name='page'),

]