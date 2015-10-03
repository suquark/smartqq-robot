#!/usr/bin/env python
#
import os,sys,urllib
from bs4 import BeautifulSoup
import mma,py,sh,c
def search(s):
 if s[0]!='=' and s[0]!='?' and s[0]!='@' and s[0]!='>' and s[0]!='$' and s[0]!='#':
  return ''
 f=open("FL","r")
 d=f.read()
 f.close()
 d=d.split('\n')
 for i in d:
  if (s.find(i)!=-1) and (i!=''):
   return 'ERROR:'+i
 d=s[0]
 s=s[1:]
 if d=='?':
  d=urllib.urlopen('http://cn.bing.com/search?q=%s'%(s,)).read()
  s=BeautifulSoup(d)
  return s.p.text.encode('utf8')
 elif d=='#':
  ans = reload(c).doer(s)
  return urllib.quote(repr(repr(ans)[1:-1])[1:-1])
 elif d=='=':
  ans = reload(mma).doer(s)
  return urllib.quote(repr(repr(ans)[1:-1])[1:-1])
 elif d=='>':
  ans = reload(py).doer(s)
  return urllib.quote(repr(repr(ans)[1:-1])[1:-1])
 elif d=='$':
  ans = reload(sh).doer(s)
  return urllib.quote(repr(repr(ans)[1:-1])[1:-1])
 elif d=='@':
  p=s.find(' ')
  if p!=-1:
   s=s[:p]
  return "%s is a doubi!"%(s,)
 else:
  return ''
if __name__ == "__main__":
 print search(sys.argv[1])
