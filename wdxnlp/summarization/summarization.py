# -*- coding: utf-8 -*-
from optparse import OptionParser

import sys
import datetime
import os
import codecs

sys.path.append('../utils')
import os_utils as ou

def help():
    print("- - - - - - - - - - - - - - - - - - - - - - - -")
    print("|             Summarization Tool              |")
    print("|             @wdxtub 2017.11.16              |")
    print("- - - - - - - - - - - - - - - - - - - - - - - -")
    parser.print_help()
    print("\n可选的参数(arg)列表，带 * 的参数为必须，其他可选")
    print("summary - 获取公告文件的摘要，参数 --input")
    sys.exit()

def summarization(input_path, output_path):
    texts = codecs.open(input_path, "r", "utf-8")
    output = codecs.open(output_path, "w+", "utf-8")

    for line in texts:
        items = line.split("_")
        code = items[0]
        title = items[1]
        datestr = items[2]
        timestr = ":".join(items[3:5]) + ":" + items[5][:2]
        content = items[5][2:]
        
        print(code, title, datestr, timestr)
        output.write("%s %s %s %s\n" %(code, title, datestr, timestr))
        summary = extract_summary(content, '。')
        print("[摘要]", summary) 
        output.write("[摘要] %s\n" % summary)
        print("[原文]", content)
        output.write("[原文] %s\n" % content)

    texts.close()
    output.close()
    return 0


# 抽取摘要
def extract_summary(content, split_flag):
    # 先进行分句，使用 split_flag（一般是逗号或者句号）
    sentences = content.split(split_flag)
    print("原文共", len(sentences), "个分句")
    result = []
    
    for s in sentences:
        skip = False
        for word in stopwords:
            if word in s:
                skip = True
                break
                
        # 判断句子中是否包含关键词
        if skip:
            continue
        for word in keywords:
            if word in s:
                result.append(s)
                break
    print("摘要共", len(result), "个分句")
    return split_flag.join(result)



parser = OptionParser(usage="%prog [options] arg", version="%prog 0.1")

parser.add_option("--input", default="../data/announcement/tingpai.txt",
                  action="store", dest="input",
                  help="输入的语料，默认为 ../data/announcement/tingpai.txt")
parser.add_option("--output", default="summary-result.txt",
                  action="store", dest="output",
                  help="结果输出的文件，默认为 summary-result.txt")
parser.add_option("--keywords", default="../data/dict/keywords.dict",
                  action="store", dest="keywords",
                  help="关键词词典，默认为 ../data/dict/keywords.dict")
parser.add_option("--stopwords", default="../data/dict/stopwords.dict",
                  action="store", dest="stopwords",
                  help="停止词词典，默认为 ../data/dict/stopwords.dict")
(options, args) = parser.parse_args()

keywords = []
stopwords = []

if __name__ == "__main__":    
    if len(args) != 1:
        help()

    with codecs.open(options.keywords, "r", "utf-8") as f:
        for word in f:
            if len(word) > 1:
                keywords.append(word[:-1])
    with codecs.open(options.stopwords, "r", "utf-8") as f:
        for word in f:
            if len(word) > 1:
                stopwords.append(word[:-1])
                
    print(keywords)
    print(stopwords)

    begin = datetime.datetime.now()
    if args[0] == "summary":
        ou.check_ret(summarization(options.input, options.output))
    else:
        help()
    end = datetime.datetime.now()
    ou.split_line()
    print("执行用时: ")
    print(end - begin)


