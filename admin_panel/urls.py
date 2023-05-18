from django.urls import path, include

import admin_panel.views

# делать на главной странице проэкта список фильмов только для главного кинотеатра чтобы не усложнять себе жизнь
urlpatterns = [
    path("", admin_panel.views.statistic, name='statistic'),
    path("film_form", admin_panel.views.FilmForm.as_view(), name='film_form'),
    path("update_film/<str:id>", admin_panel.views.update_film, name='update_film'),
    path("films", admin_panel.views.films, name='films'),
    path("cinemas", admin_panel.views.cinemas, name='admin_cinemas'),

    path("stocks_table", admin_panel.views.stocks, name='stocks_table'),
    path("stock_form", admin_panel.views.get_stock_form, name='stock_form'),
    path("update_stock/<str:id>", admin_panel.views.update_stock, name='update_stock'),
    path("delete_stock/<str:id>", admin_panel.views.delete_stock, name='delete_stock'),

    path("seances", admin_panel.views.seances, name='seances'),
    path("seance_form", admin_panel.views.get_seance_form, name='seance_form'),
    path("delete_seance/<str:id>", admin_panel.views.delete_seance, name='delete_seance'),

    path("news_table", admin_panel.views.news, name='news_table'),
    path("news_form", admin_panel.views.get_news_form, name='news_form'),
    path("update_news/<str:id>", admin_panel.views.update_news, name='update_news'),
    path("delete_news/<str:id>", admin_panel.views.delete_news, name='delete_news'),

    path("pages", admin_panel.views.pages, name='pages'),
    path("page_form", admin_panel.views.get_page_form, name='page_form'),
    path("update_page/<str:id>", admin_panel.views.update_page, name='update_page'),
    path("delete_page/<str:id>", admin_panel.views.delete_page, name='delete_page'),

    path("update_main_page", admin_panel.views.update_main_page, name='update_main_page'),

    path("clients", admin_panel.views.clients, name='clients'),
    path("update_client/<str:id>", admin_panel.views.update_client, name='update_client'),
    path("delete_client/<str:id>", admin_panel.views.delete_client, name='delete_client'),

    path("choose_client", admin_panel.views.choose_client, name='choose_client'),
    path("delete_template/<str:id>", admin_panel.views.deleteHtmlTemplate, name='delete_template'),


    path("mailing", admin_panel.views.mailing, name='mailing'),
    path("get_task_info", admin_panel.views.get_task_info, name='get_task_info'),

    path("cinema_card/<str:id>", admin_panel.views.cinema_card, name='cinema_card'),

    path("hall_form", admin_panel.views.get_hall_form, name='hall_form'),
    path("update_hall/<str:number>", admin_panel.views.update_hall, name='update_hall'),
    path("delete_hall/<str:number>", admin_panel.views.delete_hall, name='delete_hall'),

    path("banners_sliders", admin_panel.views.banners_sliders, name='banners_sliders'),
    path("top_carousel", admin_panel.views.top_carousel, name='top_carousel'),
    path("background", admin_panel.views.back_img, name='background'),
    path("bottom_carousel", admin_panel.views.bottom_carousel, name='bottom_carousel'),

    path("update_contacts", admin_panel.views.update_contacts, name='update_contacts'),

]
