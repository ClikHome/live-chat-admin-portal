from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from datetime import datetime
import json

from channels.models import Channel
from users.models import ChatUser
from LiveChatBackend.managers import OnlyActiveManager


class Message(models.Model):
    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('Messages')
        ordering = ('-created_at',)

    body = models.TextField(_('Body'), )
    channel = models.ForeignKey(Channel, related_name='chat')
    user = models.ForeignKey(ChatUser, related_name='sender')

    created_at = models.DateTimeField()  # Remove auto_now_add
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    # managers
    objects = models.Manager()
    active = OnlyActiveManager()

    @classmethod
    def from_json(cls, data):
        if isinstance(data, (unicode, str)):
            data = json.loads(data)
        elif not isinstance(data, dict):
            raise TypeError

        def get_datetime(datetime_str):
            return datetime.strptime(
                datetime_str, settings.MESSAGES_DATETIME_FORMAT)

        try:
            user = ChatUser.active.get(username=data['username'])

        # Not Found
        except ChatUser.DoesNotExist:
            return None

        return cls(
            body=data['body'],
            channel_id=int(data['channel_id']),
            user=user,
            created_at=get_datetime(data['created_at']),
            is_active=True
        )

    def save(self, *args, **kwargs):
        super(Message, self).save(*args, **kwargs)

        message_user = self.user
        message_user.last_activity = self.created_at
        message_user.save()

    def __unicode__(self):
        return self.body


# class StopWordsAction(models.Model):
#     title = models.CharField(max_length=50)
#     description = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __unicode__(self):
#         return self.title


class StopWord(models.Model):
    body = models.CharField(max_length=100)
    channel = models.ForeignKey(Channel, related_name='channel_stop_word')
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.body
