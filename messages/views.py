#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from channels.models import Channel
from .models import Message


@require_http_methods(['GET', 'POST'])
def chat_individual(request, pk):
    try:
        channel = Channel.objects.get(uid=pk)
        messages = Message.active.filter(channel__uid=pk).order_by('created_at')

        return render(request, 'portal/messages/chat.html', {'channel': channel, 'messages': messages})

    except Channel.DoesNotExist:
        return HttpResponseNotFound()

