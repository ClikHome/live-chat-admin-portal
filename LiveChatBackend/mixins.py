#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import OnlyActiveManager


class ModelMixin(models.Model):
    is_active = models.BooleanField(
        _('Is active'),
        default=True
    )

    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        _('Updated at'),
        auto_now=True
    )

    # Managers
    objects = models.Manager()
    active = OnlyActiveManager()

    class Meta:
        abstract = True