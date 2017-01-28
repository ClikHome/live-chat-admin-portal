#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .models import Channel


def channels_processor(request):
    channels = Channel.objects.filter(owner=request.user)
    return {'channels': channels}