#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin

from .views_api import ChatUserViewSet


urlpatterns = [
    # API
    url(
        r'^(?P<uid>[a-z0-9-]+)/$',
        ChatUserViewSet.as_view({'get': 'list'}),
        name='channel-users-list'
    ),

    # url(
    #     r'^'
    # )
]