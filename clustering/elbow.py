#x代表需要聚类数据的坐标
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt#导入库
from pandas import read_csv
from sklearn import preprocessing

Sum=np.zeros(13)# Sum用于储存肘部法则判断指标
file_name = "/Users/chenqinye/Downloads/kmeans/user-clustering.csv"

df = read_csv(file_name)
# X=X.drop(['name'])
X=df.drop(['name','word'],axis=1)
#X=df.loc[:,['level','attitude','follow']]
#X=np.array(X).reshape(1, -1)

scaler = preprocessing.MinMaxScaler(feature_range=(0,100))
# X['level'].values = scaler.fit_transform(X['level'].values)
# X['attitude'].values = scaler.fit_transform(X['attitude'].values)
# X['follow'].values = scaler.fit_transform(X['follow'].values)


X=X.values
K = range(2,15)

for i in K:
    kmeans=KMeans(n_clusters=i).fit(X)#kmeans算法拟合
    m=kmeans.labels_#取出分类得出的标签
    c=kmeans.cluster_centers_#取出每个分类中心
    for j in range(len(X)):
        c1=c[m[j]]#第j个样本所属类的中心
        x1=X[j]#第j个样本的坐标
        if i == 1:
            Sum[0]=Sum[0]+sum((x1-c1)**2)
        else:
            Sum[i-2]=Sum[i-2]+sum((x1-c1)**2)#计算判断指标
plt.figure(1)

plt.plot(np.arange(1,14),Sum )
plt.xticks(np.arange(1,14))
# plt.xlabel('Values of K')
# plt.ylabel('Inertia')
# plt.title('The Elbow Method using Inertia')
plt.show()
print(Sum)

