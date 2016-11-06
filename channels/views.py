#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.http import (
    HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotFound)

from .models import Channel
from .forms import ChannelForm
from messages.models import Message
from users.models import ChatUser
from domains.models import Website


@require_http_methods(['GET', 'POST'])
def channel_create(request):
    form = ChannelForm(request.user, request.POST or None)
    not_used_domains = Website.objects.filter(channel__isnull=True, owner=request.user)

    if form.is_valid():
        form.save()
        return redirect(reverse('channel-list'))
    return render(request, 'portal/channels/create.html', {'form': form, 'websites': not_used_domains})


@require_http_methods(['GET', 'POST'])
def channel_edit(request, pk=None):
    channel = get_object_or_404(Channel, pk=pk)
    form = ChannelForm(request.user, request.POST or None, instance=channel)

    if form.is_valid():
        form.save()
        return redirect(reverse('channel-list'))
    return render(request, 'portal/channels/edit.html', {'channel': channel, 'form': form})


@require_http_methods(['GET', 'POST'])
def channel_remove(request, pk=None):
    channel = get_object_or_404(Channel, pk=pk)

    if request.method == 'POST':
        # Remove channel from domains
        Website.objects\
            .filter(channel=channel, owner=request.user)\
            .update(channel=None)

        # Remove channel
        channel.delete()
        return redirect(reverse('channel-list'))

    if channel.owner != request.user:
        return HttpResponseForbidden()

    channel.websites = Website.objects.filter(channel=channel, owner=request.user)

    return render(request, 'portal/channels/remove.html', {'channel': channel})


@require_http_methods(['GET'])
def channel_detail(request, pk=None):
    channel = get_object_or_404(Channel, pk=pk)

    if not (channel.owner == request.user):
        # 403, Forbidden
        return HttpResponseForbidden()

    channel.users = ChatUser.objects.filter(channel=channel)
    channel.messages = Message.objects.filter(channel=channel)

    return render(request, 'portal/channels/detail.html', {'channel': channel})


@require_http_methods(['GET'])
def channel_list(request):
    # if not request.user.is_authenticated():
    #     return redirect(reverse('admin'))

    channels = Channel.objects.filter(owner_id=request.user.id)

    for channel in channels:
        channel.messages = Message.active.filter(channel=channel).count()
        channel.users = ChatUser.active.filter(channel=channel).count()
        channel.websites = Website.objects.filter(channel=channel)

    return render(request, 'portal/channels/list.html', {'channels': channels})


