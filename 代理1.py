import requests

proxy = {
    "http":"http://222.74.202.229:8080",
    "https":"https://222.74.202.229:8080"
}
#reuqest代理
# r = requests.get("http://www.httpbin.org/get",proxies=proxy)


#session代理
s = requests.session()
s.proxies.update(proxy)
r = s.get("http://www.httpbin.org/get")
print(r.text)