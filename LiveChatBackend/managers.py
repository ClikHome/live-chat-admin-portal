#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models


class OnlyActiveManager(models.Manager):
    def get_queryset(self):
        return super(OnlyActiveManager, self).get_queryset()\
            .filter(is_active=True)