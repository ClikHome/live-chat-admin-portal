#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.api.serializers import ChatUserSerializer
from .models import ChatUser


class ChatUserViewSet(viewsets.ViewSet):
    lookup_field = 'uid'
    permission_classes = [
        permissions.AllowAny
    ]

    # def retrieve(self, request, pk=None, username=None):
    #     queryset = ChatUser.active.all()
    #     user = queryset.filter(channel__uid=pk, username=username).first()
    #     serializer = ChatUserSerializer(user)
    #     return Response(serializer.data)

    def list(self, request, uid=None):
        queryset = ChatUser.active.filter(channel__uid=uid)
        serializer = ChatUserSerializer(queryset, many=True)
        return Response(serializer.data)


@api_view()
def chat_user_auth(request):
    pass
