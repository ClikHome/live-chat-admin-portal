#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import serializers

from users.models import ChatUser
from .models import Message


class UserMessageInfoSerializer(serializers.Serializer):
    username = serializers.CharField()

    class Meta:
        model = ChatUser


class MessageSerializer(serializers.Serializer):
    body = serializers.CharField()
    user = UserMessageInfoSerializer()
    created_at = serializers.DateTimeField(format='%H:%M:%S')

    class Meta:
        model = Message

