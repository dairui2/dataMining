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
print(raw_data.columns['渠道代号'].replace('A',''))          #
print(A.lstrip(raw_data.corr()).round(2).T)

# 4数据预处理
