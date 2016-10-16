#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import serializers

from users.models import ChatUser


class ChatUserSerializer(serializers.Serializer):
    username = serializers.CharField()

    class Meta:
        model = ChatUser



