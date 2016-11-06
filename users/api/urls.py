#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from .views import ValidationUser


urlpatterns = [
    url(
        r'^validate',
        ValidationUser.as_view(),
        name='api-user-validation'
    )
]