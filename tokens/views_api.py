#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Token
from .serializers import TokenSerializer


class TokenViewSet(viewsets.ViewSet):
    model = Token
    serializer_class = TokenSerializer
    queryset = model.objects.all()

    def retrieve(self, request, pk=None):
        queryset = Token.objects.all()
        token = queryset.filter(uid=pk).first()
        serializer = TokenSerializer(token)

        if token:
            return Response({'data': serializer.data, 'success': True})
        return Response({'data': {}, 'success': False})