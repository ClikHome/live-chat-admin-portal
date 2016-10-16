#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
import oauth2client.contrib.django_util.site as django_util_site

from .views import AuthUserViewSet

urlpatterns = [
    url(
        r'^',
        AuthUserViewSet.as_view({'get': 'list'}),
    )
]