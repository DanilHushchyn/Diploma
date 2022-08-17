from django.contrib.auth.views import LoginView
from django.urls import path

from user.views import *

urlpatterns = [
    path('register', SignUp.as_view(), name='register'),
    path('signin', loginView, name='signin'),
    path('logout', logoutView, name='logout'),
]
