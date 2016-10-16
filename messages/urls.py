#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin
from django.utils.translation import ugettext as _

from .views_api import MessageViewSet


urlpatterns = [
    url(
        r'^(?P<pk>[a-z0-9-]+)$',
        MessageViewSet.as_view({'get': 'list'}),
        name='messages-list'
    ),
]