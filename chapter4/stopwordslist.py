# ! python3
# -*- coding: utf-8 -*-
# author : yunchao.zhang
import jieba
from collections import Counter


# 创建停用词list
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords


# 对句子进行分词
def seg_sentence(sentence):
    """
    need txt
    :param sentence:
    :return:
    """
    jieba.load_userdict('./电商客服对话日志.txt')
    sentence_seged = jieba.cut(sentence.strip())
    stopwords = stopwordslist('./stopword.txt')  # 这里加载停用词的路径
    outstr = []
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr.append(word)
    return outstr


# 对分词进行词频展示
def word_frequency(line_seg):
    """
    need ['add','add']
    :param line_seg:
    :return:
    """
    c = Counter()
    for x in line_seg:
        if len(x) > 1 and x != '\r\n':
            c[x] += 1
    for (k, v) in c.most_common():
        print('%s%s  %d' % (' ' * (5 - len(k)), k, v))


inputs = open('./电商客服对话日志.txt', 'r', encoding='utf-8')
lines = ""
for line in inputs:
    lines += line.replace("\n", "")
inputs.close()
line_seg = seg_sentence(lines)  # 这里的返回值是列表
word_frequency(line_seg)  # 取词频