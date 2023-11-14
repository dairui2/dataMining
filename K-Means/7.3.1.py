import pandas as pd
# import matplotlib.pyplot as plt
# from sklearn.cluster import KMeans
# import scikit-learn

# 3读入数据
datafile = "./data/RFM聚类分析.xlsx"
data = pd.read_excel(datafile)

# 4数据探查，观察前10行数据
print(data.head(10))

# 4.2查看行列数统计
print(data.shape)   #(301, 12)

# 4.3查看数据整体描述信息
print(data.info())

# 4.4查看各列数据的汇总统计集合
print(data.describe())

# 5数据缺失值处理，统计数据缺失值
print(data.isnull().sum())

# 6检测和过滤异常值
print((data == 0).any())
