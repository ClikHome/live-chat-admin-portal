from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
import uuid

from channels.models import Channel
from LiveChatBackend.managers import OnlyActiveManager


class TokenDuration(models.Model):
    title = models.CharField(_('Title'), max_length=50)
    days = models.IntegerField(_('Days'), default=0)
    months = models.IntegerField(_('Months'), default=0)
    years = models.IntegerField(_('Years'), default=0)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(_('Is active'), default=True)

    @property
    def timedelta(self):
        return relativedelta(
            days=self.days, months=self.months, years=self.years
        )

    def save(self, *args, **kwargs):
        days_in_year, days_in_month = (365.2425, 30.437)

        if self.days > days_in_year:
            self.years += int(self.days / days_in_year)
            self.days = int(self.days % days_in_year)

        if self.days > days_in_month:
            self.months += int(self.days / days_in_month)
            self.days = int(self.days % days_in_month)

        super(TokenDuration, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title


class UsingManager(models.Manager):
    def get_queryset(self):
        return super(UsingManager, self).get_queryset()\
            .filter(is_used=True)


class Token(models.Model):
    uid = models.CharField(_('Unique token'), max_length=50, default=uuid.uuid4)
    duration = models.ForeignKey(TokenDuration, related_name='token_duration', null=True)
    channel = models.ForeignKey(Channel, related_name='channel_token', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(_('Is active'), default=False)
    is_used = models.BooleanField(default=False)

    # Action time
    started_at = models.DateTimeField(_('Started at'), null=True, blank=True)
    expiry_at = models.DateTimeField(_('Expiry at'), null=True, blank=True)
    stopped_at = models.DateTimeField(_('Stoped at'), null=True, blank=True)

    # Managers
    active = OnlyActiveManager()
    using = UsingManager()
    objects = models.Manager()

    def activation(self):
        if not self.is_used:
            for token in Token.active.filter(channel__uid=self.channel.uid, is_used=True):
                token.is_used = False
                token.save()

            self.is_used = True

            # Check token was started early
            if self.stopped_at:
                self.expiry_at += timezone.now() - self.stopped_at
            else:
                self.started_at = datetime.utcnow()
                self.expiry_at = self.started_at + self.duration.timedelta

            self.save()
            return True
        return False

    def generate_new_uid(self):
        self.uid = uuid.uuid4()

    @classmethod
    def for_time(cls, days=0, weeks=0, months=0, years=0):
        return Token.objects.create(
            expiry_at=timezone.now().date() + relativedelta(days=days, weeks=weeks, months=months, years=years))

    @property
    def remaining_time(self):
        if self.expiry_at and self.expiry_at > timezone.now():
            return str(self.expiry_at - timezone.now())
        return 0

    def save(self, *args, **kwargs):
        if self.expiry_at and self.expiry_at < timezone.now():
            self.is_active = False
        super(Token, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.uid
