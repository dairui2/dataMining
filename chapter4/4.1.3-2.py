import jieba

# source = '来到杨过曾经生活过的地方，小龙女动情地说，我也想过过儿过过的生活'
# # source2 ='关于牙膏，我只用中华为了节省每次用5g'
source2 ='他来到了网易杭研大厦'
source3 = '我来到北京清华大学","乒乓球拍卖完了","中国科学技术大学的科学家不忘初心的研究量子纠缠技术","关于牙膏我只用中华为了节省每次只用5g'
#
#添加自定义的词
# jieba.add_word('过过')
#
# print("|".join(jieba.cut(source)))  #精确模式，试图将句子最精确地切开，适合文本分析；
# print("|".join(jieba.cut(source, cut_all=True)))    #全模式，把句子中所有的可以成词的词语都扫描出来, 速度非常快，但是不能解决歧义；
# print("|".join(jieba.cut_for_search(source)))       #搜索引擎模式，在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词。


print("|".join(jieba.cut(source2)))  #精确模式 = source2, cut_all=False
print("|".join(jieba.cut(source2, cut_all=True)))    #全模式
# print("|".join(jieba.cut(source2, cut_all=False)))    #精确模式
print("|".join(jieba.cut_for_search(source2)))       #搜索引擎模式

print("|".join(jieba.cut(source3)))  #精确模式 = source2, cut_all=False
print("|".join(jieba.cut(source3, cut_all=True)))    #全模式
print("|".join(jieba.cut_for_search(source3)))       #搜索引擎模式