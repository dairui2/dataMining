# K-Means聚类算法对客户进行分析
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from Z_score import z_cdata
from pre_proccess import data

# 1确定K值
# 构建肘部法模型
SEE = []        #SEE用来记录每次聚类后样本到中心的欧氏距离
for k in range(1, 9):       #分别聚类为1～8个类别
    estimator = KMeans(n_clusters=k)
    estimator.fit(z_cdata)
    SEE.append(estimator.inertia_)       #样本到最近聚类中心的距离平方之和

# 设置x轴数据
x = range(1, 9)
# 设置字体
plt.rcParams['font.sans-serif'] = ['Songti SC']
# plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

# 开始绘图
plt.plot(x, SEE, 'o-')
plt.xlabel('k值')
plt.ylabel('SEE')
plt.title('肘部图')
# plt.show()
plt.savefig('./data/肘部图')

# 2K-Means聚类分析
kmodel = KMeans(n_clusters=4, max_iter=100,n_init=10, random_state=0)     #n_clusters初始化类时指定分类数；max_iter最大迭代次数；random_state指定质心初始化随机状态为0
kmodel.fit(z_cdata)

# 3提取整合聚类结果
print(kmodel.labels_)               # 查看每条数据所属的聚类类别
print(kmodel.cluster_centers_)      #查看聚类中心坐标

# 整合构建聚类结果
r1 = pd.Series(kmodel.labels_).value_counts()       #统计属于各个类别的数据个数
r2 = pd.DataFrame(kmodel.cluster_centers_)          #找出聚类中心

result = pd.concat([r2, r1], axis=1)                #默认情况下axis=0,按index(索引)或者按照行进行纵向连接，当axis=1时按照columns(列)进行横向连接；连接后得到聚类中心对应类别下的数目
result.columns=['R', 'F', 'M'] + ['各类别人数']       #重命名表头
print(result)

# 4分析两种K值(3 or 4)结果

# 5将类别与客户数据对应
#连接kmodel.labels与z_cdata
KM_data = pd.concat([z_cdata, pd.Series(kmodel.labels_, index=z_cdata.index)], axis=1)
data1 = pd.concat([data, pd.Series(kmodel.labels_, index=data.index)], axis=1)

#重命名列名
data1.columns=list(data.columns) + ['类别']
KM_data.columns=['R', 'F', 'M'] + ['类别']
print(KM_data.head())
print(data1.head())

# 6保存聚类分析好的数据
# 增加用户id列与列别标签相对应
KM_data['用户id'] = KM_data.index
# 保存KM_data
output_file_path = './data/类别-客户信息(标准化数据)对应.xlsx'
KM_data.to_excel(output_file_path, index=False)
# 保存data1
output_file_path = './data/类别-客户信息(预处理数据)对应.xlsx'
data1.to_excel(output_file_path, index=False)
# 保存result
output_file_path = './data/聚类结果统计.xlsx'
result.to_excel(output_file_path, index=False)

# del KM_data['用户id']