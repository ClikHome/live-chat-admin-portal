from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import urlparse

from LiveChatBackend import mixins
from channels.models import Channel


class Website(mixins.ModelMixin, models.Model):
    class Meta:
        verbose_name = _('website')
        verbose_name_plural = _('Websites')
        unique_together = [
            ('domain', 'owner'),
        ]

    url = models.URLField(
        _('URL'),
        max_length=255,
        help_text=_('Site that chat will use'),
    )

    domain = models.CharField(
        _('Domain'),
        max_length=255,
        help_text=_('Domain of URL'),
    )

    owner = models.ForeignKey(
        User,
        related_name='domain_owner',
        help_text=_('Owner of the domain')
    )

    channel = models.ForeignKey(
        Channel,
        related_name='site_channel',
        null=True,
        blank=True,
        help_text=_('Channel for this site'),
    )

    def __init__(self, *args, **kwargs):
        super(Website, self).__init__(*args, **kwargs)

        # Change default value from the mixin
        self._meta.get_field('is_active').default = False

    def save(self, *args, **kwargs):
        if self.url:
            self.domain = urlparse.urlparse(self.url).netloc

        super(Website, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.domain)


class CacheWHOIS(models.Model):
    class Meta:
        verbose_name = _('cached domain')
        verbose_name_plural = _('Cached WHOIS domains')

    domain = models.CharField(
        _('Domain'),
        max_length=255,
        help_text=_('Domain')
    )

    name = models.CharField(
        _('Name'),
        max_length=255,
        null=True,
        blank=True,
        help_text=_('Name of registrant')
    )

    phone = models.CharField(
        _('Phone'),
        max_length=50,
        null=True,
        blank=True,
        help_text=_('Phone of registrant')
    )

    email = models.EmailField(
        _('Email'),
        help_text=_('Email of registrant')
    )

    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        _('Updated at'),
        auto_now=True
    )


