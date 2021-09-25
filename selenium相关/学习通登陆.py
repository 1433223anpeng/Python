import time

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import  Keys


web = Chrome()

web.get("http://passport2.chaoxing.com/login?fid=&newversion=true&refer=http%3A%2F%2Fi.chaoxing.com")


web.find_element_by_xpath('//*[@id="phone"]').send_keys('')
web.find_element_by_xpath('//*[@id="pwd"]').send_keys('',Keys.ENTER)




time.sleep(5)
web.quit()