#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import (
    HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotFound)
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required


from .models import Website
from .forms import WebsiteForm


@login_required
@require_http_methods(['GET'])
def domain_list(request):
    websites = Website.objects.filter(owner=request.user)

    return render(request, 'portal/domains/list.html', {'websites': websites})


@login_required
@require_http_methods(['GET'])
def domain_detail(request, domain=None):
    website = get_object_or_404(Website, domain=domain, owner=request.user)

    # 403, Forbidden
    if not (website.owner == request.user):
        return HttpResponseForbidden()

    return render(request, 'portal/domains/detail.html', {'website': website})


@login_required
@require_http_methods(['GET', 'POST'])
def domain_create(request):
    form = WebsiteForm(request.user, request.POST or None)

    if form.is_valid():
        channel_id = form.cleaned_data['channel']

        if channel_id and channel_id.isdigit():
            channel_id = int(channel_id)

        Website.objects.create(
            url=form.cleaned_data['url'],
            channel_id=channel_id,
            owner=request.user,
        )

        return redirect(reverse('domain-list'))
    return render(request, 'portal/domains/create.html', {'form': form})


@login_required
@require_http_methods(['GET', 'POST'])
def domain_edit(request, domain=None):
    website = get_object_or_404(Website, domain=domain, owner=request.user)
    form = WebsiteForm(request.user, request.POST or None, instance=website)

    if form.is_valid():
        form.save()
        return redirect(reverse('domain-list'))

    return render(request, 'portal/domains/edit.html', {'form': form, 'website': website})


@login_required
@require_http_methods(['GET', 'POST'])
def domain_remove(request, domain=None):
    website = get_object_or_404(Website, domain=domain, owner=request.user)
    return render(request, 'portal/domains/remove.html', {'website': website})

