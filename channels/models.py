from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.conf import settings
import urlparse
import re
import uuid
import redis


def validate_site(value):
    if re.search(r':\d{3,}', value):
        raise ValidationError(_('Domain must be not local'))


class Channel(models.Model):
    class Meta:
        verbose_name = _('channel')
        verbose_name_plural = _('Channels')

    id = models.AutoField(primary_key=True)

    uid = models.CharField(
        _('Unique id'),
        max_length=50,
        default=uuid.uuid4,
        unique=True,
    )

    title = models.CharField(
        _('Title channel'),
        max_length=50,
        help_text=_('Only for the admin portal'),
    )

    superuser = models.ForeignKey(User, related_name='channel_admin')
    site = models.URLField(
        _('URL'),
        unique=True,
        help_text=_('Site that chat will use')
    )  # validators=[validate_site]
    domain = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    @property
    def path(self):
        return urlparse.urlparse(self.site).path

    def save(self, *args, **kwargs):
        if self.site:
            self.domain = urlparse.urlparse(self.site).netloc

        super(Channel, self).save(*args, **kwargs)

        # Save channel to settings
        r = redis.Redis(*settings.REDIS_CONNECTION)
        r.hset('channels', self.uid, self.pk)

    def __unicode__(self):
        return self.title

