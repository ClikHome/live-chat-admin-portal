#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from channels.models import Channel
from .models import Message


@require_http_methods(['GET'])
def chat(request):
    channels = Channel.objects.filter(superuser=request.user)
    messages = Message.active.filter(channel__in=channels)

    return render(request, 'portal/messages/chat.html', {'messages': messages})
