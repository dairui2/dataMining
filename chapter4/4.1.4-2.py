import  jieba

with open('./电商客服对话日志.txt', 'r', encoding='utf8', errors='ignores') as f:
    txt = f.read()

with open('./stopword.txt', 'r', encoding='utf8', errors='ignores') as f:
    stopwordlist = f.readlines()    #读取停用词到一个列表中
    maped = map(lambda  x: str(x).strip(), stopwordlist)    #删除停用词的前后空白，map是映射函数，对列表中的每一行元素都进行处理(删除前后空白).
    stopwordlist = list(maped)

#添加自定义的词
jieba.add_word('iPhone 13')

words = jieba.cut(txt) #精确模式

counts = {}     #保存次数的对象

for word in words:
    word = word.strip()     #删除词的前后空白，包括空格，换行，制表符等

    if word not in stopwordlist:
        counts[word] = counts.get(word, 0) + 1      #判断word是否被包含在停用词课表中

    # counts[word] = counts.get(word, 0) + 1      #get读取word的值，word的键，0是默认值，当没有对应的值时，返回默认值

items = list(counts.items())    #将键值对转换成列表
items.sort(key=lambda x:x[1], reverse=True)     #根据词出现的次数从大到小排序

for i in range(10):
    word, count = items[i]
    print("{0} - {1}".format(word, count))

