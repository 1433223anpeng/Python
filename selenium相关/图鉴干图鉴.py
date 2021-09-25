import requests
import json
import time


def base64_api(uname, pwd, img, typeid):
    data = {"username": uname, "password": pwd, "typeid": typeid, "image": img}
    result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]
    return ""

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36"
}

session = requests.session()
session.headers.update(headers)




re1 = session.get('http://admin.ttshitu.com/captcha_v2').json()
print(re1)

V_code = base64_api('','',re1['img'],3)

print(V_code)
data = {
    "captcha": V_code,
    "developerFlag": False,
    "imgId": re1['imgId'],
    "needCheck": True,
    "password": "",
    "userName": "",
}
print(data)
r = session.post('http://admin.ttshitu.com/common/api/login/user',json=data)
print(r.json())


#需要多次才能成功一次






