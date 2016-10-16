#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from rest_framework import serializers

from users.models import ChatUser
from ..models import Message


class UserMessageInfoSerializer(serializers.Serializer):
    username = serializers.CharField()

    class Meta:
        model = ChatUser


class MessageSerializer(serializers.Serializer):
    pk = serializers.CharField()
    body = serializers.CharField()
    user = UserMessageInfoSerializer()
    created_at = serializers.DateTimeField(settings.MESSAGES_DATETIME_FORMAT)

    class Meta:
        model = Message

