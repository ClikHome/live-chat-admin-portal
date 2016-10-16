#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from datetime import datetime

from zero_mq import *
from messages.models import Message
from users.models import ChatUser


def set(message):
    print 'Got message: ' + str(message)
    message = json.loads(message)
    data, data_type = message['data'], message['data_type']

    if data_type == 'message' and all(data.values()):
        new_message = Message.from_json(data)
        new_message.save()

        print 'Message was saved'

    elif data_type == 'user':
        check_user = ChatUser.active.filter(
            channel_id=int(data['channel_id']),
            username=data['username']
        )

        if not check_user:
            new_user = ChatUser.from_json(data)
            new_user.save()

            print 'User was saved'
            return

        print 'User already exist'

