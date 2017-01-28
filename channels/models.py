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

from LiveChatBackend import mixins
# from domains.models import Website


def validate_site(value):
    if re.search(r':\d{3,}', value):
        raise ValidationError(_('Domain must be not local'))


class Channel(mixins.ModelMixin, models.Model):
    class Meta:
        verbose_name = _('channel')
        verbose_name_plural = _('Channels')

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

    owner = models.ForeignKey(
        User,
        related_name='channel_admin'
    )

    def save(self, *args, **kwargs):
        super(Channel, self).save(*args, **kwargs)

        # Save channel to settings
        r = redis.Redis(*settings.REDIS_CONNECTION)
        r.hset('channels', self.uid, self.pk)

    def __unicode__(self):
        return unicode(self.title)

