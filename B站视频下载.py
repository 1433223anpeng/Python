import requests
import re
import os
import json
from threading import Thread


class BiliBili():
    def __init__(self, BV:str):
        if BV.startswith("BV"):
            self.root_url = "https://www.bilibili.com/video/" + BV
        else:
            raise Exception("请输入BV号")
            exit()
        self.path = self.root_url.split('/')[-1]
        self.session = requests.session()
        U_A = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36",
        }
        self.session.headers.update(U_A)
        self.U_A = {
            "range": "bytes=0-",
            "referer": self.root_url,
        }

    def get_root_page(self):
        try:
            r = self.session.get(self.root_url)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except Exception as e:
            print(f"在get_root_page 函数发生了异常-》》》{e}")
            exit()

    def get_data(self, txt):
        try:
            clear = re.compile("<script>window.__playinfo__=(.*?)</script>")
            r = clear.findall(txt)[0]
            data = json.loads(r)
            return data['data']
        except Exception as e:
            print(f"在get_data函数中发生了异常-》》》》{e}")
            exit()

    def get_video(self):
        try:
            r = self.session.get(self.vbaseurl, headers=self.U_A)
            r.raise_for_status()
            with open(f'{self.path}/video.m4s', 'wb') as f:
                f.write(r.content)
        except Exception as e:
            print(f"在get_video函数中遇到-》》》》{e}")
            exit()

    def get_audio(self):
        try:
            r = self.session.get(self.abaseUrl, headers=self.U_A)
            r.raise_for_status()
            with open(f'{self.path}/audio.m4s', 'wb') as f:
                f.write(r.content)
        except Exception as e:
            print(f"在get_video函数中遇到-》》》》{e}")
            exit()

    def V_A_to_mp4(self):
        shell = f"ffmpeg -i {self.path}/audio.m4s -i {self.path}/video.m4s {self.path}.mp4"
        print("等待视频合并中。。。。。。")
        os.system(shell)
        print("合并完成，删除中间文件")
        os.system(f"rmdir /S /Q {self.path}")
        print("删除完成。。。")

    def get_baseUrl(self,video,audio,quality,video_codecid):
        for i in video:
            if i['id'] == quality and i['codecid'] != video_codecid:
                self.vbaseurl = i['baseUrl']

        for i in audio:
            if str(i['id'])[-2:] == str(quality):
                self.abaseUrl = i['baseUrl']

    def main(self):
        a = self.get_root_page()
        b = self.get_data(a)
        quality = b['quality']  # 清晰度112:1080高码率，80：1080，64：720，32：480，16：360
        video_codecid = b['video_codecid']
        #timelength = b['timelength']  # 视频的时间毫秒为单位
        dash = b['dash']
        video = dash['video']
        audio = dash['audio']

        self.get_baseUrl(video,audio,quality,video_codecid)
        os.system(f'mkdir {self.path}')

        t1 = Thread(target=self.get_video())
        t2 = Thread(target=self.get_audio())
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        self.V_A_to_mp4()

if __name__ == '__main__':
    BV = ""#输入BV好下载视频
    BiliBili(BV).main()
