#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.response import Response

from tokens.models import Token
from..models import Channel


class ChannelTokenSerializer(serializers.Serializer):
    uid = serializers.CharField()
    created_at = serializers.DateTimeField(format='%d.%m.%Y %H:%M')
    expiry_at = serializers.DateTimeField(format='%d.%m.%Y %H:%M')


class ChannelSerializer(serializers.Serializer):
    pk = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=25)
    site = serializers.URLField()
    domain = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)
    created_at = serializers.DateTimeField(required=False, format='%d.%m.%Y %H:%M:%S')
    uid = serializers.CharField(required=False)

    def validate_site(self, value):
        if not value.startswith('http'):
            return serializers.ValidationError('Link must have start with "http"')
        return value
