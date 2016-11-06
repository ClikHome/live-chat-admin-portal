#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework import status

from urlparse import urlparse

from ..models import ChatUser


class ValidationUser(generics.RetrieveAPIView):
    queryset = ChatUser.objects.all()
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        http_referer = request.META.get('HTTP_REFERER')

        if http_referer:
            print "HTTP REFERER: " + http_referer

        phone = request.POST.get('phone')
        username = request.POST.get('username')
        channel_uid = request.POST.get('channel_uid')

        try:
            user = ChatUser.objects.get(
                channel__uid=channel_uid,
                phone=phone,
                username=username
            )

        except ChatUser.DoesNotExist:
            user = None

        print user

        return Response({'success': True})