import jieba
import jieba.posseg as pseg
# words = pseg.cut("我爱北京天安门") #jieba默认模式
#  jieba.enable_paddle() #启动paddle模式。 0.40版之后开始支持，早期版本不支持

# words = pseg.cut("科学家在中国科学技术大学不忘初心研究量子纠缠",use_paddle=True) #paddle模式
# for word, flag in words:
#    print('%s %s' % (word, flag))

# 标签	含义	        标签	含义	        标签	含义	        标签	    含义
# n	    普通名词	    f	方位名词	    s	处所名词	    t	    时间
# nr	人名	        ns	地名	        nt	机构名	    nw	    作品名
# nz	其他专名	    v	普通动词	    vd	动副词	    vn	    名动词
# a	    形容词	    ad	副形词	    an	名形词	    d	    副词
# m	    数量词	    q	量词	        r	代词	        p	    介词
# c	    连词	        u	助词	        xc	其他虚词	    w	    标点符号
# PER	人名	        LOC	地名	        ORG	机构名	    TIME	时间

# jieba.enable_paddle()   # 启动paddle模式，飞桨(PaddlePaddle)深度学习框架。 0.40版之后开始支持，早期版本不支持
# strs=["我来到北京清华大学","乒乓球拍卖完了杭研大厦碳达峰","中国科学技术大学量子纠缠不忘初心"]
strs = pseg.cut("我来到北京清华大学, 乒乓球拍卖完了杭研大厦碳达峰, 中国科学技术大学量子纠缠不忘初心",use_paddle=True)
for str, flag in strs:
    # seg_list = pseg.cut(str,use_paddle=True) # 使用paddle模式
    # print("Paddle Mode: " + '|'.join(list(seg_list)))
    print('%s %s' % (str, flag))

