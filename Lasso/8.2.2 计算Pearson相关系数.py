# 代码8-1
import numpy as np
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import HeatMap

# 读取数据
income_data = pd.read_csv('./data/income_tax.csv', index_col=0)
# 保留两位小数
data_cor = np.round(income_data.corr(method = 'pearson'), 2)

y_data = list(data_cor.columns)  # 获取y轴标签
x_data = list(data_cor.index)  # 获取x轴标签
# 相关系数矩阵转为列表
values = data_cor.values.tolist()
# 对应相关系数的位置
value = [[i, j, values[i][j]] for i in range(len(x_data))
         for j in range(len(y_data))]
heatmap = (
    # 导入热力图
    HeatMap()
    # 设置x轴
    .add_xaxis(x_data)
    # 设置y轴
    .add_yaxis(
        '', y_data, 
        value, 
        label_opts=opts.LabelOpts(
            is_show=True, position='inside'),
    )
    .set_global_opts(
        # 设置标题
        title_opts=opts.TitleOpts(title='相关系数热力图'),
        # 设置图例
        visualmap_opts=opts.VisualMapOpts(
                       is_show = False, pos_bottom='center',
                       max_=1, min_=0.9
        )
    )
)  
heatmap.render('./tmp/相关系数热力图.html')


