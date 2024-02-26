import pandas as pd
import apriori      #自定义库

data = pd.read_csv('order_table.csv')

# 第1部分 数据预处理
# 转换为关联所用的记录模式(按照order_id 合并列concat() product_name )
order_ids = pd.unique(data['order_id'])
# print(order_ids)
order_records = [data[data['order_id'] == each_id]['product_name'].tolist() for each_id in order_ids]
# print(order_records)

# 调用自定义的Apriori做关联分析
minS = 0.01     #定义最小支持度阈值
minC = 0.05     #定义最小置信度阈值
L, suppData = apriori.apriori(order_records, minSupport=minS)               #计算得到满足最小支持度的规则
rules = apriori.generateRules(order_records, L, suppData, minConf=minC)     #计算满足最小置信度的规则

# 关联结果报表评估如下
model_summary = 'data record: {1} \ nassociation rules count: {0}'  #展示数据集记录数和满足阈值定义的规则数量
print(model_summary.format(len(rules), len(order_records)), '\n', '-'*60)   #使用str.format做格式化输出
rules_all = pd.DataFrame(rules, columns=['item1', 'item2', 'instance', 'support', 'confidence', 'lift'])    #创建频繁规则数据框
rules_sort = rules_all.sort_values(['lift'], ascending=False)
print(rules_sort.head(10))

# 第2部分 Python调用R完成关联分析
from rpy2.robjects import r
# 定义R关联规则语法
r_script = '''
    library(arules)
    data <- read.transactions("order_table.csv", format = "single", header=TRUE, cols = c("order_id", "product_name"), sep=",")
    init_rules <- apriori(data, parameter = list(support = 0.01, confidence = 0.05, minlen = 2))
    sort_rules <- sort(init_rules, by = "lift")
    rules_pd <- as(sort_rules, "data.frame")
'''
rules_pd = r(r_script)
print(rules_pd)

# 第3部分 关联分析的结果展示
# 用到了pyecharts中的Graph库
from pyecharts.charts import Graph

# 选取有效数据
rules_sort_filt = rules_sort[rules_sort['lift']>1]      #只取有效规则
display_data = rules_sort_filt.iloc[:, :3]              #取出前3列，前项，后项和实例数

# 汇总每个item出现的次数
item1 = display_data[['item1', 'instance']].rename(index=str, columns={"item1": "item"})
item2 = display_data[['item2', 'instance']].rename(index=str, columns={"item2": "item"})
item_concat = pd.concat((item1, item2), axis=0)
item_count = item_concat.groupby(['item'])['instance'].sum()

# 取出规则最多的TOP N items进行展示
control_num = 10
top_n_rules = item_count.sort_values(ascending=False).iloc[:control_num]
top_n_items = top_n_rules.index
top_rules_list = [all((item1 in top_n_items, item2 in top_n_items)) for item1, item2 in zip(display_data['item1'], display_data['item2'])]
top_display_data = display_data[top_rules_list]

# 绘图
node_data = top_n_rules/100         #圆的尺寸太大，等比缩小100倍
nodes = [{"name": ('').join(i[0]), "symbolSize": i[1], "value": j} for i, j in zip(node_data.to_dict().items(), item_count)]
#创建边以及边权重数据
edges = [{"source": ('').join(i), "target": ('').join(j), "value": k} for i, j , k in top_display_data.values]
#创建关系图
# graph = Graph("商品关系结果图", width=800, height = 800)
# graph.add("商品名称", nodes, edges, is_label_show=True, is_focusnode=True, is_roam=True,
#           repulsion=8000, graph_layout='circular',
#           line_width=2, label_text_size=14, is_random=True)
# graph
from pyecharts import options as opts  # 导入opts模块
graph = (
    Graph(init_opts=opts.InitOpts(width="900px", height="900px"))
    .add("商品名称", nodes, edges, repulsion=8000, layout='circular', linestyle_opts=opts.LineStyleOpts(width=2), label_opts=opts.LabelOpts(is_show=True))
    .set_global_opts(title_opts=opts.TitleOpts(title="商品捆绑/关联图"))
)
graph.render('association_analysis.html')