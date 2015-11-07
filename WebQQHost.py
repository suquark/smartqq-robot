# -*- coding: utf-8 -*-
import sys
import os, sys, urllib, requests

from WebQQ import WebQQ
from robot_handler import *
# import sys
# sys.getdefaultencoding('utf-8')




"""

ha 群 487472872
robogame 459402307

"""


def group_message_hook(msg):
    print "..."
    group_id = int(msg['value']['info_seq'])
    try:
        if group_id == 344123287 or group_id == 384350610:
            do_search(w, msg)
        elif group_id == 459402307:
            do_search(w, msg)
            do_action(msg)
    except Exception, e:
        print e.message


def poll_msg_hook():
    return None

if __name__ == "__main__":
    vpath = './v.jpg'
    qq = 0
    if len(sys.argv) > 1:
        vpath = sys.argv[1]
    if len(sys.argv) > 2:
        qq = sys.argv[2]
        # while True:
        # try:
    w = WebQQ(vpath, qq)
    w.group_msg_hook = group_message_hook
    w.poll_msg_hook = poll_msg_hook
    w.login()
    w.listen()
