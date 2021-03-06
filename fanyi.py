#!/usr/bin/python3

import requests
import re
import js2py
import sys
import os

js = r"""
function n(r, o) {
    for (var t = 0; t < o.length - 2; t += 3) {
    var a = o.charAt(t + 2);
    a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a), a = "+" === o.charAt(t + 1) ? r >>> a : r << a, r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a
    }
    return r
}
function e(r) {
    var o = r.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g);
    if (null === o) {
        var t = r.length;
        t > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(t / 2) - 5, 10) + r.substr(-10, 10))
    } else {
        for (var e = r.split(/[\uD800-\uDBFF][\uDC00-\uDFFF]/), C = 0, h = e.length, f = []; h > C; C++) "" !== e[C] && f.push.apply(f, a(e[C].split(""))), C !== h - 1 && f.push(o[C]);
        var g = f.length;
        g > 30 && (r = f.slice(0, 10).join("") + f.slice(Math.floor(g / 2) - 5, Math.floor(g / 2) + 5).join("") + f.slice(-10).join(""))
    }
    var u = void 0, l = "" + String.fromCharCode(103) + String.fromCharCode(116) + String.fromCharCode(107);
    u = "gtk";
    for (var d = u.split("."), m = Number(d[0]) || 0, s = Number(d[1]) || 0, S = [], c = 0, v = 0; v < r.length; v++) {
        var A = r.charCodeAt(v);
        128 > A ? S[c++] = A : (2048 > A ? S[c++] = A >> 6 | 192 : (55296 === (64512 & A) && v + 1 < r.length && 56320 === (64512 & r.charCodeAt(v + 1)) ? (A = 65536 + ((1023 & A) << 10) + (1023 & r.charCodeAt(++v)), S[c++] = A >> 18 | 240, S[c++] = A >> 12 & 63 | 128) : S[c++] = A >> 12 | 224, S[c++] = A >> 6 & 63 | 128), S[c++] = 63 & A | 128)
    }
    for (var p = m, F = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(97) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(54)), D = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(51) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(98)) + ("" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(102)), b = 0; b < S.length; b++) p += S[b], p = n(p, F);
    return p = n(p, D), p ^= s, 0 > p && (p = (2147483647 & p) + 2147483648), p %= 1e6, p.toString() + "." + (p ^ m)
}
"""

class BaiduFanyi(object):
    def __init__(self,content):
        self.content = content#??????
        self.session = requests.session()
        self.headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36",
        'origin': 'https://fanyi.baidu.com',
        # 'referer': 'https://fanyi.baidu.com/?aldtype=16047'
        }
        self.session.headers = self.headers
        self.url_read = 'https://fanyi.baidu.com/gettts'#??????uel
        self.url_root = 'http://fanyi.baidu.com/'  # ?????????url
        self.url_langdetect = 'https://fanyi.baidu.com/langdetect'  # ????????????url
        self.url_trans = 'https://fanyi.baidu.com/v2transapi'  # ????????????url
        self.context = js2py.EvalJs()# ????????????js?????????
        self.landata = {
            "query":self.content
        }

    def get_token_gtk(self):
        try:
            r = self.session.get(self.url_root)
            r_str = r.content.decode()
            token = re.findall(r"token: '(.*?)'", r_str)[0]
            gtk = re.findall(r";window.gtk = ('.*?');", r_str)[0]
            return token,gtk
        except :
            return 0,0

    def lan(self):
        try :
            r = self.session.post(self.url_langdetect,self.landata)
            return r.json()['lan']
        except:
            return 0

    def fanyi(self):
        global js
        try:
            lan = self.lan()#?????????token???????????????????????????
            if lan ==0 :
                raise Exception("?????????????????????")
            token,gtk = self.get_token_gtk()#??????token??????gtk
            if token == 0 or gtk ==0 :
                raise Exception("token???gtk??????")
            self.context.execute(js)# ??????????????????e(r),???keywords????????????
            sign = self.context.e(self.content)
            data = {
                    'from': lan,
                    'to': 'en' if lan == 'zh' else 'zh',
                    'query': self.content,
                    'transtype': 'translang',
                    'simple_means_flag': 3,
                    'sign': sign,  # ??????????????????
                    'token': token  # ??????????????????

            }
            r = self.session.post(self.url_trans,data=data)
            #print(r.status_code)
            if r.status_code != 200:
                raise Exception("???????????????")
            a = ""
            s = r.json()['trans_result']['data']
            for i in s:
                a += i['dst'] + '\n'
            return a
        except Exception as e:
            return e

    def read(self):
        self.url_read
        params = {
            # lan=en&text=World&spd=3&source=web
            'lan' : 'en',
            'text' : self.content,
            'spd' : 3,
            'source' : 'web'
        }
        r = self.session.get(self.url_read,params=params)
        if r.status_code != 200:
            raise Exception("???????????????")
        elif r.status_code == 200:
            with open('read.mp3','wb') as f:
                f.write(r.content)
            os.system("cvlc read.mp3 --play-and-exit 2>1 1>/dev/null &")
        else :
            raise Exception("???????????????")


def help():
    print(r"""
?????????
???????????????????????????????????????????????????
fanyi and
fanyi "and or"
fanyi -r    ?????????????????????
echo "and\nor"|fanyi	#??????????????????????????????????????????

****|fanyi -i			#?????????????????????????????????????????????
						??????????????????????????????????????????????????????5000????????????
						(?????????????????????????????????????????????)
????????????????????????????????????????????????5000???
        """
    )

if __name__ == "__main__":
    if len(sys.argv) == 1:
        stdin_list = sys.stdin.readlines()
        #print(stdin_list)
        content = "".join(stdin_list)
        print(BaiduFanyi(content).fanyi())
    elif ("-h" or "--help") in (sys.argv):
        help()
    elif "-i" in (sys.argv):
        a = sys.stdin.readlines()
        c = 0
        index = 0
        for i in a:
            c += len(i)
            if c > 4000:
                print(BaiduFanyi("".join(a[index:a.index(i,index+1)])).fanyi())
                c = 0
                index = a.index(i,index+1)
            elif len(a) == a.index(i) + 1:
                print(BaiduFanyi("".join(a[index:])).fanyi())
    elif '-r' in (sys.argv):
        arg = sys.argv[-1]
        # print(arg)
        # print(type(arg))
        a = BaiduFanyi(arg)
        print(a.fanyi())
        a.read()
    else :
        arg = sys.argv[1:]
        #print(arg)
        content = ",".join(arg)
        #print(content)
        print(BaiduFanyi(content).fanyi())
