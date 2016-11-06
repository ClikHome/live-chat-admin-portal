#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions

from .models import Token
from .serializers import TokenSerializer


class ChannelTokensAPIList(generics.ListAPIView):
    model = Token
    serializer_class = TokenSerializer

    def get_queryset(self):
        queryset = super(ChannelTokensAPIList, self).get_queryset()
        return queryset.filter(uid=self.kwargs.get('channel'))
