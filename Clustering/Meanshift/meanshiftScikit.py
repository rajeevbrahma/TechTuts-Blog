import numpy as np
from sklearn.cluster import MeanShift
from sklearn.datasets.samples_generator import make_blobs
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import style
style.use("ggplot")

# centers = [[1,2],[2,3]]
# # ,centers=centers
# X = make_blobs(n_samples = 10,centers=centers,cluster_std=1)



X = np.array([[1,2,1],
			  [1,3,2],
			  [2,3,3],
			  [3,4,1],
			  [6,8,4],
			  [7,8,5],
			  [8,7,6],
			  [9,10,11],
			  [10,11,9],
			  [11,12,5],
			  [10,11.5,4]])

ms = MeanShift()
ms.fit(X)
labels = ms.labels_
cluster_centers = ms.cluster_centers_
print(cluster_centers)

n_clusters = len(np.unique(labels))
# or
n_clusters = len(set(labels))

print "clusters:",n_clusters

colors = ["r","g","b","c","k","y","m"]
fig = plt.figure()
ax = fig.add_subplot(111,projection="3d")


for i in range(len(X)):
	ax.scatter(X[i][0],X[i][1],X[i][2],c=colors[labels[i]],marker="o")

ax.scatter(cluster_centers[:,0],cluster_centers[:,1],cluster_centers[:,2],marker="x",color='m',s=150)	

plt.show()


