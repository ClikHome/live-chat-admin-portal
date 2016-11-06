#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import template
import json

from channels.models import Channel


register = template.Library()


@register.simple_tag(name='validation_values')
def channel_field(field, user, exclude=None):
    channels = Channel.objects.filter(owner=user)
    fields = list(channels.values_list(field, flat=True))

    if isinstance(exclude, (str, unicode)) and exclude in fields:
        fields.remove(exclude)

    return json.dumps(fields)