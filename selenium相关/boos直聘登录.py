import time

from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import  ActionChains
import json
import requests


def base64_api( b64, typeid=27,uname='', pwd=''):
    data = {"username": uname, "password": pwd, "typeid": typeid, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]
    return ""

web = Chrome()

web.get("https://login.zhipin.com/?ka=header-login")

web.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/form/div[3]/span[2]/input').send_keys('19834501230')
web.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/form/div[4]/span/input').send_keys('anpeng1314')

web.find_element_by_xpath('//*[@id="pwdVerrifyCode"]').click()

time.sleep(2)

v_code_div = web.find_element_by_xpath('/html/body/div[5]/div[2]/div[1]/div')

b64 = v_code_div.screenshot_as_base64

V_code = base64_api(b64).split('|')

print(V_code)
for z in V_code:
    i = z.split(',')
    x = i[0]
    y = i[1]
    print(x,y)
    ActionChains(web).move_to_element_with_offset(v_code_div,xoffset=int(x),yoffset=int(y)).click().perform()

time.sleep(2)
web.find_element_by_xpath('/html/body/div[5]/div[2]/div[1]/div/div/div[3]/a/div').click()

time.sleep(2)
web.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/form/div[6]/button').click()

time.sleep(5)



