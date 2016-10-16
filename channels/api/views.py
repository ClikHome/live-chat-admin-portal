#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from django.utils import timezone
from urlparse import urlparse

from tokens.models import Token
from ..models import Channel
from .serializers import (ChannelSerializer,)


class ChannelRetrieve(generics.RetrieveAPIView):
    queryset = Channel.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]

    def retrieve(self, request, *args, **kwargs):
        channel_uid = request.GET.get('channel')
        domain = request.GET.get('domain')
        http_referer = request.META.get('HTTP_REFERER')

        error = lambda x: {'success': False, 'error': x}

        if http_referer and domain == urlparse(http_referer).netloc:
            channel = self.queryset.get(uid=channel_uid, domain=domain)

            if channel and channel.is_active:
                return Response({'success': True})
            elif channel and not channel.is_active:
                return Response(error('Channel is not active'))

        return Response(error(None))


class ChannelCreate(generics.CreateAPIView):
    model = Channel
    serializer_class = ChannelSerializer
    queryset = Channel.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, TokenAuthentication)

    def create(self, request, *args, **kwargs):
        data = request.data.dict()

        if request.user.is_authenticated() \
                and self.serializer_class(data=data).is_valid():
            data['superuser_id'] = request.user.pk
            channel = Channel.objects.get_or_create(**data)
            serializer = self.serializer_class(channel[0])
            was_created = channel[1]

            return Response({
                'channel': serializer.data,
                'created': was_created
            })


class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    pass

