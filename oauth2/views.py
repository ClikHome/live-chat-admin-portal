#!/usr/bin/env python
# -*- coding: utf-8 -*-

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope
from rest_framework import permissions, viewsets

from users.api.serializers import ChatUserSerializer
from users.models import ChatUser


class AuthUserViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
        TokenHasReadWriteScope
    ]
    queryset = ChatUser.active.all()
    serializer_class = ChatUserSerializer

    def get(self, request):
        print request

