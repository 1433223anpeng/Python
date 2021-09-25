from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
import time

#添加无头配置
opt = Options()
opt.add_argument("--headless")
opt.add_argument("--disable-gpu")

web = Chrome(options=opt)

web.get("https://www.endata.com.cn/BoxOffice/BO/Year/index.html")

se = web.find_element_by_xpath('//*[@id="OptionDate"]')

sel_new = Select(se)

print(len(sel_new.options))

for i in range(len(sel_new.options)):
    sel_new.select_by_index(i)
    time.sleep(3)
    trs = web.find_elements_by_xpath('/html/body/section[1]/div/div[2]/div/div/div[2]/table/tbody')
    for tr in trs:
        print(tr.text)