#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.response import Response

from ..models import Website


class DomainSerializer(serializers.Serializer):
    domain = serializers.CharField()
    channel = serializers.CharField()

