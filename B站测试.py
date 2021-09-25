import requests
import os

url = "https://www.bilibili.com/video/BV1xM4y137or"



U_A = {
    "range": "bytes=0-",
    "referer": "https://www.bilibili.com/video/BV1xM4y137or",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36",
}

#r = requests.get('https://xy120x193x190x217xy.mcdn.bilivideo.cn:4483/upgcxcode/06/05/413200506/413200506-1-30033.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1632495845&gen=playurlv2&os=mcdn&oi=1865698326&trid=00017084564dcde74b4097ba5fa80b20a4d5u&platform=pc&upsig=9a2e2ed692f3bb294aafe0e16aae67cf&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mcdnid=8000394&mid=0&bvc=vod&nettype=0&orderid=0,3&agrr=0&logo=A0000080',headers=U_A)
#r = requests.options('https://xy120x193x190x217xy.mcdn.bilivideo.cn:4483/upgcxcode/06/05/413200506/413200506-1-30033.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1632495845&gen=playurlv2&os=mcdn&oi=1865698326&trid=00017084564dcde74b4097ba5fa80b20a4d5u&platform=pc&upsig=9a2e2ed692f3bb294aafe0e16aae67cf&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mcdnid=8000394&mid=0&bvc=vod&nettype=0&orderid=0,3&agrr=0&logo=A0000080',headers=U_A)

#r = requests.get("https://xy39x153x132x15xy.mcdn.bilivideo.cn:4483/upgcxcode/06/05/413200506/413200506_nb2-1-30032.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1632412150&gen=playurlv2&os=mcdn&oi=2026927756&trid=00017149c5e372c5441f9be747d93fc4a327u&platform=pc&upsig=0e1eafa14dd76bb890f723623f55849e&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mcdnid=8000049&mid=0&bvc=vod&nettype=0&orderid=0,3&agrr=0&logo=A0000080",headers=U_A)


print(r)

with open("4443.m4s",'wb') as f:
    f.write(r.content)
