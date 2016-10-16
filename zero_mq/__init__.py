#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LiveChatBackend.settings")
django.setup()