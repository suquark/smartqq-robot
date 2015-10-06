__author__ = 'suquark'
import requests
from bs4 import BeautifulSoup


def Search(s):
    try:
        s = s.encode('utf-8')
    except Exception, e:
        pass
    try:
        html_text = requests.get('http://cn.bing.com/search?q=' + s).text
        html_data = BeautifulSoup(html_text, "html.parser")
        return html_data.p.text.encode('utf-8')
    except Exception, e:
        return 'Invalid search'


def Servoctl(s):
    # TODO make it safe
    requests.get('http://192.168.43.206/servoctl/' + s)
