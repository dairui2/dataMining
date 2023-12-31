from wordcloud import WordCloud
import matplotlib.pyplot as plt

with open('./电商客服对话日志.txt', 'r', encoding='utf8', errors='ignores') as f:

# with open('/Users/dai/Downloads/stopword.txt', 'r', encoding='utf8', errors='ignores') as f:
    txt = f.read()

# wc = WordCloud(font_path='/System/Library/Fonts/SFNSMono.ttf', mode ='RGBA', background_color='white')  # 创建WordCloud对象
wc = WordCloud(font_path='/System/Library/Fonts/STHeiti Light.ttc', mode ='RGBA', background_color='white')  # 创建WordCloud对象


wc.generate(txt)    # 由文本生成词云，但此时并没有生成图片文件

wc.to_file('/Users/dai/Downloads/001.png')     # 保存词云到文件中

#绘制词云图
plt.imshow(wc)      #将生成的词云进行处理，但是此时不能显示
plt.axis('off')     #不显示坐标轴

#显示生成词云图
plt.show()          #通过matplotlib.pyplot模块显示图片