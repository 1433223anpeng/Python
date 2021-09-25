from Crypto.Cipher  import AES
import requests
import re



    
class wbdyM3U8():
    def __init__(self,txtindex,filename) -> None:
        self.txtindex = txtindex
        self.filename = filename
        self.U_A = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        }
        self.session = requests.Session()
        self.session.headers.update(self.U_A)
        self.key = b""
        self.url = "https://vod6.wenshibaowenbei.com"

    def get_index2(self,url) -> str:
        try :
            r = self.session.get(url)
            r.raise_for_status
            return r.text
        except:
            print(f"无法请求到该页面，URL={url}")
            return ""

    def get_key(self,url) -> None:
        try :
            r = self.session.get(url)
            r.raise_for_status
            self.key = r.content
        except:
            print(f"无法请求到该KEY，URL={url}")
            exit()

    def get_ts(self,url) -> bytes:#多次调用该方法，每次返回都是2进制数据
        try :
            r = self.session.get(url)
            r.raise_for_status
            aes = AES.new(self.key,AES.MODE_CBC,self.key)
            res = aes.decrypt(r.content)
            return  res
        except:
            print(f"无法请求到该TS，URL={url}")
            return b""

    def write_ts_file(self,data):
        with open(self.filename,'wb') as f:
            f.write(data)

    def notrootindex(self):
        url = re.findall("\n.*?m3u8",self.txtindex)[0].strip()
        m3u8index = self.get_index2(self.url+url)
        print(m3u8index)
        k = re.findall('URI="(.*?key)"',m3u8index)[0].strip()
        print(k)
        self.get_key(k)
        url_all = m3u8index.split('\n')[6:]
        url_li = url_all[1::2]
        for i in url_li:
            if i.strip() != '':
                self.write_ts_file(self.get_ts(i.strip()))

    def haverootindex(self):
        k = re.findall('URI="(.*?key)"',self.txtindex)[0].strip()
        print(k)
        self.get_key(k)
        url_all = self.txtindex.split('\n')[6:]
        url_li = url_all[1:50:2]
        for i in url_li:
            if i.strip() != '':
                self.write_ts_file(self.get_ts(i.strip()))

    def main(self) -> None:
        if "#EXTINF" not in self.txtindex:
            self.notrootindex()
        else:
            self.haverootindex()

if __name__ == "__main__":
    with open("index.m3u8",'r') as f:
        a = f.read()
    wbdyM3U8(a,"火星.mp4").main()
    