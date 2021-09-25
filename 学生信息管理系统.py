#!/usr/local/bin/python3

import json

class Student(object):
    def __init__(self):
        self.initstr = """
===========================学生信息管理系统===========================
------------------------------功能菜单--------------------------------
            1.录入学生信息
            2.查找学生信息
            3.删除学生信息
            4.修改学生信息
            5.排序
            6.统计学生总人数
            7.显示所有学生信息
            0.退出系统
----------------------------------------------------------------------
"""

    def read_list(self):
        try:
            with open("student.db",'r') as f:
                x = []
                for i in f.readlines():
                    x.append(json.loads(i))
                return x
        except:
            with open("student.db",'w') as f:
                return []


    def write_file(self,dict_list):
        with open("student.db",'w') as f:
            for i in dict_list:
                f.write(json.dumps(i))
                f.write('\n')

    def add(self):
        while True:
            ID = input("请输入学生ID：").strip()
            name = input("请输入学生姓名：").strip()
            English = input("请输入英语成绩：").strip()
            Math = input("请输入数学成绩：").strip()
            Python = input("请输入Python成绩：").strip()
            Total = float(English) + float(Math) + float(Python)
            dict_list = self.read_list()
            dict_list.append({"ID":int(ID),"Name":name,"English":int(English),"Math":int(Math),"Python":int(Python),"Total":Total})
            self.write_file(dict_list)
            print("添加学生信息成功！！")
            IN = input("继续Y，否则N：").strip()
            if IN == "Y" or IN == "y":
                continue
            else :
                break

    def query(self):
        l = self.read_list()
        mod = input("请输入查询方式(1:ID查询，2:姓名查询)").strip()
        if mod == "1":
            query_id = input("请输入ID：").strip()
            print("ID\t姓名\t英语\t数学\tPython\t合计")
            for i in l:
                if i["ID"] == query_id:
                    print("{ID}\t{Name}\t{English}\t{Math}\t{Python}\t{Total}".format(**i))
        elif mod == "2":
            query_id = input("请输入姓名：").strip()
            print("ID\t姓名\t英语\t数学\tPython\t合计")
            for i in l:
                if i["Name"] == query_id:
                    print("{ID}\t{Name}\t{English}\t{Math}\t{Python}\t{Total}".format(**i))

    def delect_student(self):
        del_id = input("请输入要删除的学生ID：").strip()
        dict_list = self.read_list()
        for i in dict_list:
            if i["ID"] == del_id:
                dict_list.remove(i)
        self.write_file(dict_list)
        print("删除学生信息成功！！")

    def moify(self):
        moify_ID = input("请输入需要修改的ID：").strip()
        name = input("请输入学生姓名：").strip()
        English = input("请输入英语成绩：").strip()
        Math = input("请输入数学成绩：").strip()
        Python = input("请输入Python成绩：").strip()
        Total = float(English) + float(Math) + float(Python)
        stdout_list = self.read_list()
        for i in stdout_list:
            if i["ID"] == int(moify_ID):
                i["Name"] = name
                i["English"] = English
                i["Math"] = Math
                i["Python"] = Python
                i["Total"] = Total
        self.write_file(stdout_list)
        print("修改已完成！！")

    def sort_func(self,sort_mod):
        not_sort_list = self.read_list()
        if sort_mod == "1":
            not_sort_list.sort(key=lambda x:x["English"])
        elif sort_mod == "2":
            not_sort_list.sort(key=lambda x:x["Math"])
        elif sort_mod == "3":
            not_sort_list.sort(key=lambda x:x["Python"])
        elif sort_mod == "4":
            not_sort_list.sort(key=lambda x:x["Total"])
        return not_sort_list

    def sort_student(self):
        mod1 = input("请选择排序方式(1:降序,2:升序):").strip()
        mod2 = input("请选择排序的项目(1:英语,2:数学,3:Python,4:总分):").strip()
        sort_list = self.sort_func(mod2)
        if mod1 == "1":
            self.show(sort_list[::-1])
        elif mod1 == "2":
            self.show(sort_list)

    def statistics_number(self):
        print("学生人数总计：{}".format(len(self.read_list())))

    def show(self,show_list):
        print("ID\t姓名\t英语\t数学\tPython\t合计")
        for i in show_list:
            print("{ID}\t{Name}\t{English}\t{Math}\t{Python}\t{Total}".format(**i))

    def main(self):
        while True:
            print(self.initstr)
            in_selcet = input("请选择:")
            in_selcet = in_selcet.strip()
            if in_selcet == "0":
                str = input("确定要退出吗(y/n)")
                str = str.strip()
                if str == "y" or str == "Y":
                    exit()
                else:
                    continue
            elif in_selcet == "1":
                self.add()
            elif in_selcet == "2":
                self.query()
            elif in_selcet == "3":
                self.delect_student()
            elif in_selcet == "4":
                self.moify()
            elif in_selcet == "5":
                self.sort_student()
            elif in_selcet == "6":
                self.statistics_number()
            elif in_selcet == "7":
                self.show(self.read_list())

if __name__ == "__main__":
    Student().main()
