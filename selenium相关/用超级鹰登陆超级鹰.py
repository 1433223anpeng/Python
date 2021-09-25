from selenium.webdriver import Chrome
from chaojiying import Chaojiying_Client

url = "http://www.chaojiying.com/user/login/"

web = Chrome()

web.get(url)

png = web.find_element_by_xpath("/html/body/div[3]/div/div[3]/div[1]/form/div/img").screenshot_as_png

chaojiying = Chaojiying_Client('', '', '')	#用户中心>>软件ID 生成一个替换 96001
v_code = chaojiying.PostPic(png, 1902)['pic_str']

web.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[1]/form/p[1]/input').send_keys("18614075987")
web.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[1]/form/p[2]/input').send_keys('q6035945')
web.find_element_by_xpath("/html/body/div[3]/div/div[3]/div[1]/form/p[3]/input").send_keys(v_code)
web.find_element_by_xpath("/html/body/div[3]/div/div[3]/div[1]/form/p[4]/input").click()
