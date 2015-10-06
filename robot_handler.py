__author__ = 'suquark'
import Robot_API
import os
import time
import re

def do_action(msg):
    value = msg['value']
    content = value['content'][1].encode('utf-8').strip()
    fpath = 'action/' + content + '.txt'
    print fpath
    if os.path.exists(fpath):
        print 'Go!!!'
        try:
            f = open(fpath)
            data = f.read()
            for line in data.splitlines():
                if line[0] == '#':
                    Robot_API.Servoctl(line.replace('#', '_'))
                    time.sleep(float(re.sub(r'.*T', '', line))/1000.)
        except Exception, e:
            pass


def do_search(w, msg):
    value = msg['value']
    content = value['content'][1].encode('utf-8')
    group_uid = int(value['from_uin'])
    if content[0] == '?':
        r = Robot_API.Search(content[1:])
        a = '(%s): %s' % (content[1:], r)
        w.send_group_msg_d(group_uid, a)