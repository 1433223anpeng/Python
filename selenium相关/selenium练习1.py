


from selenium.webdriver import Chrome

web = Chrome()

url = "https://www.baidu.com"

web.get(url)

print(web.title)