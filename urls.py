
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from apps.web import urls as web_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include(web_urls, namespace='web')),
    
]
