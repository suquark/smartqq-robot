#!/usr/bin/env python
import os,sys,urllib
def send(s):
 if s=='':
  return 0
 if s.find('ERROR')==-1:
  s='ans:%5C%5Cn'+s
 print s
 os.system("curl 'http://d.web2.qq.com/channel/send_qun_msg2' -H 'Origin: http://d.web2.qq.com' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Accept: */*' -H 'Referer: http://d.web2.qq.com/proxy.html?v=20130916001&callback=1&id=2' -H 'Cookie: RK=N1t/C54NHp; ts_refer=www.qplus.com/productForWeb.shtml; ts_last=web2.qq.com/; ts_uid=8522433757; pt_clientip=7d187f000001edbc; pt_serverip=b8270abf06626050; ptisp=edu; pt2gguin=o3157282269; uin=o3157282269; skey=@xowHvFcfQ; p_uin=o3157282269; p_skey=4PxF8FRuHuVzRATODFWaBwv9JcSi93PHlcf2KHxH3kk_; pt4_token=GzzJFYM-sCznn6HAimRehQ__; pgv_info=ssid=s43371068; pgv_pvid=3842234142; o_cookie=3157282269; ptwebqq=c2e021a1fe2304d77002982c3c03205e1ae5dc3612977328a079584e5dd00872' -H 'Connection: keep-alive' --data 'r=%7B%22group_uin%22%3A1858778931%2C%22content%22%3A%22%5B%5C%22"+s+"%5C%22%2C%5B%5C%22font%5C%22%2C%7B%5C%22name%5C%22%3A%5C%22%E5%AE%8B%E4%BD%93%5C%22%2C%5C%22size%5C%22%3A10%2C%5C%22style%5C%22%3A%5B0%2C0%2C0%5D%2C%5C%22color%5C%22%3A%5C%22000000%5C%22%7D%5D%5D%22%2C%22face%22%3A0%2C%22clientid%22%3A53999199%2C%22msg_id%22%3A68600001%2C%22psessionid%22%3A%228368046764001d636f6e6e7365727665725f77656271714031302e3133392e372e31363400007745000012ad016e0400dd4d30bc6d0000000a40786f774876466366516d000000286509dadafdd2a1cec410420b19233e5569454008d3957a3aef0a099b726b63875e2d820bd41ae4cf%22%7D' --compressed")
 return 0
if __name__=="__main__":
 send(sys.argv[1])
