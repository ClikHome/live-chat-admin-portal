#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

from .views_api import TokenViewSet


urlpatterns = [
    # API
    # url(
    #     r'^(?P<pk>[a-zA-Z0-9-]+)$',
    #     TokenViewSet.as_view({'get': 'retrieve'}),
    #     name='token-detail',
    # ),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])