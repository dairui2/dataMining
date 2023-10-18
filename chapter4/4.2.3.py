import jieba
from wordcloud import WordCloud
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# 读取数据源文件
with open('/Users/dai/Downloads/玩转Python网络爬虫作者.txt', 'r', encoding='utf8', errors='ignores') as f:
    txt = f.read()

# 读取停用词文件
with open('/Users/dai/Downloads/stopword.txt', 'r', encoding='utf8', errors='ignores') as f:

    # 读取停用词到一个列表中
    stopwordlist = f.readlines()

    # 删除停用词的前后空白，map是映射函数，对列表中的每一行元素都进行处理(删除前后空白).
    maped = map(lambda  x: str(x).strip(), stopwordlist)
    stopwordlist = list(maped)

    # 将列表对象转为集合对象
    stopword_set = set(stopwordlist)
    # print(stopword_set)

words = jieba.cut(txt)  #精确模式

custom_mask = np.array(Image.open('/Users/dai/Pictures/apple.jpg'))

# wc = WordCloud(font_path='/System/Library/Fonts/SFNSMono.ttf', width=800, height=600, mode ='RGBA', background_color='white')  # 创建WordCloud对象
wc = WordCloud(font_path='/System/Library/Fonts/STHeiti Light.ttc', #支持中文的字体
               width=600, height=800, mode ='RGBA',
               stopwords=stopword_set, #过滤停用词
                mask = custom_mask,
               background_color='white')  # 创建WordCloud对象

wc.generate(txt)    # 由文本生成词云，但此时并没有生成图片文件

wc.to_file('/Users/dai/Downloads/001.png')     # 保存词云到文件中

#绘制词云图
plt.imshow(wc)      #将生成的词云进行处理，但是此时不能显示
plt.axis('off')     #不显示坐标轴

#显示生成词云图
plt.show()          #通过matplotlib.pyplot模块显示图片