#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django import forms

from urlparse import urlparse

from .models import Website
from channels.models import Channel


class WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = ('url',)

    url = forms.CharField(
        label=_('Website URL'),
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': "form-control col-md-7 col-xs-12",

        }),
        help_text=_('Website URL')
    )

    channel = forms.ChoiceField(
        label=_('Channel'),
        required=False,
        choices=(),
        widget=forms.Select(attrs={
            'class': 'select2_single form-control',
            'style': 'width: 100%',
        }),
        help_text=_('Messages channel for current website')
    )

    def __init__(self, user, *args, **kwargs):
        super(WebsiteForm, self).__init__(*args, **kwargs)
        self.user = user

        # Create choices
        choices = Channel.objects.filter(owner=user).values_list('pk', 'title')
        self.fields['channel'].choices = [('', '')] + list(choices)

        # Edit form
        if self.instance and self.instance.channel:
            self.fields['channel'].initial = str(self.instance.channel.pk)

    def save(self, *args, **kwargs):
        data = self.cleaned_data

        url = data.get('url')
        domain = urlparse(url).netloc
        channel = data.get('channel')

        try:
            website = Website.objects.get(domain=domain, owner=self.user)
        except Website.DoesNotExist:
            website = Website()

        website.url = url
        website.owner = self.user

        if channel and isinstance(channel, (str, unicode)) and channel.isdigit():
            website.channel_id = int(channel)

        return website.save()

class WebsiteNewEmail(forms.Form):
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.TextInput(attrs={
            'class': "form-control col-md-7 col-xs-12",
        }),
        help_text=_('New email for domain verification')
    )

    email_page = forms.URLField(
        label=_('URL'),
        widget=forms.TextInput(attrs={
            'class': "form-control col-md-7 col-xs-12",
        }),
        help_text=_('Page with this email')
    )