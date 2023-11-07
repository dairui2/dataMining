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
# c	    连词	        u	助词	        xc	其他虚词	    w,x	    标点符号
# PER	人名	        LOC	地名	        ORG	机构名	    TIME	时间
# // jieba词性对照表
# - a 形容词
#     - ad 副形词
#     - ag 形容词性语素
#     - an 名形词
# - b 区别词
# - c 连词
# - d 副词
#     - df
#     - dg 副语素
# - e 叹词
# - f 方位词
# - g 语素
# - h 前接成分
# - i 成语
# - j 简称略称
# - k 后接成分
# - l 习用语
# - m 数词
#     - mg
#     - mq 数量词
# - n 名词
#     - ng 名词性语素
#     - nr 人名
#     - nrfg
#     - nrt
#     - ns 地名
#     - nt 机构团体名
#     - nz 其他专名
# - o 拟声词
# - p 介词
# - q 量词
# - r 代词
#     - rg 代词性语素
#     - rr 人称代词
#     - rz 指示代词
# - s 处所词
# - t 时间词
#     - tg 时语素
# - u 助词
#     - ud 结构助词 得
#     - ug 时态助词
#     - uj 结构助词 的
#     - ul 时态助词 了
#     - uv 结构助词 地
#     - uz 时态助词 着
# - v 动词
#     - vd 副动词
#     - vg 动词性语素
#     - vi 不及物动词
#     - vn 名动词
#     - vq
# - x 非语素词
# - y 语气词
# - z 状态词
#     - zg



# jieba.enable_paddle()   # 启动paddle模式，飞桨(PaddlePaddle)深度学习框架。 0.40版之后开始支持，早期版本不支持
# strs=["我来到北京清华大学","乒乓球拍卖完了杭研大厦碳达峰","中国科学技术大学量子纠缠不忘初心"]
strs = pseg.cut("我来到北京:清华大学, 乒乓球拍卖完了杭研大厦碳达峰;中国科学技术大学'量子纠缠'不忘初心。",use_paddle=True)
for str, flag in strs:
    if flag  in ['m', 'c', 'q', 'u', 'r', 't', 'd','p','w','x','ul']:   ##数量词,连词,量词,助词,代词,时间,副词,介词,标点符号,标点符号,时态助词
    # seg_list = pseg.cut(str,use_paddle=True) # 使用paddle模式
    # print("Paddle Mode: " + '|'.join(list(seg_list)))
        print('%s %s' % (str, flag),'----------------')

strs = pseg.cut("我来到北京:清华大学, 乒乓球拍卖完了杭研大厦碳达峰;中国科学技术大学'量子纠缠'不忘初心。",use_paddle=True)
for str, flag in strs:
    if flag not in ['m', 'c', 'q', 'u', 'r', 't', 'd','p','w','x','ul']:   ##数量词,连词,量词,助词,代词,时间,副词,介词,标点符号,标点符号,时态助词
    # seg_list = pseg.cut(str,use_paddle=True) # 使用paddle模式
    # print("Paddle Mode: " + '|'.join(list(seg_list)))
        print('%s %s' % (str, flag))

