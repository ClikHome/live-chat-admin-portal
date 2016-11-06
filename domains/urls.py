#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from .views import (
    domain_detail, domain_list, domain_create, domain_edit, domain_remove)


urlpatterns = [
    url(
        r'^$',
        domain_list,
        name='domain-list'
    ),

    url(
        r'^create$',
        domain_create,
        name='domain-create'
    ),

    url(
        r'(?P<domain>[w]?\.?[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,})/',
        include([
            url(
                r'^detail',
                domain_detail,
                name='domain-detail'
            ),

            url(
                r'^edit',
                domain_edit,
                name='domain-edit'
            ),

            url(
                r'^remove',
                domain_remove,
                name='domain-remove'
            ),
        ])
    )


]