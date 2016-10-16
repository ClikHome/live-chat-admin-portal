#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        if '\migrations' in root and name != '__init__.py':
            os.remove(os.path.join(root, name))