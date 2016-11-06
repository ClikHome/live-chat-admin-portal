from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from dateutil.relativedelta import relativedelta
from django.conf import settings
import redis

from channels.models import Channel
from LiveChatBackend.managers import OnlyActiveManager


class ModelMixin(models.Model):
    is_active = models.BooleanField(
        _('Is active'),
        default=True
    )

    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        _('Updated at'),
        auto_now=True
    )

    # Managers
    objects = models.Manager()
    active = OnlyActiveManager()

    class Meta:
        abstract = True


class ChatUserRole(models.Model):
    class Meta:
        verbose_name = _('user role')
        verbose_name_plural = _('Users roles')
        unique_together = ('title', 'channel')

    title = models.CharField(max_length=50)
    channel = models.ForeignKey(Channel, related_name='channel')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title


class ChatUser(ModelMixin, models.Model):
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('Users')
        unique_together = [
            ('username', 'channel'),
            ('phone', 'channel'),
        ]
        ordering = ('username',)

    username = models.CharField(max_length=50)
    phone = models.CharField(max_length=50, null=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    channel = models.ForeignKey(Channel, related_name='user_channel')
    last_activity = models.DateTimeField(null=True, blank=True)

    # managers
    objects = models.Manager()
    active = OnlyActiveManager()

    def save(self, *args, **kwargs):
        super(ChatUser, self).save(*args, **kwargs)

        # Save user to redis
        # r = redis.Redis(*settings.REDIS_CONNECTION)
        # r.hset('channel:{}:users:id'.format(self.channel.uid), self.username, self.pk)

    def __unicode__(self):
        return unicode(self.username)


class ChatSession(models.Model):
    session_id = models.CharField(max_length=50)
    user = models.ForeignKey(ChatUser, related_name='session_user')
    created_at = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField()

    def __unicode__(self):
        return self.session_id


class UserBan(models.Model):
    class Meta:
        verbose_name = _('ban')
        verbose_name_plural = _('Bans')
        unique_together = ('is_permanent', 'user')

    reason = models.TextField(blank=True, null=True)
    user = models.ForeignKey(ChatUser, related_name='chat_user')
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_at = models.DateField(blank=True, null=True)
    is_permanent = models.BooleanField(_('Permanent ban'), default=False)
    is_active = models.BooleanField(default=True)

    # managers
    objects = models.Manager()
    active = OnlyActiveManager()

    @classmethod
    def for_time(cls, days=0, weeks=0, months=0, years=0):
        return cls.objects.create(
            expiry_at=timezone.now().date() + relativedelta(
                days=days, weeks=weeks, months=months, years=years))

    @property
    def duration(self):
        if self.expiry_at:
            return str(self.expiry_at - self.created_at.date())
        return None

    @property
    def remaining_time(self):
        if self.expiry_at and self.expiry_at > timezone.now().date():
            return str(self.expiry_at - timezone.now().date())
        return 0

    def save(self, *args, **kwargs):
        self.user.is_active = False
        super(UserBan, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.reason

