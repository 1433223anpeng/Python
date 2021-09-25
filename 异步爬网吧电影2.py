from requests_html import AsyncHTMLSession,requests
import asyncio
import time
import logging
from Crypto.Cipher import AES
import re
import threading

#传递一个url即可

#使用requests-html

logging.basicConfig(level= logging.INFO,filename="m3u8async.py.log",filemode='a',format = "%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

class WBDYM3U8():
    def __init__(self,url) -> None:
        self.root_url = url
        self.url = "https://vod6.wenshibaowenbei.com"
        self.U_A = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        }
        self.key = b''
        self.dicta = dict()
        logger.info("初始化已完成！")

    def getroothtml(self):
        try:
            logger.info(f"正在获取目标首页，{self.root_url}")
            r = requests.get(self.root_url,headers=self.U_A)
            r.raise_for_status
            logger.info(f"获取目标首页成功，{self.root_url}")
            text = r.text
            data = re.findall("url=(.*?)&id=.*?<h2>(.*?)</h2>",text,re.S)[0]
            return data
        except:
            logger.error(f"获取目标首页发生异常，{self.root_url}->{r.status_code}")

    def get_root_m3u8(self,url):
        try:
            logger.info(f"正在获取初始M3U8文件，{url}")
            r = requests.get(url,headers=self.U_A)
            r.raise_for_status
            logger.info(f"获取初始M3U8文件成功，{url}")
            r.encoding = 'utf-8'
            return r.text
        except:
            logger.error(f"获取初始M3U8文件发生异常，{url}->{r.status_code}")
            exit()
    
    def get_real_m3u8(self) -> str:
        u = self.txtindex.strip().split('\n')[-1]
        url = self.url+u
        print(url)
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
        print(txt)
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
        for i in range(5):
            try:
                logger.info(f"正在获取第{index:0>4}个片段，URL：{url}")
                r = await self.session.get(url,timeout=10)
                r.raise_for_status
                x = r.content
                aes = AES.new(self.key,AES.MODE_CBC,self.key)
                con = aes.decrypt(x)
                logger.info(f"获取第{index:0>4}个片段成功，URL：{url}")
                r.close()
                self.dicta.update({index:con})
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
        self.session = AsyncHTMLSession()
        self.session.headers.update(self.U_A)

        tasks = []
        for i in range(len(ul)):
            t = asyncio.create_task(self.get_ts(ul[i],i))
            tasks.append(t)

        await asyncio.wait(tasks)
        await self.session.close()

    def main(self):
        data = self.getroothtml()
        
        firsturl = data[0]
        self.filename = data[1] + ".mp4"

        self.txtindex = self.get_root_m3u8(firsturl)


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
    URL= "http://www.wbdy.tv/play/43938_1_1.html"
    start = time.time()
    a = "#EXTM3U\n#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1000000,RESOLUTION=1280x534\n/20210720/BiB1eWyS/1000kb/hls/index.m3u8"
    # WBDYM3U8(a,"热带往事.mp4").main()
    WBDYM3U8(URL).main()
    print("OK!")
    print("用时",time.time()-start)