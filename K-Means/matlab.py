# 数据可视化及数据分析
import matplotlib.pyplot as plt
from pre_proccess import data, gender, age
from K_Means import KM_data, result

# 1.a对预处理好的数据的性别和年龄进行可视化处理
# 设置中文字体
plt.rcParams['font.sans-serif'] = 'Arial Unicode MS'
# 1.a绘制性别-人数柱状图
plt.bar(gender.index, gender, width=0.5, color='c')
# 完善图表信息
plt.xticks(range(1,3),['男','女'])    #设置x轴刻度值对应range=[1, 2]
plt.xlabel('性别', fontsize=12)
plt.ylabel('人数', fontsize=12)
plt.title('性别-人数统计图', fontsize=14)
# 保存图形
plt.savefig('./data/性别-人数统计图',dpi=128)
# 展示图形
# plt.show()

# 1.b绘制年龄-人数折线图
# 按照索引年龄排序,否则绘制出的折线图是混乱的
age = age.sort_index()
# 设置图像大小，因为数据比较密集，需要更大尺寸的图以看清数据分布
plt.figure(figsize=(10,6))
# 设置中文字体
plt.rcParams['font.sans-serif'] = 'Arial Unicode MS'
# 绘制折线图
plt.plot(age.index, age)
# 完善图表
plt.xticks(range(0,80,5), fontsize=12)
plt.yticks(range(2,20), fontsize=12)
plt.grid(ls=':',alpha=0.8)
plt.xlabel('年龄', fontsize=12)
plt.ylabel('人数', fontsize=12)
plt.title('年龄-人数统计图', fontsize=14)
# 填充折线与x轴间的颜色，使结果更直观，颜色在x轴覆盖范围用age.index标识
plt.fill_between(age.index, age, color='c', alpha=0.3)
# 保存图形
plt.savefig('./data/年龄-人数统计图',dpi=128)
# 展示图形
# plt.show()


# 2绘制聚类结果统计柱状图
# 分组统计求均值
kmeans_analysis = KM_data.groupby(['类别'])[['R','F','M',]].mean()
# 重命名列
kmeans_analysis.columns=['R','F','M']
print(kmeans_analysis)
# 设置中文字体
plt.rcParams['font.sans-serif'] = 'Arial Unicode MS'
# 绘制柱状图
kmeans_analysis.plot(kind='bar', rot=0, yticks=range(-1,9))
# 完善图表
plt.title('聚类结果柱状图', fontsize=14)
plt.xlabel('类别', fontsize=12)
plt.xticks(range(0,4), ['第0类','第1类','第2类','第3类'], fontsize=12)
plt.grid(axis='y',color='grey',linestyle='--',alpha=0.5)
plt.ylabel('R,F,M 3个指标均值')

# 保存图形
plt.savefig('./data/聚类结果统计柱状图',dpi=128)
# 展示图形
# plt.show()


# 3对聚类结果中类别人数进行可视化处理
# 设置中文字体
plt.rcParams['font.sans-serif'] = 'Arial Unicode MS'
# 绘制柱状图
result.plot(kind='bar', y='各类别人数', rot=0)    #使用DataFrame形变量自带的plot()函数来绘图，指定绘图类型为bar
# 完善图表
plt.xlabel('类别', fontsize=12)
plt.ylabel('人数', fontsize=12)
plt.title('聚类结果各类别人数统计图', fontsize=14)
# 保存图形
plt.savefig('./data/聚类结果各类别人数统计图',dpi=128)


# 4绘制客户群特征雷达图
#将values转化为数组
center_num = kmeans_analysis.values
print(center_num)

import numpy as np
# 创建Figure实例
fig = plt.figure(figsize=(10, 8))
# 设置极坐标模式
ax = fig.add_subplot(111, polar=True)
# 存储特征标签
feature =['R(最后一次消费距提数提数日的时间)','F(月均消费次数)','M(月均消费金额)']
# 统计特征数
N = len(feature)

# 遍历数组以绘图
for i, v in enumerate(center_num):
    angles = np.linspace(0, 2*np.pi, N, endpoint=False)             #设置雷达图的角度，用于评分切开一个圆面
    center = np.concatenate((v[:], [v[0]]))                         #为了使雷达图一圈封闭起来，需要执行下面的步骤
    angles = np.concatenate((angles, [angles[0]]))
    ax.plot(angles, center, 'o-', linewidth=2, label='第%d类'%(i))    #绘制折线图
    ax.fill(angles, center, alpha=0.25)                              #填充颜色

    ang = angles * 180/np.pi                                         #添加每个特征的标签
    ax.set_thetagrids(ang[:-1], feature)                             #添加每个特征的标签

    plt.title('客户群特征分析图', fontsize=14)                          #添加标题
    ax.grid()                                                        #添加网格线
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1.0), shadow=True, fontsize=12)   #设置图例
    plt.savefig('./data/客户群特征分析图', dpi=128, bbox_inches='tight')                    #保存图形，指定bbox_inches来裁剪图形多余空白区域

# 显示图形
plt.show()