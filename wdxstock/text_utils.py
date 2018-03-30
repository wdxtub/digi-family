from gensim import corpora, models, similarities

import datetime
import jieba

def clean_topic(line):
    # 用来清理 topic 的显示
    # example 0.075*"投" + 0.060*"失败" + 0.059*"智定" + 0.043*"邮政" + 0.036*"持仓" + 0.030*"开通" + 0.029*"定" + 0.025*"为什么" + 0.023*"支付" + 0.022*"卡"
    newline = []
    arr = line.split('+')
    for item in arr:
        words = item.split("\"")
        newline.append(words[1])
    return " ".join(newline)

# source 是一个语料 list（未分词）
def get_lda_result(source):
    documents = []
    num_topic = 10
    show_count = 5000
    print("对输入语料进行分词")
    jieba.set_dictionary("./data/dict/dict.txt.small")
    jieba.load_userdict("./data/dict/jieba_user.dict")
    count = 0
    for line in source:
        # 去掉空格
        arr = line.split(" ")
        seg_list = jieba.cut("".join(arr))
        documents.append(" ".join(seg_list))
        count = count + 1
        if count % show_count == 0:
            print("已处理 %d 行" % count)
    print("日志共 %d 条有效记录" % count)
    # 处理为语料格式
    texts = [[word for word in document.lower().split()] for document in documents]
    dictionary = corpora.Dictionary(texts)
    print("载入词典完成")
    begin = datetime.datetime.now()
    corpus = [dictionary.doc2bow(text) for text in texts]
    print("开始训练 LDA 模型，共 %d 个 topic" % num_topic)
    LDA = models.LdaMulticore(corpus, num_topics=num_topic, id2word=dictionary, workers=4, passes=3, chunksize=2000)
    print("模型训练完成，用时", datetime.datetime.now() - begin)
    print("开始用 LDA 模型分类语料")
    topic_result = [[] for i in range(num_topic)]
    for i in range(len(texts)):
        if i != 0 and i % show_count == 0:
            print("已处理 %d 行" % i)
        topics = LDA.get_document_topics(corpus[i])
        if len(topics) < 1:
            continue
        # 这里插入一个 tuple
        topic_result[topics[0][0]].append(("".join(texts[i]), topics[0][1]))
    for i in range(len(topic_result)) :
        print("- - - - - - 子类别 %d 信息 - - - - - - - -" % i)
        print("关键词",clean_topic(LDA.print_topic(i, 10)))
        for line in topic_result[i]:
            print(line[0])
    

if __name__ == "__main__":
    get_lda_result(["lalal", "hahaha"])