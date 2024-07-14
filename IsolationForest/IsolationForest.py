from sklearn.preprocessing import OrdinalEncoder
from sklearn.ensemble import IsolationForest
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # 导入3D样式库

# 数据准备
raw_data = pd.read_csv('outlier.txt',sep=',')  # 读取数据
raw_data.shape

# 去除全部为空的特征
data_dropna = raw_data.dropna(axis='columns',how='all')
data_dropna = data_dropna.drop(['clientId'],axis=1)
data_dropna.shape

# 填充NA列
# 找到NA列
cols_is_na = data_dropna.isnull().any()
na_cols = [cols_is_na.index[ind]
           for ind, na_result in enumerate(cols_is_na) if na_result == True]
print(data_dropna[na_cols].dtypes)
# 填充NA列
print(data_dropna[na_cols].head())
#print(type(data_dropna[na_cols].iloc[2,3]))
fill_rules = {'newVisits': 0, 'pageviews': 0, 'isVideoAd': False, 'isTrueDirect': False}
data_fillna = data_dropna.fillna(fill_rules)
print(data_fillna.isnull().any().sum())

# 拆分数值特征和字符串特征
str_or_num = (data_fillna.dtypes=='object')
str_cols = [str_or_num.index[ind]
           for ind, na_result in enumerate(str_or_num) if na_result == True]
string_data = data_fillna[str_cols]
num_data = data_fillna[[i for i in str_or_num.index if i not in str_cols]]

# 分类特征转换为数值型索引
model_oe = OrdinalEncoder()
string_data_con = model_oe.fit_transform(string_data)
string_data_pd = pd.DataFrame(string_data_con,columns=string_data.columns)

# 合并原数值型特征和onehotencode后的特征
feature_merge = pd.concat((num_data,string_data_pd),axis=1)

# 异常点检测
model_isof = IsolationForest(n_estimators=20, n_jobs=1)
outlier_label = model_isof.fit_predict(feature_merge)

# 异常结果汇总
outlier_pd = pd.DataFrame(outlier_label,columns=['outlier_label'])
data_merge = pd.concat((data_fillna,outlier_pd),axis=1)
outlier_count = data_merge.groupby(['outlier_label'])['visitNumber'].count()
print('outliers: {0}/{1}'.format(outlier_count.iloc[0], data_merge.shape[0]))  # 输出异常的结果数量

# 统计每个渠道的异常情况
def cal_sample(df):
    data_count = df.groupby(['source'],as_index=False)['outlier_label'].count()
    return data_count.sort_values(['outlier_label'],ascending=False)

# 取出异常样本
outlier_source = data_merge[data_merge['outlier_label']==-1]
outlier_source_sort = cal_sample(outlier_source)
# 取出正常样本
normal_source = data_merge[data_merge['outlier_label']==1]
normal_source_sort = cal_sample(normal_source)
# 合并总样本
source_merge = pd.merge(outlier_source_sort,normal_source_sort,on='source',how='outer')
source_merge = source_merge.rename(index=str, columns={'outlier_label_x':'outlier_count','outlier_label_y':'normal_count'})
source_merge=source_merge.fillna(0)
# 计算异常比例
source_merge['total_count'] = source_merge['outlier_count']+source_merge['normal_count']
source_merge['outlier_rate'] = source_merge['outlier_count']/(source_merge['total_count'])
print(source_merge.sort_values(['total_count'],ascending=False).head())

# 异常点图形展示
# 设置中文字体
plt.rcParams['font.sans-serif'] = 'Arial Unicode MS'
plt.style.use('ggplot')  # 使用ggplot样式库
fig = plt.figure(figsize=(10, 8))  # 创建画布对象
# 画图
ax = fig.add_subplot(111, projection='3d')
ax.scatter(source_merge['outlier_count'], source_merge['total_count'], source_merge['outlier_rate'],
           s=100, edgecolors='k', c='r', marker='o',alpha=0.5)
ax.set_xlabel('outlier_count')
ax.set_ylabel('total_count')
ax.set_zlabel('outlier_rate')
plt.title('网站广告流量的离群点分布')  # 设置图像标题
plt.show()
