import  jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt

with open('./电商客服对话日志.txt', 'r', encoding='utf8', errors='ignores') as f:
    txt = f.read()
#添加自定义的词
jieba.add_word('iPhone 13')

with open('./stopword.txt', 'r', encoding='utf8', errors='ignores') as f:
    stopwordlist = f.readlines()    #读取停用词到一个列表中
    maped = map(lambda  x: str(x).strip(), stopwordlist)    #删除停用词的前后空白，map是映射函数，对列表中的每一行元素都进行处理(删除前后空白).
    stopwordlist = list(maped)

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


# wc = WordCloud(font_path='/System/Library/Fonts/STHeiti Light.ttc', mode ='RGBA', background_color='white')  # 创建WordCloud对象

# wc.generate(word)    # 由文本生成词云，但此时并没有生成图片文件

# wc.to_file('/Users/dai/Downloads/000.png')     # 保存词云到文件中

for word  in words():
    wc = WordCloud(font_path='/System/Library/Fonts/STHeiti Light.ttc', mode='RGBA',
                   background_color='white')  # 创建WordCloud对象
    wc.generate(word)
    wc.to_file("/Users/dai/Downloads/_" + category + ".jpg")

#绘制词云图
plt.imshow(wc)      #将生成的词云进行处理，但是此时不能显示
plt.axis('off')     #不显示坐标轴

#显示生成词云图
plt.show()          #通过matplotlib.pyplot模块显示图片