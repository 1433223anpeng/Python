import asyncio
import requests
import aiohttp
import logging
from Crypto.Cipher import AES
import threading
import re
import time


logging.basicConfig(level= logging.INFO,filename="m3u8async.py.log",filemode='a',format = "%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

class WBDYM3U8():
    def __init__(self,txtindex:str,filename:str) -> None:
        self.txtindex = txtindex
        self.filename = filename
        self.url = "https://vod6.wenshibaowenbei.com"
        self.U_A = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        }
        self.key = b''
        self.dicta = dict()
        logger.info("初始化已完成！")

    def get_real_m3u8(self) -> str:
        u = self.txtindex.split('\n')[-1]
        url = self.url+u
        try:
            logger.info(f"正在获取真实M3U8文件，{url}")
            r = requests.get(url,headers=self.U_A)
            r.raise_for_status
            logger.info(f"获取真实M3U8文件成功，{url}")
            r.encoding = 'utf-8'
            return r.text
        except:
            logger.error(f"获取真实M3U8文件发生异常，{url}->{r.status_code}")
            exit()

    def get_key(self,txt) -> None:
        url = re.findall('URI="(.*?key)"',txt)[0].strip()
        try:
            logger.info(f"正在获取KEY，{url}")
            r = requests.get(url,headers=self.U_A)
            r.raise_for_status
            logger.info(f"获取KEY成功，{url}")
            self.key = r.content
        except:
            logger.error(f"获取KEY发生异常，{url}->{r.status_code}")
            exit()

    async def get_ts(self,url,index):
        # print(self.dicta)
        for i in range(5):
            try:
                async with self.session.get(url,verify_ssl = False) as resp:
                    resp.raise_for_status
                    logger.info(f"正在获取第{index:0>4}个片段，URL：{url}")
                    r = await resp.content.read()
                    aes = AES.new(self.key,AES.MODE_CBC,self.key)
                    con = aes.decrypt(r)
                    self.dicta.update({index:con})
                    logger.info(f"获取第{index:0>4}个片段成功，URL：{url}")
                    break
            except Exception as e:
                logger.info(f"获取第{index:0>4}个片段发生异常，{(i+1)*3}秒后，URL：{url}>>>ERROR>>{e}, ")
                await asyncio.sleep((i+1)*3)

    def write_ts(self):
        i = 0
        logger.info("进入写文件线程")
        while (True):
            with open(self.filename,'ab') as f:
                x = self.dicta.pop(i,False)
                if x :
                    logger.info(f"正在写入第{i+1}块数据！")
                    # print(self.dicta)
                    f.write(x)
                    i +=1
                if i == self.control:
                    break
        logger.info("数据写入完成！")


    async def download(self,ul):
        self.session = aiohttp.ClientSession()
        self.session.headers.update(self.U_A)

        tasks = []
        for i in range(0,len(ul)):
            print(ul[i],i)
            t = asyncio.create_task(self.get_ts(ul[i],i))
            tasks.append(t)

        await asyncio.wait(tasks)
        await self.session.close()


    def main(self):
        #写文件还是开一个线程
        urlstr = self.get_real_m3u8().strip()
        urllist = urlstr.split('\n')
        ul = []

        self.get_key(urlstr)

        for url in urllist:
            if not url.startswith("#"):
                ul.append(url.strip())

        self.control = len(ul)

        del urllist
        del urlstr
        
        t = threading.Thread(target=self.write_ts)
        t.start()

        #开始异步
        asyncio.run(self.download(ul))

if __name__ == "__main__":
    start = time.time()
    a = "#EXTM3U\n#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1000000,RESOLUTION=1280x534\n/20210720/BiB1eWyS/1000kb/hls/index.m3u8"
    WBDYM3U8(a,"热带往事.mp4").main()
    print("OK!")
    print("用时",time.time()-start)