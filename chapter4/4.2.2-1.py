from wordcloud import WordCloud

with open('/Users/dai/Downloads/玩转Python网络爬虫作者.txt', 'r', encoding='utf8', errors='ignores') as f:

# with open('/Users/dai/Downloads/stopword.txt', 'r', encoding='utf8', errors='ignores') as f:
    txt = f.read()

# wc = WordCloud(font_path='/System/Library/Fonts/SFNSMono.ttf', mode ='RGBA', background_color='white')  # 创建WordCloud对象
wc = WordCloud(font_path='/System/Library/Fonts/STHeiti Light.ttc', mode ='RGBA', background_color='white')  # 创建WordCloud对象


wc.generate(txt)    # 由文本生成词云，但此时并没有生成图片文件

wc.to_file('/Users/dai/Downloads/001.png')     # 保存词云到文件中
