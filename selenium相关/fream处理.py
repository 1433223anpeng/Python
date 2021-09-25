from selenium.webdriver import Chrome
import time


url = "http://www.wbdy.tv/play/43938_1_1.html"

web = Chrome()

web.get(url)



#切换到  //*[@id="mplay"]
fr = web.find_element_by_xpath('//*[@id="mplay"]')
web.switch_to.frame(fr)

#找到frame里面的某个元素
x = web.find_element_by_xpath('./html/body/div/div[4]/div[1]/input')
print(x.get_property('placeholder'))

#切出去
web.switch_to.parent_frame()
y = web.find_element_by_xpath('/html/body/div[2]/div[3]/div[2]/div/div[2]')
print(y.text)

web.quit()