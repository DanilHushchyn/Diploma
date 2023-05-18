"""avada_project2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.urls import path, include
from django.views.i18n import JavaScriptCatalog

import Diploma.settings as proj
import admin_panel.views
from django.db import connections

connections.close_all()
urlpatterns = i18n_patterns(
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),

    path('admin/', include('admin_panel.urls')),
    path('accounts/', include('user.urls')),
    path('', include('kino_app.urls')),

) + static(proj.STATIC_URL, document_root=proj.STATIC_ROOT)
urlpatterns += static(proj.MEDIA_URL, document_root=proj.MEDIA_ROOT)

# if proj.DEBUG:
#     import debug_toolbar
#
#     urlpatterns = [
#                       path('__debug__/', include(debug_toolbar.urls)),
#                   ] + urlpatterns + static(proj.MEDIA_URL, document_root=proj.MEDIA_ROOT)

# from django.contrib.static.views import serve
# from django.views.static import serve as media_serve
# from django.conf import settings
#
# if not settings.DEBUG:
#     urlpatterns.append(path('static/<path:path>', serve, {"insecure": True}))
#     urlpatterns.append(path('media/<path:path>', media_serve, {"document_root": proj.MEDIA_ROOT}))
