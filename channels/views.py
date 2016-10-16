#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseForbidden
from django.views.decorators.http import require_http_methods

from .models import Channel
from .forms import (ChannelCreateForm, ChannelEditForm)
from messages.models import Message
from users.models import ChatUser


@require_http_methods(['GET', 'POST'])
def channel_create(request):
    form = ChannelCreateForm(request.POST or None)

    if form.is_valid():
        form.save(user=request.user)
        return redirect(reverse('channel-list'))
    return render(request, 'portal/channels/create.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def channel_edit(request, pk=None):
    channel = Channel.objects.get(pk=pk)
    form = ChannelEditForm(request.POST or None, instance=channel)

    if request.method == 'POST' and form.is_valid():
        form.save()

        return redirect(reverse('channel-list'))

    return render(request, 'portal/channels/edit.html', {
        'channel': channel, 'form': form
    })


@require_http_methods(['GET', 'POST'])
def channel_remove(request, pk=None):
    channel = Channel.objects.get(pk=pk)

    if request.method == 'POST':
        Channel.objects.get(pk=pk).delete()
        return redirect(reverse('channel-list'))

    if channel.superuser != request.user:
        return HttpResponseForbidden()

    return render(request, 'portal/channels/remove.html', {'channel': channel})


@require_http_methods(['GET'])
def channel_detail(request, pk=None):
    channel = Channel.objects.get(pk=pk)
    channel.users = ChatUser.objects.filter(channel=channel)
    channel.messages = Message.objects.filter(channel=channel)

    return render(request, 'portal/channels/detail.html', {'channel': channel})


@require_http_methods(['GET'])
def channel_list(request):
    # if not request.user.is_authenticated():
    #     return redirect(reverse('admin'))

    channels = Channel.objects.filter(superuser__pk=request.user.id)

    for channel in channels:
        channel.messages = Message.active.filter(channel=channel).count()
        channel.users = ChatUser.active.filter(channel=channel).count()

    return render(request, 'portal/channels/list.html', {'channels': channels})


