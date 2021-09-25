#目标 拉勾网

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
import time

url  = "https://lagou.com"

web = Chrome()
web.get(url)

#找x号，点击，
x = web.find_element_by_xpath('//*[@id="cboxClose"]')
x.click()


#找到输入的框，输入
time.sleep(1)


#找到输入的地方 输入Python 和回车
web.find_element_by_xpath('//*[@id="search_input"]').send_keys("python",Keys.ENTER)

time.sleep(2)


#用js代码删掉广告
web.execute_script("""
    var a = document.getElementsByClassName("un-login-banner")[0];
    a.parentNode.removeChild(a);

    var b = document.getElementsByClassName("share-app-download-wrap login-close-container init-show-share")[0];
    b.parentNode.removeChild(b);

""")

#找到所有li标签
ul = web.find_elements_by_xpath('//*[@id="s_position_list"]/ul/li')

for li in ul:#循环出每个li标签
    h3 = li.find_element_by_xpath('./div[1]/div[1]/div[1]/a/h3')
    h3.click()#点击
    web.switch_to_window(web.window_handles[-1])#切换标签页，
    job = web.find_element_by_xpath('//*[@id="job_detail"]/dd[2]/div')#找到job元素
    print(job.text)
    print('='*40)
    time.sleep(2)
    web.close()#关闭当前标签
    web.switch_to_window(web.window_handles[-1])#切换到第一个标签

web.quit()
