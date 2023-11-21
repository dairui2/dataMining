from K_Means import KM_data


kmeans_analysis = KM_data[['R','F','M','类别']]
# kmeans_analysis.columns=['R','F','M','means']
# kmeans_analysis.groupby(kmeans_analysis['means'])
# kmeans_analysis.groupby(['means']).mean()
# aaa = kmeans_analysis.groupby(['means'])[['R','F','M',]].mean()
aaa = kmeans_analysis.groupby(['类别'])[['R','F','M',]].mean()

#重命名列
# kmeans_analysis.columns = ['R','F','M']
# del kmeans_analysis["用户id"]
# kmeans_analysis2 = kmeans_analysis.drop('用户id',axis=1)
print(aaa)
print(KM_data.groupby(['类别'])[['R','F','M',]].mean())
print(KM_data.groupby(KM_data['类别'])[['R','F','M',]].mean())
