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

# 6检测和过滤异常值: 统计有0值的数据列;统计空字符串的数据列 print((data == ' ').any())
print((data == 0).any())
# user_id                 False
# gender                   True
# last_pay_time           False
# pay_num                  True
# pay_times                True
# last_month_traffic       True
# local_trafffic_month     True
# local_caller_time        True
# service1_caller_time     True
# service2_caller_time     True
# online_time             False
# age                      True
# 除了user_id，last_pay_time，online_time 3列外，其他列都存在0值。为了进一步观察数据，需要对每一列的0值的个数进行统计。

# 统计每一列0值数据的个数
# 遍历data的每一列
for col in data.columns:
    # count从0开始累加
    count = 0
    # 如果值为0，则count累加
    count = [count + 1 for x in data[col] if x == 0]
    # 输出该列的0值个数
    print(col + ' ' + str(sum(count)))
# user_id 0
# gender 13
# last_pay_time 0
# pay_num 2
# pay_times 6
# last_month_traffic 205
# local_trafffic_month 68
# local_caller_time 92
# service1_caller_time 164
# service2_caller_time 101
# online_time 0
# age 12
# 在存在0值的列中，gender，pay_num，pay_times，age这4列的0值个数很少，其他列0值的个数很多，可以初步猜测这4列的0值可能是不正常的统计数值；根据其他列的数据类型可以判断，其他列出现0值是合理的。
# 因为性别和年龄不存在0值，消费次数和消费金额可以同时为0，但是不能有一项为0，而另一项不为0的情况。

# 调出gender与age两列都为0值的行
index1 = (data['gender'] == 0 ) & (data['age'] == 0)
print(data[index1])

# 调出pay_num，pay_times两者有一项为0值的行
index2 = (data['pay_num'] == 0) | (data['pay_times'] == 0)
print(data[index2])

# 将以上两种情况结合在一起，将无效数据行调出来统计
index3 = (data['gender'] == 0 ) & (data['age'] == 0) | (data['pay_num'] == 0) | (data['pay_times'] == 0)
print(data[index3])     #[13 rows x 12 columns]

# 删除13条记录
data = data.drop(data[index3].index)
print(data.shape)       #(288, 12)

# 7处理重复值
# 统计重复值
print(data.duplicated().sum())              #0
# 统计user_id这一列的重复值
print(data.duplicated(['user_id']).sum())   #2

# 删除重复值
data = data.drop_duplicates(['user_id'])
print(data.shape)                           #(286, 12)

# 统计不同性别和不同年龄的人数
gender = pd.Series(data['gender']).value_counts()
age = pd.Series(data['age']).value_counts()
# print(gender, age)

# 8属性规约

# 9计算特征R, F, M
# 10保存预处理完成的数据