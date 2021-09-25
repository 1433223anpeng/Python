from   requests_html  import HTMLSession
from   Crypto.Cipher  import AES
import re
import logging
#可作为模块调用


from concurrent.futures import ThreadPoolExecutor


# from T  import ThreadPoolExecutor

logging.basicConfig(level= logging.INFO,filename="m3u8async.py.log",filemode='a',format = "%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

class WBDYM3U8():
    def __init__(self,txtindex,filename) -> None:
        self.txtindex = txtindex
        self.filename = filename
        self.U_A = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        }
        self.sessionA = HTMLSession()
        self.sessionA.headers.update(self.U_A)
        self.key = b""
        self.url = "https://vod6.wenshibaowenbei.com"
        self.Thread_NUM = 25
        self.THPOOL = ThreadPoolExecutor(11)
        logger.info("初始化已完成")

    def get_index2(self) -> str:#请求有效码m3u8页面
        u = re.findall("\n.*?m3u8",self.txtindex)[0].strip()
        url = self.url+u
        try :
            r = self.sessionA.get(url)
            logger.info(f"正在请求 URL->{url}")
            r.raise_for_status
            logger.info(f"请求成功 URL->{url}")
            return r.text
        except:
            logger.error(f"无法请求到该页面，URL->{url}")
            exit()
    
    def get_key(self,txt) -> None:
        url = re.findall('URI="(.*?key)"',txt)[0].strip()
        try :
            r = self.sessionA.get(url)
            logger.info(f"正在请求 URL->{url}")
            r.raise_for_status
            logger.info(f"请求成功 URL->{url}")
            self.key = r.content
        except:
            logger.error(f"无法请求到该KEY，URL={url}")
            exit()

    def get_tsP(self,url,num):
        try :
            r = self.sessionA.get(url,timeout=3)
            logger.info(f"第{num+1} 个片段正在请求 URL->{url}")
            r.raise_for_status
            logger.info(f"第{num+1} 个片段请求成功 URL->{url}")
            aes = AES.new(self.key,AES.MODE_CBC,self.key)
            res = aes.decrypt(r.content)
            self.dicta.update({num:res})
        except:
            logger.warning(f"第{num+1} 无法请求到该TS，URL={url}")
            self.THPOOL.submit(self.get_tsP,url,num,priority=0)
            logger.info("错误链接入线程池！")

    def write_ts_F(self):#开启一个线程，while True写入，用字典的pop方法
        i = 0
        logger.info("进入写文件线程")
        while (True):
            with open(self.filename,'ab') as f:
                x = self.dicta.pop(i,False)
                if x :
                    logger.info(f"正在写入第{i+1}块数据！")
                    f.write(x)
                    i +=1
                if i == self.control:
                    break
        logger.info("数据写入完成！")

    def _get_url_li(self,txt:str) -> list:
        a = txt.strip().split('\n')[6:]
        return a[1::2]

    def notrootindex(self):
        m3u8index = self.get_index2()
        logger.info("进入到非直接就是tsurl的m3u8文件")

        self.get_key(m3u8index)
        logger.info("获得KEY")
        
        url_all = self._get_url_li(m3u8index)[0:300]

        logger.info("添加URL到队列")

        self.control = len(url_all)
        self.dicta = dict()

        logger.info("开启写入文件线程")
        self.THPOOL.submit(self.write_ts_F,priority=0)

        for i in range(0,len(url_all)):
            self.THPOOL.submit(self.get_tsP,url_all[i],i)
        
        self.THPOOL.shutdown()

    def main(self) -> None:
        if "#EXTINF" not in self.txtindex:
            self.notrootindex()
        else:
            print("传入数据不对")
            logger.error("传入数据不对")

if __name__ == "__main__":
    print("OK!")
    a = "#EXTM3U\n#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1000000,RESOLUTION=1280x534\n/20210720/BiB1eWyS/1000kb/hls/index.m3u8"
    WBDYM3U8(a,"热带往事.mp4").main()
    
#修改成双端队列
#2021年9月12日
#江户川
