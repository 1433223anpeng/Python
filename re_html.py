from requests_html import AsyncHTMLSession
import asyncio
import requests
import threading

class A():
    def __init__(self) -> None:
        self.a = 123123123

    def b(self):
        print(self.c)

    def main(self):
        self.c = 222
        t1 = threading.Thread(target=self.b)
        t1.start()


A().main()