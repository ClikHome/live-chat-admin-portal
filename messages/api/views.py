#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from ..models import Message
from .serializers import MessageSerializer


class MessagesHistory(viewsets.ViewSet):
    model = Message
    queryset = Message.active.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    paginate_by = 5

    def list(self, request, pk=None):
        start = request.POST.get('start', None)

        if start == 0:
            return Response({'messages': [], 'success': False})
        elif start is None:
            start = self.queryset.count()

        messages = self.queryset.filter(
            channel__uid=pk, pk__lte=int(start))[:self.paginate_by]
        serializer = MessageSerializer(messages, many=True)

        if serializer.data:
            return Response({
                'messages': serializer.data,
                'success': True
            })
        return Response({'messages': [], 'success': False})






