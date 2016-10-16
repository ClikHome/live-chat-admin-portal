#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from .views import MessagesHistory


urlpatterns = [
    url(r'^(?P<pk>[a-zA-Z0-9-]+)/', include([
        url(
            r'^history/$',
            MessagesHistory.as_view({'post': 'list'}),

        ),

    ]))
]