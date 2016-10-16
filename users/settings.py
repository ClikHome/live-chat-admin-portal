#!/usr/bin/env python
# -*- coding: utf-8 -*-

ROLE_CHOICES = (
        ('admin', _('Admin')),
        ('moderator', _('Moderator')),
        ('user', _('User')),
        ('read-only', _('Read only'))
    )

ROLES = (
    #   Admin
    ('change_roles', 'Can change roles'),
    ('perm_ban_to_user', 'Can give bane to user for all time'),
    ('ban_by_ip', 'Can get ban by IP'),
    ('remove_all_messages_of_user', 'Can remove all messages in the chat of user'),
    ('', ''),


    #   Moderator
    ('ban_to_user_for_time', 'Can get ban to user for some time'),
    ('delete_messages', 'Can delete messages'),
    ('add_stop_words', 'Can add stop words'),
    ('', ''),
)

TIME_OF_BAN = (
    (1/6, '10 minutes'),
    (1, 'one hour'),
    (24, 'one day'),
    (24 * 7, 'one week'),
    (24 * 30, 'one month'),
)