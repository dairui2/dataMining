import pandas as pd
import apriori      #自定义库

data = pd.read_csv('order_table.csv')

# 第1部分 数据预处理
# 转换为关联所用的记录模式(按照order_id 合并列concat() product_name )


# 调用自定义的Apriori做关联分析

# 关联结果报表评估

# 第2部分 Python调用R完成关联分析
from rpy2.robjects import r

# 定义R关联规则语法


# 第3部分 关联分析的结果展示
# 用到了pyecharts中的Graph库
from pyecharts import Graph

# 选取有效数据

# 汇总没个item出现的次数

# 绘图