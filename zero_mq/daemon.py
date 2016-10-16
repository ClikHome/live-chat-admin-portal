# !/usr/bin/env python
# -*- coding: utf-8 -*-

import zmq
import time
import logging

from zero_mq.working import set


def main():
    print 'Zero MQ started...'
    context = zmq.Context()

    subscriber = context.socket(zmq.PAIR)
    subscriber.connect("tcp://127.0.0.1:5557")

    while True:
        print 'Waiting message...'
        message = subscriber.recv()
        set(message)


if __name__ == '__main__':
    main()