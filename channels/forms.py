#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django import forms

from .models import Channel


class ChannelCreateForm(forms.ModelForm):
    title = forms.CharField(
        label=_('Title'),
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': "form-control col-md-7 col-xs-12",
        })
    )

    site = forms.URLField(
        label=_('Url'),
        help_text=_('Site for the chat'),
        widget=forms.TextInput(attrs={
            'placeholder': 'http://google.com',
            'class': "form-control col-md-7 col-xs-12",
            'type': 'url',
        })
    )

    is_active = forms.BooleanField(
        label=_('Active'),
        help_text=_('Channel is active'),
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': "icheckbox_flat-green",
            'checked': 'true',
        })
    )

    class Meta:
        model = Channel
        fields = ('title', 'site', 'is_active')

    def is_valid(self):
        return super(ChannelCreateForm, self).is_valid()

    def save(self, *args, **kwargs):
        data = self.cleaned_data

        new_channel = Channel(
            title=data['title'],
            superuser=kwargs['user'],
            site=data['site'],
            is_active=data['is_active']
        )

        new_channel.save()
        return new_channel


class ChannelEditForm(forms.ModelForm):
    title = forms.CharField(
        label=_('Title'),
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': "form-control col-md-7 col-xs-12",
        })
    )

    site = forms.URLField(
        label=_('Url'),
        help_text=_('Site for the chat'),
        widget=forms.TextInput(attrs={
            'placeholder': 'http://google.com',
            'class': "form-control col-md-7 col-xs-12",
        })
    )

    is_active = forms.BooleanField(
        label=_('Active'),
        help_text=_('Channel is active'),
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': "icheckbox_flat-green",
        })
    )

    class Meta:
        model = Channel
        fields = ('title', 'site', 'is_active')

    def is_valid(self):
        print self.data
        return super(ChannelEditForm, self).is_valid()
