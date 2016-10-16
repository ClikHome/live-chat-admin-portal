"""LiveChatBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext as _
import oauth2_provider.views as oauth2_views
from rest_framework_jwt.views import (obtain_jwt_token, refresh_jwt_token, verify_jwt_token)


# OAuth2 provider endpoints
oauth2_endpoint_views = [
    url(r'^authorize/$', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    url(r'^token/$', oauth2_views.TokenView.as_view(), name="token"),
    url(r'^revoke-token/$', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

# if settings.DEBUG:
#     # OAuth2 Application Management endpoints
#     oauth2_endpoint_views += [
#         url(r'^applications/$', oauth2_views.ApplicationList.as_view(), name="list"),
#         url(r'^applications/register/$', oauth2_views.ApplicationRegistration.as_view(), name="register"),
#         url(r'^applications/(?P<pk>\d+)/$', oauth2_views.ApplicationDetail.as_view(), name="detail"),
#         url(r'^applications/(?P<pk>\d+)/delete/$', oauth2_views.ApplicationDelete.as_view(), name="delete"),
#         url(r'^applications/(?P<pk>\d+)/update/$', oauth2_views.ApplicationUpdate.as_view(), name="update"),
#     ]
#
#     # OAuth2 Token Management endpoints
#     oauth2_endpoint_views += [
#         url(r'^authorized-tokens/$', oauth2_views.AuthorizedTokensListView.as_view(),
#             name="authorized-token-list"),
#         url(r'^authorized-tokens/(?P<pk>\d+)/delete/$', oauth2_views.AuthorizedTokenDeleteView.as_view(),
#             name="authorized-token-delete"),
#     ]

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^portal/', include('portal.urls'), name='portal'),
    url(r'^channel/', include('channels.urls'), name='channel'),
    url(r'^messages/', include('messages.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^token/', include('tokens.urls')),
    url(r'^oauth2/', include('oauth2.urls')),

    # API
    url(r'^api/v1.0/', include([
        url(r'^auth/', include([
            url(r'^token', obtain_jwt_token, name='auth_token'),
            url(r'^refresh', refresh_jwt_token, name='auth_refresh'),
            url(r'^verify', verify_jwt_token, name='auth_verify'),
        ])),
        url(r'^messages/', include('messages.api.urls')),
        url(r'^channels/', include('channels.api.urls')),
    ]))

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
