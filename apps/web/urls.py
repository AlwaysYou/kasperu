# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import (home, create_account)

app_name = 'web'

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^create_account$', create_account, name='create_account'),
]
