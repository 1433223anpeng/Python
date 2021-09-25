import os
import json
import asyncio

class BiliHebin():
    def __init__(self):pass

    def get_dir(self):
        try:
#            a = input("请输入需要修改的目录：").strip()
#            b = input("请输入输出目录：").strip()
            self.workdir = "885561160"
            self.outdir = "out"
        except:
            print("出现异常，退出")
            exit()

    async def hebing(self,cwd):

        with open(f"{cwd}/entry.json") as f:
            name = json.loads(f.read())['page_data']['part']
        s = os.listdir(f"{cwd}")
        for i in s:
            if  os.path.isdir(f"{cwd}/"+i):
                qinxidu = i

        mingl = f'ffmpeg -i {cwd}/{qinxidu}/video.m4s -i {cwd}/{qinxidu}/audio.m4s  -codec copy "{self.outdir}/{name}.mp4"'
        a = await asyncio.create_subprocess_shell(mingl,
                                                    stdout=asyncio.subprocess.PIPE,
                                                    stderr=asyncio.subprocess.PIPE
                                                        )
        stdout,__stderr = await a.communicate()
        stdout = stdout.decode('utf-8')
        print(f"{name}---> 合并完成")
    
    async def get_info(self):
        self.get_dir()
        try:
            os.chdir(self.workdir)
            if not os.path.isdir(self.outdir):
                os.mkdir(self.outdir)
        except:
            print("目录错误！")
            exit()
        
        li = os.listdir()
        l2 = []
        for i in li:
            if os.path.isdir(i):
                l2.append(i)
        del li

        try: 
            l2.remove(self.outdir)
        except:
            pass
        #print(l2)
        task = [asyncio.ensure_future(self.hebing(i)) for i in l2]
        await asyncio.gather(*task)

    def main(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.get_info())

if __name__ == "__main__":
    BiliHebin().main()