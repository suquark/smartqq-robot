# -*- coding: utf-8 -*-

from HttpClient import HttpClient
import re, random, md5, json, os, sys, datetime, time, thread, subprocess, logging
import requests

class WebQQ(HttpClient):
    channel = 'http://d.web2.qq.com/channel/'
    send_qun = channel + 'send_qun_msg2'
    poll2 = channel + 'poll2'

    group_msg_hook = None
    poll_msg_hook = None
    ClientID = int(random.uniform(111111, 888888))
    APPID = 0
    FriendList = {}
    MaxTryTime = 5
    PSessionID = ''
    Referer = 'http://d.web2.qq.com/proxy.html?v=20130916001&callback=1&id=2'
    SmartQQUrl = 'http://w.qq.com/login.html'

    def __init__(self, vpath, qq=0):
        self.VPath = vpath  # QRCode保存路径
        self.AdminQQ = int(qq)
        self.VFWebQQ = ''
        logging.basicConfig(filename='qq.log', level=logging.DEBUG,
                            format='%(asctime)s  %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='[%Y-%m-%d %H:%M:%S]')
        self.initUrl = self.getReValue(self.Get(self.SmartQQUrl), r'\.src = "(.+?)"', 'Get Login Url Error.', 1)

        html = self.Get(self.initUrl + '0')

        self.APPID = self.getReValue(html, r'g_appid=encodeURIComponent\("(\d+)"\)', 'Get AppId Error', 1)
        #self.APPID=501004106
        self.html = html
        self.msgId = int(random.uniform(50790000, 60790000))

    def login(self):
        html = self.html
        sign = self.getReValue(html, r'g_login_sig=encodeURIComponent\("(.*?)"\)', 'Get Login Sign Error', 1)
        logging.info('get sign : %s', sign)

        JsVer = self.getReValue(html, r'g_pt_version=encodeURIComponent\("(\d+)"\)', 'Get g_pt_version Error', 1)
        logging.info('get g_pt_version : %s', JsVer)

        MiBaoCss = self.getReValue(html, r'g_mibao_css=encodeURIComponent\("(.+?)"\)', 'Get g_mibao_css Error', 1)
        logging.info('get g_mibao_css : %s', sign)
        StarTime = self.date_to_millis(datetime.datetime.utcnow())
        T = 0
        while True:
            T += 1
            self.Download('https://ssl.ptlogin2.qq.com/ptqrshow?appid={0}&e=0&l=L&s=8&d=72&v=4'.format(self.APPID),
                          self.VPath)
            os.system("open %s" % self.VPath)
            logging.info('[{0}] Get QRCode Picture Success.'.format(T))
            while True:
                html = self.Get(
                    'https://ssl.ptlogin2.qq.com/ptqrlogin?webqq_type=10&remember_uin=1&login2qq=1&aid={0}&u1=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10&ptredirect=0&ptlang=2052&daid=164&from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=0-0-{1}&mibao_css={2}&t=undefined&g=1&js_type=0&js_ver={3}&login_sig={4}'.format(
                        self.APPID, self.date_to_millis(datetime.datetime.utcnow()) - StarTime, MiBaoCss, JsVer, sign),
                    self.initUrl)
                # logging.info(html)
                ret = html.split("'")
                if ret[1] == '65' or ret[1] == '0':  # 65: QRCode 失效, 0: 验证成功, 66: 未失效, 67: 验证中
                    break
                time.sleep(2)
            if ret[1] == '0' or T > self.MaxTryTime:
                break

        logging.debug(ret)
        if ret[1] != '0':
            return

        if os.path.exists(self.VPath):  # 删除QRCode文件
            os.remove(self.VPath)



        html = self.Get(ret[5])
        url = self.getReValue(html, r' src="(.+?)"', 'Get mibao_res Url Error.', 0)
        if url != '':
            html = self.Get(url.replace('&amp;', '&'))
            url = self.getReValue(html, r'location\.href="(.+?)"', 'Get Redirect Url Error', 1)
            html = self.Get(url)
        self.PTWebQQ = self.getCookie('ptwebqq')
        logging.info('PTWebQQ: {0}'.format(self.PTWebQQ))
        print "Successfully login"

    def listen(self):
        while 1:
            html = self.Post('http://d.web2.qq.com/channel/login2', {
                'r': '{{"ptwebqq":"{0}","clientid":{1},"psessionid":"{2}","status":"online"}}'.format(self.PTWebQQ,
                                                                                                      self.ClientID,
                                                                                                      self.PSessionID)
            }, self.Referer)

            logging.debug(html)
            ret = json.loads(html)

            if ret['retcode'] != 0:
                break

            self.VFWebQQ = ret['result']['vfwebqq']
            self.PSessionID = ret['result']['psessionid']

            logging.info('Login success')

            #  self.msgID = int(random.uniform(20000, 50000))

            E = 0
            while True:

                html = self.Post('http://d.web2.qq.com/channel/poll2', {
                    'r': '{{"ptwebqq":"{1}","clientid":{2},"psessionid":"{0}","key":""}}'.format(self.PSessionID,
                                                                                                 self.PTWebQQ,
                                                                                                 self.ClientID)
                }, self.Referer)

                # 超时时会返回空, 所以此处如果是空, 则继续发出请求, 不用往后走下去
                if html == '':
                    continue

                logging.info(html)

                # self.send_group_msg_d(2931677874, '......')  # 384350610
                if self.poll_msg_hook:
                    self.poll_msg_hook()

                try:
                    ret = json.loads(html)
                    E = 0
                except ValueError as e:
                    logging.debug(e)
                    E += 1
                except Exception as e:
                    logging.debug(e)
                    E += 1

                if E > 0 and E < 5:
                    time.sleep(2)
                    continue

                if E > 0:
                    logging.debug('try auto login ...')
                    break

                if ret['retcode'] == 100006:
                    break
                elif ret['retcode'] == 102:  # 无消息
                    pass
                elif ret['retcode'] == 116:  # 更新PTWebQQ值
                    self.PTWebQQ = ret['p']
                elif ret['retcode'] == 0:
                    for msg in ret['result']:
                        msgType = msg['poll_type']
                        if msgType == 'message':  # QQ消息
                            txt = msg['value']['content'][1]
                            logging.debug(txt)
                            tuin = msg['value']['from_uin']
                            if not tuin in self.FriendList:  # 如果消息的发送者的真实QQ号码不在FriendList中,则自动去取得真实的QQ号码并保存到缓存中
                                try:
                                    info = json.loads(self.Get(
                                        'http://s.web2.qq.com/api/get_friend_uin2?tuin={0}&type=1&vfwebqq={1}'.format(
                                            tuin, self.VFWebQQ), self.Referer))
                                    logging.info(info)
                                    if info['retcode'] != 0:
                                        raise ValueError, info
                                    info = info['result']
                                    self.FriendList[tuin] = info['account']
                                except Exception as e:
                                    logging.debug(e)
                                    continue
                            if self.FriendList.get(tuin, 0) != self.AdminQQ:  # 如果消息的发送者与AdminQQ不相同,则忽略本条消息不往下继续执行
                                continue
                            if txt[0] == '#':
                                thread.start_new_thread(self.runCommand, (tuin, txt[1:].strip(), msgId))
                                self.msgId += 1
                            if txt[0:4] == 'exit':
                                logging.info(self.Get(
                                    'http://d.web2.qq.com/channel/logout2?ids=&clientid={0}&psessionid={1}'.format(
                                        self.ClientID, self.PSessionID), self.Referer))
                                exit(0)
                        elif msgType == 'sess_message':  # QQ临时会话的消息
                            logging.debug(msg['value']['content'][1])
                        elif msgType == 'group_message':  # 群消息
                            if self.group_msg_hook:
                                self.group_msg_hook(msg)
                            txt = msg[u'value'][u'content'][1]
                            logging.debug("QQGroup Message:" + json.dumps(txt))
                        elif msgType == 'discu_message':  # 讨论组的消息
                            txt = msg['value']['content'][1]
                            logging.debug("Discu Message:" + txt)
                        elif msgType == 'kick_message':  # QQ号在另一个地方登陆,被挤下线
                            logging.error(msg['value']['reason'])
                            raise Exception, msg['value']['reason']  # 抛出异常,重新启动WebQQ,需重新扫描QRCode来完成登陆
                            break
                        elif msgType != 'input_notify':
                            logging.debug(msg)

    def send_group_msg_d(self, group_uin, msg):
        self.msgId += 1
        reqURL = "http://d.web2.qq.com/channel/send_qun_msg2"
        data = {
            'r'.encode('utf-8'):'{"group_uin":"%d", "face":588,"content":"[\\\"%s\\\"]","clientid":%d, "msg_id":%d,"psessionid":"%s"}'.encode('utf-8') %
                (group_uin, msg.replace("\\", "\\\\\\\\"), self.ClientID, self.msgId, self.PSessionID.encode('utf-8'))}




        print data
        rsp = self.Post(reqURL, data, self.Referer)
        print rsp

    def send_group_msg(self, group_uin, msg):
        content = '[\\"%s\\"]' % msg
        data = 'r={"group_uin":%d,"content":"%s","clientid":%d,"psessionid":"%s"}' % \
               (group_uin, content, int(self.ClientID), self.PSessionID)
        r = self.post_msg(self.send_qun, {'Referer': 'http://d.web2.qq.com'}, data)
        print r
        logging.debug(r)
        return r

    def runCommand(self, fuin, cmd, msgId):
        ret = 'Run Command: [{0}]\n'.format(cmd)
        try:
            popen_obj = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0)
            (stdout, stderr) = popen_obj.communicate()

            ret += stdout.strip()
            ret += '\n' + stderr.strip()
        except Exception, e:
            ret += e

        logging.info(ret)

        ret = ret.replace('\\', '\\\\\\\\').replace('\t', '\\\\t').replace('\r', '\\\\r').replace('\n', '\\\\n')
        ret = ret.replace('"', '\\\\\\"')
        self.Post("http://d.web2.qq.com/channel/send_buddy_msg2", (
            ('r',
             '{{"to":{0},"face":567,"content":"[\\"{4}\\",[\\"font\\",{{\\"name\\":\\"Arial\\",\\"size\\":\\"10\\",\\"style\\":[0,0,0],\\"color\\":\\"000000\\"}}]]","msg_id":{1},"clientid":"{2}","psessionid":"{3}"}}'.format(
                 fuin, msgId, self.ClientID, self.PSessionID, ret)),
            ('clientid', self.ClientID),
            ('psessionid', self.PSessionID)
        ), self.Referer)

    def getReValue(self, html, rex, er, ex):
        v = re.search(rex, html)
        if v is None:  # 如果匹配失败
            logging.error(er)  # 记录错误
            if ex:  # 如果条件成立,则抛异常
                raise Exception, er
            return ''
        return v.group(1)  # 返回匹配到的内容

    def date_to_millis(self, d):
        return int(time.mktime(d.timetuple())) * 1000


if __name__ == "__main__":
    vpath = './v.jpg'
    qq = 0
    if len(sys.argv) > 1:
        vpath = sys.argv[1]
    if len(sys.argv) > 2:
        qq = sys.argv[2]
    # while True:
        # try:
    WebQQ(vpath, qq)
        #    print 'OK'
        # except Exception, e:
        #    print e
# vim: tabstop=2 softtabstop=2 shiftwidth=2 expandtab
