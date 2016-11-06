#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django import forms

from .models import Channel
from domains.models import Website


class ChannelForm(forms.ModelForm):
    title = forms.CharField(
        label=_('Title'),
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': "form-control col-md-7 col-xs-12",
        })
    )

    websites = forms.MultipleChoiceField(
        label=_('Websites'),
        required=False,
        choices=(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control chosen-select',
            'style': 'width: 100%',
        }),

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
        fields = ('title', 'is_active')

    def __init__(self, user, *args, **kwargs):
        super(ChannelForm, self).__init__(*args, **kwargs)

        self.user = user

        # Create choices
        choices = Website.objects.filter(owner=self.user, channel__isnull=True).values_list('pk', 'domain')
        self.fields['websites'].choices = [('', '')] + list(choices)

        # Edit form
        if self.instance:
            channel_domains = Website.objects \
                .filter(owner=self.user, channel=self.instance) \
                .values_list('pk', 'domain')
            self.fields['websites'].choices += channel_domains
            self.fields['websites'].initial = [str(domain[0]) for domain in channel_domains]

    def is_valid(self):
        return super(ChannelForm, self).is_valid()

    def save(self, *args, **kwargs):
        data = self.cleaned_data

        # Create or edit channel
        channel = self.instance
        channel.title = data['title']
        channel.is_active = data['is_active']
        channel.owner = self.user
        channel.save()

        # Update selected websites
        websites_id_selected = data.get('websites')
        print websites_id_selected

        if websites_id_selected and all(pk.isdigit() for pk in websites_id_selected):
            websites_id_selected = map(int, websites_id_selected)

            # Remove websites
            Website.objects \
                .filter(channel=channel) \
                .exclude(pk__in=websites_id_selected) \
                .update(channel=None)

            # Add
            Website.objects \
                .filter(pk__in=websites_id_selected, channel__isnull=True) \
                .update(channel=channel)

        return channel


class ChannelEditForm(forms.ModelForm):
    title = forms.CharField(
        label=_('Title'),
        max_length=50,
        widget=forms.TextInput(attrs={
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
        fields = ('title', 'is_active')

    def is_valid(self):
        print self.data
        return super(ChannelEditForm, self).is_valid()

