import jieba

import utils.os_util as ou

# source 是一个语料 list（未分词）
def segementation(input_file, output_file, user_dict, seperator, output_encoding):
    jieba.set_dictionary("./data/dict/dict.txt.small")
    jieba.load_userdict(user_dict)

    line_count = 0
    empty_count = 0
    for line in input_file:
        if len(line) == 0: # 跳过空行
            empty_count = empty_count + 1
            continue
        # 从 bytes 转成字符串
        newline = bytes.decode(line)
        # 去掉多于空格
        arr = newline.split(' ')
        seg_list = jieba.cut("".join(arr))  # 默认是精确模式
        output_file.write(bytes(seperator.join(seg_list), encoding=output_encoding))  
        line_count = line_count + 1
    
    print("\n[完成]共处理 %d 行数据，跳过 %d 行空行" % (line_count, empty_count))
    return 0
    