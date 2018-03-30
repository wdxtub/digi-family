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

def check_file(path, hint):
    if not os.path.exists(path):
        print("没有找到",path,"文件，", hint)
        sys.exit()