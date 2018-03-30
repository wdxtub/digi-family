import sys
import os

def split_line(letter="=", gap=0, length=30):
    unit = letter + " " * gap
    line = unit * length
    print(line)

def check_path(path):
    if path[-1] != "/":
        return path + "/"
    return path


def check_ret(code):
    if code != 0:
        print("任务执行失败，错误码", code)
        sys.exit()


def check_para(para, option, hint):
    if para is None:
        print("没有指定 %s,请使用 --%s 选项指定", hint, option)
        sys.exit()

def check_file(path, hint):
    if not os.path.exists(path):
        print("没有找到",path,"文件，", hint)
        sys.exit()

def check_interval(interval):
    if interval == "D":
        print("获取以天为单位的数据")
        return interval
    elif interval == "W":
        print("获取以周为单位的数据")
        return interval
    elif interval == "M":
        print("获取以月为单位的数据")
        return interval
    elif interval == "5":
        print("获取以 5 分钟为单位的数据")
        return interval
    elif interval == "15":
        print("获取以 15 分钟为单位的数据")
        return interval
    elif interval == "30":
        print("获取以 30 分钟为单位的数据")
        return interval
    elif interval == "60":
        print("获取以 60 分钟为单位的数据")
        return interval
    return -1