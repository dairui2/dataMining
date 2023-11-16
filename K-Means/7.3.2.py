# Z-score数据标准化：标准化数据 = (原数据 - 均值)/标准差;  (data - data.mean())/data.std()
import pandas as pd

# 1读入数据
datafile ='./data/某移动公司客户信息预处理.xlsx'    #读入预处理的数据
data = pd.read_excel(datafile)
print(data.head(10))

# 2提取特征并更改索引
cdata = data[['R(最后一次消费距提数提数日的时间)', 'F(月均消费次数)', 'M(月均消费金额)']]      #提取3列
cdata.index = data['用户id']          #修改索引为 用户id，使后续结果能与用户id一一对应，方便定位具体用户
print(cdata.head())

# 3标准化
z_cdata = (cdata - cdata.mean())/cdata.std()
z_cdata.columns = ['R(标准化)', 'F(标准化)', 'M(标准化)']
print(z_cdata.head())