#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from .views import (DomainIsAvailable, DomainAvailable)


urlpatterns = [
    url(
        r'^available',
        DomainIsAvailable.as_view(),
        name='api_domain_is_available'
    ),

    # url(
    #     r'^get_owner$',
    #     GetDomainOwner.as_view(),
    #     name='api-get-owner'
    # ),


    url(
        r'^domain_available$',
        DomainAvailable.as_view(),
        name='api-domain-available',
    ),

    # url(
    #     r'^create$',
    #     AddNewDomain.as_view(),
    #     name='api-domain-create'
    # )

]