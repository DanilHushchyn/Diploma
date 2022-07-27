from django.contrib.auth.views import LoginView
from django.urls import path

from user.views import *

urlpatterns = [
    path("signup", signup, name='signup'),
    path("signin", signin, name='signin'),
    path (' accounts/login/ ' , LoginView. as_view () , name=' login') ,
]