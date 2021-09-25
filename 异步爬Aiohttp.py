import asyncio
import aiohttp
import threading



class Spider():
    def __init__(self) -> None:
        self.U_A = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        }
        self.url = [
            "https://www.baidu.com",
            "https://www.qq.com",
            "https://hao123.com",
            "https://www.360.com"
            ]
        self.dic = dict()

    async def get_html(self,url,index):
        async with self.session.get(url,verify_ssl=False) as resp:
            
            t = await resp.text()
            # print(t)
            self.dic.update({index:t})

    async def dow(self):
        self.session = aiohttp.ClientSession()
        self.session.headers.update(self.U_A)
        tasks = []
        x = 0
        for i in self.url:
            t = asyncio.create_task(self.get_html(i,x))
            tasks.append(t)
            x+=1
        await asyncio.wait(tasks)

        await self.session.close()

    def w(self):
        i = 0
        while True:
            x = self.dic.pop(i,False)
            if x:
                print(x)
                i+=1
            if i == 3:
                break

    def main(self):
        t = threading.Thread(target=self.w)
        t.start()

        asyncio.run(self.dow())

if __name__ == "__main__":
    Spider().main()