import  jieba

with open('./电商客服对话日志.txt', 'r', encoding='utf8', errors='ignores') as f:
    txt = f.read()
# print(txt)
words = jieba.cut(txt) #精确模式

counts = {}     #保存次数的对象

for word in words:
    word = word.strip()     #删除词的前后空白，包括空格，换行，制表符等
    counts[word] = counts.get(word, 0) + 1      #get读取word的值，word的键，0是默认值，当没有对应的值时，返回默认值

items = list(counts.items())    #将键值对转换成列表
items.sort(key=lambda x:x[1], reverse=True)     #根据词出现的次数从大到小排序

for i in range(100):
    word, count = items[i]
    print("{0} - {1}".format(word, count))