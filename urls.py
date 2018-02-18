
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from apps.web import urls as web_urls
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include(web_urls, namespace='web')),
] + (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +
     static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
