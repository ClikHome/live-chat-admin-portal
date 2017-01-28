#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin
from django.utils.translation import ugettext as _

from .views import chat_individual


urlpatterns = [

    url(
        r'^(?P<pk>[a-z0-9-]+)',
        chat_individual,
        name='chat-individual'
    )






]