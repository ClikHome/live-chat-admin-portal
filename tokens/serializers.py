#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import serializers

from channels.api.serializers import ChannelSerializer


class TokenSerializer(serializers.Serializer):
    """
    Data for token AJAX validation
    """
    created_at = serializers.DateTimeField(format='%d.%m.%Y %H:%M')
    expiry_at = serializers.DateTimeField(format='%d.%m.%Y %H:%M')
    remaining_time = serializers.CharField(max_length=50)
    is_active = serializers.BooleanField()
    channel = ChannelSerializer()



