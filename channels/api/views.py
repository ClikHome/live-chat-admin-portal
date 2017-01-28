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
from messages.models import Message
from messages.api.serializers import MessageSerializer
from domains.models import Website


class ChannelRetrieve(generics.RetrieveAPIView):
    queryset = Channel.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]

    def retrieve(self, request, *args, **kwargs):
        channel_uid = request.GET.get('channel_uid')
        domain = request.GET.get('domain')
        http_referer = request.META.get('HTTP_REFERER')
        http_referer = 'http://site.com/'  # !!! DEBUG

        if http_referer and domain == urlparse(http_referer).netloc:
            try:
                website = Website.objects.get(domain=domain)

                if not (channel_uid == website.channel.uid):
                    return Response(status=status.HTTP_404_NOT_FOUND)

                # Channel is not active
                if website.channel and not website.channel.is_active:
                    return Response(status=status.HTTP_403_FORBIDDEN)

                messages = Message.active.filter(channel=website.channel).order_by('-created_at')[:30]
                serializer = MessageSerializer(messages, many=True)

                return Response({'success': True, 'messages': serializer.data})

            # Channel not exists
            except Channel.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        # Wrong referrer
        return Response(status=status.HTTP_400_BAD_REQUEST)


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

