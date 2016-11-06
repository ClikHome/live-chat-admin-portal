#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.authentication import (
    BasicAuthentication, TokenAuthentication, SessionAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from urlparse import urlparse
import requests


from ..models import Website, CacheWHOIS
from .serializers import DomainSerializer


def response_error(message=None, status=None):
    response = {'success': False, 'error': message}

    return Response(response, status=status)


class DomainIsAvailable(generics.RetrieveAPIView):
    queryset = Website.objects.all()
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        domain = request.GET.get('domain')
        http_referer = request.META.get('HTTP_REFERER')

        if http_referer and domain == urlparse(http_referer).netloc:
            try:
                website = self.queryset.get(domain=domain)
            except Website.DoesNotExist:
                website = None

            if not website:
                return response_error(_('Domain is not exists'))
            elif not website.is_approved:
                return response_error(_('Domain is not approved'))

            # Add getting chat template selected

            serializer = DomainSerializer(website)
            return Response({'data': serializer.data, 'success': True})
        return response_error(_('Wrong source'))


class DomainAvailable(generics.GenericAPIView):
    """
    BootstrapValidator request ['remote' type]

    Pages:
        - /portal/domains/create.html
        - /portal/domains/edit.html
    """

    queryset = Website.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = None

    def get(self, request, *args, **kwargs):
        http_referer = request.META.get('HTTP_REFERER')

        url = request.GET.get('url')
        domain = urlparse(url).netloc.replace('www.', '')
        valid = not (Website.objects.filter(domain=domain, owner=request.user).exists())

        # Edit form
        if not valid and domain in http_referer:
            valid = True

        return Response({'valid': valid})

# # Classes for JQuery Wizard
# class AddNewDomain(generics.GenericAPIView):
#     queryset = Website.objects.all()
#     permission_classes = [permissions.AllowAny]
#     serializer_class = None
#
#     def post(self, request, *args, **kwargs):
#         url = request.POST.get('url')
#         email = request.POST.get('email')
#         email_page = request.POST.get('email_page')
#
#         # Check email in WHOIS cache
#         domain = urlparse(url).netloc
#         email_in_whois = CacheWHOIS.objects.filter(domain=domain, email=email).exists()
#
#         print email_in_whois
#         #
#         # # If not, check email on email page
#         # if not email_in_whois:
#         #     if not email_page:
#         #         return response_error('Bad request', status=status.HTTP_400_BAD_REQUEST)
#         #
#         #     response = requests.get(email_page).content
#         #
#         #     if email not in response:
#         #         return response_error('Bad data', status=status.HTTP_400_BAD_REQUEST)
#         #
#         # send_mail(
#         #     subject='Domain confirmation',
#         #     message='',
#         #     from_email=settings.EMAIL_HOST_USER,
#         #     recipient_list=[email]
#         # )
#
#         return Response({'success': True, 'message': 'Email was sent'})


# class GetDomainOwner(generics.GenericAPIView):
#     """
#     Get owner of domain by WHOIS (email) for the validation
#     """
#     queryset = Website.objects.all()
#     permission_classes = [
#         permissions.AllowAny
#     ]
#     serializer_class = None
#
#     def post(self, request, *args, **kwargs):
#         domain = request.data.get('domain', None)
#
#         if not domain:
#             return response_error('Bad request', status=status.HTTP_400_BAD_REQUEST)
#
#         domain = urlparse(domain)
#         domain = domain.netloc or domain.path
#
#         # Check domain in the database
#         domain_already_registered = self.queryset.filter(domain=domain).exists()
#
#         if domain_already_registered:
#             return response_error('This domain already registered')
#
#         try:
#             domain_cached = CacheWHOIS.objects.get(domain=domain)
#             email = domain_cached.email
#
#         except ObjectDoesNotExist:
#             # Send request to whoisxmlapi.com
#             url = 'http://www.whoisxmlapi.com/whoisserver/WhoisService?domainName={domain}&' \
#                   'username={username}&password={password}&outputFormat=JSON'
#
#             params = {
#                 'domain': domain,
#                 'username': settings.WHOISXMLAPI_SETTINGS['username'],
#                 'password': settings.WHOISXMLAPI_SETTINGS['password']
#             }
#
#             # Example response: https://www.whoisxmlapi.com/order_paypal.php?domainName=google.com&outputFormat=json
#             response = requests.get(url=url.format(**params))
#
#             if response.status_code == 200:
#                 registrant_data = response.json()["WhoisRecord"]["registrant"]
#
#                 # Cache domain to database
#                 CacheWHOIS.objects.create(
#                     domain=domain,
#                     name=registrant_data.get('name'),
#                     email=registrant_data.get('email'),
#                     phone=registrant_data.get('telephone')
#                 )
#
#                 email = registrant_data.get('email')
#             else:
#                 return response_error('Bad response from WHOIS API', status=response.status_code)
#
#         return Response({
#             'success': True,
#             'data': {
#                 'email': email
#             }
#         # })
