# -*- coding: utf-8 -*-

"""
curl 'http://d.web2.qq.com/channel/send_qun_msg2' -H 'Referer: http://d.web2.qq.com' -H 'Cookie: p_uin=o2980412917; p_skey=JmZsMKhOh*Mc3W0pVngGB7vy0tltEWWnl52YpQ8XY6M_; uin=o2980412917; skey=@PtCIUVqS4;' --data 'r={"group_uin":285293966,"content":"[\"。。。。。。。\"]","face":588,"clientid":53999199,"psessionid":"8368046764001d636f6e6e7365727665725f77656271714031302e3133392e372e31363400002b9d00001550016e0400f57da5b16d0000000a405074434955567153346d000000287dfc8fd811d9185d84060056adc0d7bc7b9f7328345bd285055c90e7ba3ea14323d3b53c0e8e8e29"}'
curl 'http://d.web2.qq.com/channel/poll2' -H 'Referer: http://d.web2.qq.com' -H 
'Cookie: p_uin=o2980412917; p_skey=JmZsMKhOh*Mc3W0pVngGB7vy0tltEWWnl52YpQ8XY6M_; uin=o2980412917; skey=@PtCIUVqS4;' 
--data 'r={"ptwebqq":"e0fcaa3fd5e6cce695161ae64574f38c07c713d0c41da720bb44f01102989f14","clientid":53999199,"psessionid":"8368046764001d636f6e6e7365727665725f77656271714031302e3133392e372e31363400002b9d00001550016e0400f57da5b16d0000000a405074434955567153346d000000287dfc8fd811d9185d84060056adc0d7bc7b9f7328345bd285055c90e7ba3ea14323d3b53c0e8e8e29","key":""}'

curl 'http://d.web2.qq.com/channel/send_qun_msg2' -H 'Origin: http://d.web2.qq.com' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Accept: */*' -H 'Referer: http://d.web2.qq.com/proxy.html?v=20130916001&callback=1&id=2' -H 'Cookie: pgv_pvi=175453184; RK=sdHuuQHJu1; ptcz=a829f57f4db9707f0b1bdc4d9e1bc8a65cd658f2e23a17245b75af952261d5b6; verifysession=h01760423c9992c09d9a7a95bb7bd26d0130eb9d5b995abbd4d3523d8f3342b189903080bfa8b09af2b; FTN5K=29451997; ts_refer=www.google.com/; ts_uid=6973411104; pt_clientip=d0b37f00000130d7; pt_serverip=dadd0af1716429d3; ptisp=os; pt2gguin=o2980412917; uin=o2980412917; skey=@uugokxneq; p_uin=o2980412917; p_skey=T6X6zbrZClLZbTG4A98kt0R6H0I*1DCdZQojMLMC0Zo_; pt4_token=sAxrup9rKrE7H89D4fgIxA__; pgv_info=ssid=s2258016895; pgv_pvid=1159463035; o_cookie=2980412917; ptwebqq=abc4a8046c9daa52e984c2b97ccee4b7a395a4ee5e4ce9cdeeb280322bdac99b' -H 'Connection: keep-alive' --data 'r=%7B%22group_uin%22%3A2344029517%2C%22content%22%3A%22%5B%5C%22%E5%8F%8D%E6%AD%A3MIT%20%2450%20billion%5C%22%2C%5B%5C%22font%5C%22%2C%7B%5C%22name%5C%22%3A%5C%22%E5%AE%8B%E4%BD%93%5C%22%2C%5C%22size%5C%22%3A10%2C%5C%22style%5C%22%3A%5B0%2C0%2C0%5D%2C%5C%22color%5C%22%3A%5C%22000000%5C%22%7D%5D%5D%22%2C%22face%22%3A588%2C%22clientid%22%3A53999199%2C%22msg_id%22%3A33340006%2C%22psessionid%22%3A%228368046764001d636f6e6e7365727665725f77656271714031302e3133392e372e31363400000223000015b1016e0400f57da5b16d0000000a407575676f6b786e65716d00000028f65db4586b304318ee1c6afd553d4353ef998380c39695c4df6e3bbedadc3f8b2fa4afabe484a886%22%7D' --compressed
"""

import requests

channel = 'http://d.web2.qq.com/channel/'
send_qun = channel + 'send_qun_msg2'
poll2 = channel + 'poll2'


class SmartQQ():
    @staticmethod
    def gen_content_msg(msg):
        return '[\\"%s\\"]' % (msg)

    @property
    def cookies(self):
        quin = 'o' + str(self.uin)
        return {'uin': quin, 'p_uin': quin, 'skey': self.skey, 'p_skey': self.p_skey}

    def gen_data_send(self, content):
        return 'r={"group_uin":%d,"content":"%s","clientid":53999199,"psessionid":"%s"}' % (
        self.group_uin, content, self.psessionid)

    @property
    def header(self):
        headers = {'Referer': 'http://d.web2.qq.com'}
        return headers

    def post(self, url, data):
        print self.gen_data_send(data)
        print url
        r = requests.get(url, data=self.gen_data_send(data), headers=self.header, cookies=self.cookies)
        print r.text

    def send_msg(self, content):
        self.post(send_qun, self.gen_content_msg(content))

    def __init__(self, uin, group_uin, psessionid, skey, p_skey):
        self.uin = uin
        self.group_uin = group_uin
        self.psessionid = psessionid
        self.skey = skey
        self.p_skey = p_skey


smq = SmartQQ(2980412917, 304046810,
              '8368046764001d636f6e6e7365727665725f77656271714031302e3133392e372e313634000030f2000015b4016e0400f57da5b16d0000000a405473335a39364748706d00000028ab755e528064faba1c16f4c212f64061757c7710a212a8b31c2f4016a3ecd9851391c00958427de1',
              '@Ts3Z96GHp', 'eGBcqaGWu3pRYyrf8r8pJSmwA-iBAtf9o8Gacpgah4g_')

smq.send_msg('adfghjkl')
