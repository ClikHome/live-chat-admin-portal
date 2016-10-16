#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from channels.views import (
    channel_create, channel_detail, channel_list, channel_edit, channel_remove)


urlpatterns = [
    url(
        r'^$',
        channel_list,
        name='channel-list'
    ),

    url(
        r'^(?P<pk>[0-9]+)/',
        include([
            url(
                r'^$',
                channel_detail,
                name='channel-detail',
            ),

            url(
                r'^edit/?$',
                channel_edit,
                name='channel-edit'
            ),

            url(
                r'^remove/?$',
                channel_remove,
                name='channel-remove'
            )
        ])
    ),

    url(
        r'^create/$',
        channel_create,
        name='channel-create'
    ),
]