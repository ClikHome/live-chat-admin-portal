#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from .views import index


urlpatterns = [
    url(r'^$', index),
]