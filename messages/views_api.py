#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions

from .models import Message
from .serializers import MessageSerializer


class MessageViewSet(viewsets.ViewSet):
    permission_classes = [
        permissions.AllowAny
    ]

    def list(self, request, pk=None):
        queryset = Message.active.filter(channel__uid=pk)
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)