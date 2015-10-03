# -*- coding: utf-8 -*-
import sys
import os, sys, urllib, requests
from bs4 import BeautifulSoup
from WebQQ import WebQQ

# import sys
# sys.getdefaultencoding('utf-8')


def search(s):
    try:
        d = requests.get(u'http://cn.bing.com/search?q=%s' % unicode(s)).text
    except Exception, e:
        d = requests.get(u'http://cn.bing.com/search?q=%s'.encode('utf-8') % s).text
    s1 = BeautifulSoup(d, "html.parser")
    return s1.p.text.encode('utf-8')



def group_message_hook(msg):
    value = msg[u'value']
    content = value[u'content'][1]
    group_id = value[u'info_seq']
    # speaker_id =
    try:
        print unicode(group_id) + u" : " + unicode(content)
        if int(group_id) == 384350610 or int(group_id) == 2931677874:
            content = content.encode('utf-8')
            # if content.startswith('?'):
            print '############'
            # w.send_group_msg_d(2931677874, u'Message received :' + unicode(content))
            print content[0]
            if content[0] == '?'.encode('utf-8') or content[0] == '?'.encode('utf-8'):
                w.send_group_msg_d(2931677874, u"命中: ".encode('utf-8') + content[1:])
                r = search(content)
                a = u'自动搜索结果(%s): %s'.encode('utf-8') % (content[1:], r)
                w.send_group_msg_d(2931677874, a)

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
    #    print 'OK'
    # except Exception, e:
    #    print e
# vim: tabstop=2 softtabstop=2 shiftwidth=2 expandtab
