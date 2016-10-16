#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from .views import (ChannelRetrieve, ChannelCreate)


urlpatterns = [
    url(
        r'^validation$',
        ChannelRetrieve.as_view(),
        name='api_channel_validation',
    ),

    url(
        r'^create$',
        ChannelCreate.as_view(),
        name='api_channel_create',
    ),


]