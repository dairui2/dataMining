# 代码8-3
import numpy as np
import pandas as pd
from gm11 import gm11  # 引入自编的灰色预测函数

# 读取经过特征选择后的数据
new_reg_data = pd.read_csv('./tmp/new_reg_data.csv', index_col=0)
# 读取数据
income_data = pd.read_csv('./data/income_tax.csv', index_col=0)
new_reg_data.index = range(2005, 2020)
new_reg_data.loc[2020] = None
new_reg_data.loc[2021] = None

c = []
p = []
# 进行灰色预测
for i in list(new_reg_data.columns):
    f = gm11(np.array(new_reg_data.loc[range(2005, 2020), i]))[0]
    c.append(gm11(np.array(new_reg_data.loc[range(2005, 2020), i]))[4])
    p.append(gm11(np.array(new_reg_data.loc[range(2005, 2020), i]))[5])
    new_reg_data.loc[2020, i] = f(len(new_reg_data) - 1)
    new_reg_data.loc[2021, i] = f(len(new_reg_data))
    new_reg_data[i] = new_reg_data[i].round(2)  # 保留两位小数

new_reg_data = pd.concat([new_reg_data, income_data['y']], axis=1)
new_reg_data.to_csv('./tmp/new_reg_data_GM11.csv')  # 结果输出
print('预测结果为：\n', new_reg_data.iloc[-2:, :6])  # 预测结果展示




# 代码8-4
# 读取灰色预测数据
from sklearn.svm import LinearSVR
from sklearn.metrics import explained_variance_score,\
mean_absolute_error, median_absolute_error, r2_score

gm11_data = pd.read_csv('./tmp/new_reg_data_GM11.csv', index_col=0)
feature = gm11_data.columns[: -1]
# 取2005~2019年的数据建模
data_train = gm11_data.loc[range(2005, 2020)].copy()
data_mean = data_train.mean()
data_std = data_train.std()
data_train = (data_train - data_mean) / data_std  # 数据标准化

x_train = np.array(data_train[feature])  # 特征数据
y_train = np.array(data_train['y'])  # 标签数据
linearsvr = LinearSVR(random_state=1234)  # 调用LinearSVR类
linearsvr.fit(x_train, y_train)
# 预测，并还原结果
x = np.array(((gm11_data[feature] - data_mean[feature]) / data_std[feature]))
gm11_data['y_pred'] = linearsvr.predict(x) * data_std['y'] + data_mean['y']
# SVR预测后保存的结果
gm11_data.to_csv('./tmp/new_reg_data_GM11_revenue.csv')
print('真实值与预测值分别为：\n', gm11_data[['y', 'y_pred']])

print('可解释方差值：',
      explained_variance_score(gm11_data['y'][:-2], gm11_data['y_pred'][:-2]))
print('平均绝对误差：',
      mean_absolute_error(gm11_data['y'][:-2], gm11_data['y_pred'][:-2]))
print('中值绝对误差：',
      median_absolute_error(gm11_data['y'][:-2], gm11_data['y_pred'][:-2]))
print('R2值：',
      r2_score(gm11_data['y'][:-2], gm11_data['y_pred'][:-2]))



# 代码8-5
from pyecharts.charts import Grid
from pyecharts.charts import Scatter, Line
from pyecharts import options as opts

# 设置x轴的值
x_data = ['2005', '2006', '2007', '2008', '2009', '2010',
          '2011', '2012', '2013', '2014', '2015', '2016',
          '2017', '2018', '2019', '2020', '2021']
# 绘制线
line = (Line(init_opts=opts.InitOpts(width='800px', height='310px'))
   # 设置x轴
   .add_xaxis(x_data)
   # 真实值的线
   .add_yaxis('真实值', gm11_data['y'].tolist(),
              label_opts=opts.LabelOpts(is_show=False)) 
   # 预测值的线
   .add_yaxis('预测值', gm11_data['y_pred'].tolist(),
              label_opts=opts.LabelOpts(is_show=False))
    )
# 绘制点
scatter = (
    Scatter(init_opts=opts.InitOpts(width='800px', height='310px'))
    .add_xaxis(x_data)
   # 真实值的点
    .add_yaxis('真实值', gm11_data['y'].tolist(), 
               label_opts=opts.LabelOpts(is_show=False), 
               symbol_size=10, symbol='diamond')
   # 预测值的点
    .add_yaxis('预测值', gm11_data['y_pred'].tolist(), 
               label_opts=opts.LabelOpts(is_show=False), 
               symbol_size=10, symbol='pin')
    # 标题
    .set_global_opts(
        title_opts=opts.TitleOpts(title='真实值与预测值对比'),
        yaxis_opts=opts.AxisOpts(name='企业所得税（万元）',
                                 name_location='middle',
                                 name_gap=70),
        xaxis_opts=opts.AxisOpts(name='年份',
                         name_location='middle',
                         name_gap=30),
        )
    )
# 叠加图
scatter.overlap(line)
grid=Grid()
# 修改相对位置
grid.add(scatter, grid_opts=opts.GridOpts(pos_top='10%', pos_left='12%',
                                         pos_bottom='35%'))
grid.render('./tmp/真实值与预测值对比.html')
