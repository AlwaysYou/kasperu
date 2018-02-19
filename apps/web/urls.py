# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import (home, create_account, aplicativo, user_logout)

app_name = 'web'

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^create_account$', create_account, name='create_account'),
    url(r'^aplicativo$', aplicativo, name='aplicativo'),
    url(r'^user_logout$', user_logout, name='user_logout'),
]
