# #！/usr/bin/python3
import random

class Cmp():

    def __init__(self,p1,p2):#传两个比较大小
        self.p1 = p1#玩家1
        self.p2 = p2#玩家2
        self.BAOZI = 6# 豹子
        self.COLORSEQ = 5# 同花顺
        self.COLOR = 4# 同花
        self.SEQ = 3# 顺子
        self.PAIR = 2# 对子
        self.SINGLE = 1# 单张
    
    #判断是不是豹子
    def Baozi(self,a):#a是扑克牌列表
        x = self.Dic_Pai(a)#字典，{牌面:张数}
        x = sorted(x.items() ,key = lambda a:a[1])#x变成列表
        if len(x) == 1:
            return (True,x[0][0])#表示豹子,第二个值就是牌面
        else :
            return (False,0)

    #判断牌里面相同牌的张数 返回字典，{牌面:张数}
    def Dic_Pai(self,a):#a是扑克牌列表
        x = {}
        for p,i in a:#i是牌面
            x[i] = x.get(i,0) + 1
        return x

    #判断是不是对子
    def Pair(self,a):#a是扑克牌列表
        x = self.Dic_Pai(a)#字典，{牌面:张数}
        x = sorted(x.items() ,key = lambda a:a[1])#x变成列表
        if len(x) == 2:#表示是对子
            return (True,x[0][0],x[1][0])#3表示豹子,第二个值就是对子牌面，第三个是单张牌面
        else :
            return (False,0,0)

    #判断花色有几张相同的
    def Color(self,a):#a是扑克牌列表
        x = set()
        for p,i in a:
            x.add(p) 
        if len(x) == 1:#集合里面只有一个说明3个花色相同
            return (True,self.One(a))#都是同花比单张
        else:
            return (False,0)

    #判断是不是同花顺
    def TongHuaShun(self,a):#a是扑克牌列表
        x = self.Color(a)
        y = self.ShunZi(a)
        if x == True and y == True:
            return (True,self.One(a))#假如都是同花顺比较那个大牌多
        else :
            return (False,0)

    #判断是不是顺子 从最大牌开始比
    def ShunZi(self,a):#a是扑克牌列表
        x = self.One(a)
        # print("x = ",x)
        if x[0]+2 == x[-1]:#这个应为之前排过序，又是for依次添加，所以这个为True那么他就是顺子
            #【1,12,13】和【1,2,13】
            return True
        elif x == [1,12,13] or x == [1,2,13]:
            return True
        else :#这个就说明不是顺子
            return False

    #判断单张的
    def One(self,a):#a是扑克牌列表
        x = [i for p,i in a]
        return x
    
    ##判断牌是那种类型的
    def Swith(self,a):
        b = self.Baozi(a)[0]#a设为一个比较变量,结果为bool
        if b :
            return self.BAOZI#返回 豹子
        b = self.TongHuaShun(a)[0]
        if b :#查看a是不是同花顺
            return self.COLORSEQ#返回 同花顺
        b = self.Color(a)[0]
        if b:#查看是不是同花
            return self.COLOR
        b = self.ShunZi(a)
        if b :#查看是不是顺子
            return self.SEQ
        b = self.Pair(a)
        if b[0] :#查看是不是对子
            return self.PAIR
        else :
            return self.SINGLE

    def main(self):#设置返回值为-1,0,1   -1表示第一个玩家赢，0表示平局，1表示第二个玩家赢
        a = self.Swith(self.p1)
        b = self.Swith(self.p2)
        if a > b:#p1赢
            return 0
        elif a == b and a == self.BAOZI:#都是同一种类型
            x = self.Baozi(self.p1)[1]
            y = self.Baozi(self.p2)[1]
            if x > y :#p1赢
                return 0
            elif x == y :#平局
                return -1
            else:
                return 1
        elif a == b and a == self.COLORSEQ:#都是同花顺，比单张
            x = self.TongHuaShun(self.p1)[1]
            y = self.TongHuaShun(self.p2)[1]
            if x > y:#p1赢
                return 0
            elif x == y :#平局
                return -1
            else:
                return 1
        elif a==b and a == self.COLOR:#都是同花，比单张
            x = self.Color(self.p1)[1]
            y = self.Color(self.p2)[1]
            if x > y:#p1赢
                return 0
            elif x == y :#平局
                return -1
            else:
                return 1
        elif a==b and a == self.SEQ:#都是顺子，比单张
            x = self.One(self.p1)
            y = self.One(self.p2)
            if x > y:#p1赢
                return 0
            elif x == y :#平局
                return -1
            else:
                return 1
        elif a == b and a == self.PAIR :#对子
            x = self.Pair(self.p1)[1:]
            y = self.Pair(self.p2)[1:]
            if x[0] > y[0]:#p1赢
                return 0
            elif x[0] == y[0] and x[1] > y[1]:#对子相等#比单张牌 p1赢
                return 0
            elif x[0] == y[0] and x[1] == y[1]:#单张也相等
                return -1
            else:#p2赢
                return 1
        elif a==b and a == self.SINGLE:#单张
            x = self.One(self.p1)
            y = self.One(self.p2)
            if x > y:#p1赢
                return 0
            elif x == y :#平局
                return -1
            else:
                return 1
        else:
            return 1

class ZhaJinHua():
    def __init__(self):
        self.PK = [(j,i)  for j in range(4)  for i in range(1,14)]#定义扑克牌列表(里面是元组)去掉大小王
        self.PAI = {#映射关系，数字:牌面,所有数字在最后输出时替换为牌面
            13:'A',
            12:'K',
            11:'Q',
            10:'J',
            9:'10',
            8:'9',
            7:'8',
            6:'7',
            5:'6',
            4:'5',
            3:'4',
            2:'3',
            1:'2',
        }
        self.COLOR = {#映射关系，数字:花色,所有数字在最后输出时替换为牌面
            0:"红桃",
            1:"方块",
            2:"黑桃",
            3:"梅花",
        }
        self.main()#调用这个类时，启动main函数

    def InputPeople(self):#输入人数
        try :
            self.PEOPLE = int(input("请输入玩家个数(整数大于2,小于17)："))
            if self.PEOPLE > 17 or self.PEOPLE < 0:
                raise 
        except:
            print("输入人数错误")
            exit()
    
    def PrintPai(self):
        print("-"*50)
        for i in range(1,len(self.Dic_List)+1):
            Str_Pai = ""
            for j in self.Dic_List[i-1]:
                Str_Pai += j[0] + ":" + j[1] +', '
            print(f"玩家{i} 的牌是==> {Str_Pai}")
            print("-"*50)

    def main(self):
        #定义一副扑克牌（去掉大小王的扑克牌）
        #了解了一下发现A最大，2最小所以 
        #用元组来表示花色和牌面 (0,13) 表示红桃A
        #(1,13)表示方块A (2,13)表示黑桃A (3,13)表示梅花A(因为A最大所以用13)   ‘K‘ == 12 ‘2‘ == 1
        self.InputPeople()
        self.P_List = [[] for i in range(self.PEOPLE)]#n个玩家对应的牌面列表，每个列表有三个元祖，每个元祖表示，一张牌
        for x in range(3):
            for i in self.P_List:
                a = self.PK[random.randint(0,len(self.PK)-1)]
                i.append(a)
        self.P_List2 = self.P_List[:]

        #冒泡排序，最大的在后面
        for i in range(len(self.P_List2)):
            for j in range(len(self.P_List2)-i-1):
            # print(Cmp(P_List2[j],P_List2[j+1]).main())
                if Cmp(self.P_List2[j],self.P_List2[j+1]).main() == 0:
                    # print("adsaddddddd")
                    self.P_List2[j], self.P_List2[j+1] = self.P_List2[j+1], self.P_List2[j]

        #因为上面排序了，P_List2里面最后一个的牌最大，第一个牌最小
        for i in range(1,len(self.P_List)+1):
            self.Dic_List = [[] for i in range(self.PEOPLE)]
            for i in range(0,len(self.P_List)):
                for x,y in self.P_List[i]:
                    # print(i,x)
                    self.Dic_List[i].append((self.COLOR.get(x),self.PAI.get(y)))

        #输出每个玩家的牌
        self.PrintPai()
        
        #赢家顺序是
        self.P_List2.reverse()#现在大牌在前
        for i in self.P_List2:
            print("玩家 ",self.P_List.index(i)+1)

if __name__ == '__main__':
    ZhaJinHua()
#


"""
兰州大学      平均281    总招生人数21*20(420)人                      双向选择
西南大学      平均270    总招生人数31*4+5(129)人
安徽大学     平均270分    总招生人数20*87+4*10+14*1+5*6(1824)人 
太原科技大学 平均268       总招生人数24*4(96)人                       双向选择
江苏大学     平均266       总招生人数31*5(155)人
"""