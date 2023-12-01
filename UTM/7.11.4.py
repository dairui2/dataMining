# 广告效果分析
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score                        #轮廓系数指标，用来做最佳K值选择
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder       #MinMaxScaler数据预处理库，用来将数据做标准化处理；OneHotEncoder哑编码转换模块，与LatelEncoder模块配合

# 2读取数据
raw_data = pd.read_table('./ad_performance.txt', delimiter='\t')

# 3数据审查和校验
print('{:*^60}'.format('Data overview:'))
print(raw_data.head(2))                     #查看原始数据是否正常识别，有无异常信息

print('{:*^60}'.format('Data dtypes:'))
print(pd.DataFrame(raw_data.dtypes).T)      #查看数据类型分布

print('{:*^60}'.format('Data DESC:'))
print(raw_data.describe().round(2).T)       #查看数据描述性统计信息

# 缺失值审查：
na_clos = raw_data.isnull().any(axis=0)     #查看每一列是否有缺失值
print('{:*^60}'.format('NA Cols:'))
print(na_clos[na_clos==True])               #将只有结果为True(缺失)的列'平均停留时间'过滤并打印出来
print('Total number of NA lines is: {0}'.format(raw_data.isnull().any(axis=1).sum()))   #查看有缺失值的行总记录数'2'

# 相关性分析
print('{:*^60}'.format('Correlation analysis:'))
# print(A.lstrip(raw_data.corr()).round(2).T)
# print(raw_data.corr().round(2).T)

# 4数据预处理
# 删除平均停留时间列
raw_data2 = raw_data.drop(['平均停留时间'], axis=1)
# 字符串分类OneHotEncode处理
cols =['素材类型','广告类型','合作方式','广告尺寸','广告卖点']
model_ohe = OneHotEncoder(sparse=False)                 #建立OneHotEncoder对象
ohe_matrix = model_ohe.fit_transform(raw_data2[cols])   #直接转换
print(ohe_matrix[:2])
# 数据标准化
data_matrix = raw_data2.iloc[:,1:7] # 第一列为渠道编号，不是数值，无法标准化，应去掉
model_scaler = MinMaxScaler() # 建立MinMaxScaler模型对象，将数据归一到 [ 0，1 ]
data_norm = model_scaler.fit_transform(data_matrix) #标准化处理
# 合并归一化数据和one-hot编码数据
X = np.hstack((data_norm,ohe_matrix))
# 预览数据
print(X.round(2))

# 5通过平均轮廓系数检验得到最佳K-Means聚类模型
score_list = list() #建立列表存储每个K下模型的平均轮廓系数
silhouette_int = -1 #初始化的平均轮廓系数阈值
for n_clusters in range(2,8): #遍历2到8有限个组
    model_kmeans = KMeans(n_clusters = n_clusters) #建立聚类模型对象
    labels_tmp = model_kmeans.fit_predict(X) #训练聚类模型
    silhouette_tmp = silhouette_score(X,labels_tmp)#计算每个K下的平均轮廓系数
    if silhouette_tmp > silhouette_int: #如果平均轮廓系数更高
        best_k = n_clusters #保存最好的k值
        silhouette_int = silhouette_tmp #保存平均轮廓系数得分
        best_kmeans = model_kmeans # 保存模型实例对象
        cluster_labels_k = labels_tmp #保存聚类标签
    score_list.append([n_clusters,silhouette_tmp]) # 将每次K及其得分追加到列表
print('K值对应的轮廓系数为：\n',np.array(score_list))
print('最优的K值为：\n',best_k,'对应的轮廓系数为：\n',silhouette_int)

# 6针对聚类结果的特征分析
# 将原始数据与聚类标签整合
cluster_labels = pd.DataFrame(cluster_labels_k,columns = ['clusters']) # 获得训练集下的标签信息
merge_data = pd.concat((raw_data2,cluster_labels),axis = 1) # 将原始处理过的数据跟聚类标签整合
merge_data.head()
# 计算每个聚类下样本数量和占比情况
#计算每个聚类类别的样本量
clusters_count = pd.DataFrame(merge_data['渠道代号'].groupby(merge_data['clusters']).count()).T.rename({'渠道代号':'counts'})
#计算每个聚类类别的样本占比
clusters_rat = (clusters_count/ len(merge_data)).round(2).rename({'counts':'percentage'})
print('每个聚类下的样本量：\n',clusters_count,'\n\n每个聚类下的样本占比：\n',clusters_rat)

# 计算每个聚类类别内部最显著特征值
cluster_features = []  # 空列表，用于存储最终合并后的所有特征信息
for line in range(best_k):  # 读取每个类索引
    label_data = merge_data[merge_data['clusters'] == line]  # 获得特定类的数据

    part1_data = label_data.iloc[:, 1:7]  # 获得数值型数据特征
    part1_desc = part1_data.describe().round(3)  # # 得到数值型特征的描述性统计信息
    merge_data1 = part1_desc.iloc[2, :]  # 得到数值型特征的均值

    part2_data = label_data.iloc[:, 7:-1]  # 获得字符串型数据特征
    part2_desc = part2_data.describe(include='all')  # 获得字符串型数据特征的描述性统计信息
    merge_data2 = part2_desc.iloc[2, :]  # 获得字符串型数据特征的最频繁值

    merge_line = pd.concat((merge_data1, merge_data2), axis=0)  # 将数值型和字符串型典型特征沿列合并
    cluster_features.append(merge_line)  # 将每个类别下的数据特征追加到列表

# 输出完整的类别特征信息
cluster_pd = pd.DataFrame(cluster_features).T  # 将列表转化为DataFrame

# 将每个聚类类别的所有信息合并
clusters_all = pd.concat((clusters_count, clusters_rat, cluster_pd), axis=0)
print('每个类别的主要特征为：\n',clusters_all)

# 7各类别显著数值特征对比
# part1 各类别数据预处理
num_sets = cluster_pd.iloc[:6, :].T.astype(np.float64)  # 获取要展示的数据
num_sets_max_min = model_scaler.fit_transform(num_sets)  # 获得标准化后的数据

# 绘制雷达图
# part2 画布基本设置
fig = plt.figure(figsize=(6,6))  # 建立画布
ax = fig.add_subplot(111, polar=True)  # 增加子网格，注意polar参数
labels = np.array(merge_data1.index)  # 设置要展示的数据标签
cor_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']  # 定义不同类别的颜色
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)  # 计算各个区间的角度
angles = np.concatenate((angles, [angles[0]]))  # 建立相同首尾字段以便于闭合
# print('anglesanglesangles: ',angles)

labels = np.concatenate((labels,[labels[0]]))   # 新版本增加，对labels进行封闭

# part3 画雷达图
for i in range(len(num_sets)):  # 循环每个类别
    data_tmp = num_sets_max_min[i, :]  # 获得对应类数据
    data = np.concatenate((data_tmp, [data_tmp[0]]))  # 建立相同首尾字段以便于闭合
    ax.plot(angles, data, 'o-', c=cor_list[i], label=i)  # 画线

# part4 设置图像显示格式
ax.set_thetagrids(angles * 180 / np.pi, labels, fontproperties="Arial Unicode MS")  # 设置极坐标轴
ax.set_title("广告各聚类类别显著特征图", fontproperties="Arial Unicode MS")  # 设置标题放置
ax.set_rlim(-0.2, 1.2)  # 设置坐标轴尺度范围
plt.legend(loc=0)  # 设置图例位置
plt.savefig('./广告各聚类类别显著特征图')
plt.show()