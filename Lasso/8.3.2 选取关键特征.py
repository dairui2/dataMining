# 代码8-2
import pandas as pd
import numpy as np
from sklearn.linear_model import Lasso

income_data = pd.read_csv('./data/income_tax.csv', index_col=0)  # 读取数据

data_train = income_data.iloc[: , 0:13].copy()  # 取2005年~2019年的数据建模
data_mean = data_train.mean()
data_std = data_train.std()
data_train = (data_train - data_mean) / data_std  # 数据标准化

lasso = Lasso(alpha=1000, random_state=1234)  # 构建Lasso回归模型
lasso.fit(data_train, income_data['y'])
print('Lasso回归系数为：', np.round(lasso.coef_, 5)) # 输出结果，保留5位小数

# 计算系数非零的个数
print('系数非零个数为：', np.sum(lasso.coef_ != 0))  

mask = lasso.coef_ != 0  # 返回系数非零特征
print('系数非零特征：', income_data.columns[:-1][mask])

# 返回系数非零的数据
new_reg_data = income_data.iloc[:, 0: 13].iloc[:, mask]
new_reg_data.to_csv('./tmp/new_reg_data.csv')  # 存储数据
print('输出数据的维度为：', new_reg_data.shape)  # 查看输出数据的维度