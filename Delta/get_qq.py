#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os,simplejson,sys,threading
import do_search,send_message
def sender(s):
 return lambda : reload(send_message).send(reload(do_search).search(s.encode('utf8')))
s="curl 'http://d.web2.qq.com/channel/poll2' -H 'Origin: http://d.web2.qq.com' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Accept: */*' -H 'Referer: http://d.web2.qq.com/proxy.html?v=20130916001&callback=1&id=2' -H 'Cookie: RK=N1t/C54NHp; ts_refer=www.qplus.com/productForWeb.shtml; ts_last=web2.qq.com/; ts_uid=8522433757; pt_clientip=7d187f000001edbc; pt_serverip=b8270abf06626050; ptisp=edu; pt2gguin=o3157282269; uin=o3157282269; skey=@xowHvFcfQ; p_uin=o3157282269; p_skey=4PxF8FRuHuVzRATODFWaBwv9JcSi93PHlcf2KHxH3kk_; pt4_token=GzzJFYM-sCznn6HAimRehQ__; pgv_info=ssid=s43371068; pgv_pvid=3842234142; o_cookie=3157282269; ptwebqq=c2e021a1fe2304d77002982c3c03205e1ae5dc3612977328a079584e5dd00872' -H 'Connection: keep-alive' --data 'r=%7B%22ptwebqq%22%3A%22c2e021a1fe2304d77002982c3c03205e1ae5dc3612977328a079584e5dd00872%22%2C%22clientid%22%3A53999199%2C%22psessionid%22%3A%228368046764001d636f6e6e7365727665725f77656271714031302e3133392e372e31363400007745000012ad016e0400dd4d30bc6d0000000a40786f774876466366516d000000286509dadafdd2a1cec410420b19233e5569454008d3957a3aef0a099b726b63875e2d820bd41ae4cf%22%2C%22key%22%3A%22%22%7D' --compressed"
p=os.pipe()
while True:
 if os.system("%s -m 5 1>/proc/%d/fd/%d 2>/dev/null"%(s,os.getpid(),p[1]))!=0:
  continue
 f=open("/proc/%d/fd/%d"%(os.getpid(),p[0]),"r")
 d=f.readline()
 f.close()
 try:
  data=simplejson.loads(d)
  poll=data['result']
 except:
  print "error"
  continue
 for i in poll:
  #print i
  try:
   if i["poll_type"]=="group_message":
    i['value']['content'][1]=unicode(i['value']['content'][1])
    print "%s : %d :%d : %s"%(i["poll_type"],i['value']['info_seq'],i['value']['send_uin'],i['value']['content'][1].encode('utf8'))
    ##
    if i['value']['info_seq']==104157227:
     thr=threading.Thread(target=sender(i['value']['content'][1]))
     thr.start()
    ##
   elif i["poll_type"]=="message":
    i['value']['content'][1]=unicode(i['value']['content'][1])
    print "%s : %d : %s"%(i["poll_type"],i['value']['from_uin'],i['value']['content'][1].encode('utf8'))
   elif i["poll_type"]=="buddies_status_change":
    pass
  except TypeError:
   print "ERROR OCCUR"
   print i
