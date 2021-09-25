from selenium.webdriver import Chrome

from selenium.webdriver import ActionChains

browser = Chrome()
browser.get("https://www.runoob.com/try/try-cdnjs.php?filename=jqueryui-api-droppable")

fr = browser.find_element_by_xpath('//*[@id="iframeResult"]')
browser.switch_to.frame(fr)

s = browser.find_element_by_css_selector("#draggable")
t = browser.find_element_by_css_selector("#droppable")

action = ActionChains(browser)

action.drag_and_drop(s,t)
action.perform()

browser.quit()