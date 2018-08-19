import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
import numpy as np 
from sklearn.cluster import KMeans


# import pandas as pd 
# from sklearn.cluster import KMeans
# from sklearn import preprocessing

x = np.array([[1,2],
	[1.2,1.4],[2,3.2],[6,7],[7.6,8],[9,9.9]])

# plt.scatter(x[:,0],x[:,1],marker="*",s=100)
# plt.show()

markers = ["o","*",".","..","^","s"]

colors = ["g","r","c","b","k","y"]

clf = KMeans(n_clusters=2)
clf.fit(x)

centeroids = clf.cluster_centers_
labels = clf.labels_
print labels

# ,marker=markers[labels[i]]

for i in range(len(x)):
	plt.scatter(x[i][0],x[i][1],marker=markers[labels[i]],color = colors[labels[i]],s=150)
	print colors[labels[i]]
	plt.scatter(centeroids[:,0],centeroids[:,1],s=150,linewidth=5)
plt.show()


