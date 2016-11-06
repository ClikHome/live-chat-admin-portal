#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin
from django.utils.translation import ugettext as _

from .views import chat


urlpatterns = [
    url(
        r'^chat',
        chat,
        name='chat'
    ),


]