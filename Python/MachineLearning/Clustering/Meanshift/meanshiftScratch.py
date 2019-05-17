import matplotlib.pyplot as plt 
from matplotlib import style 

import numpy as np 


x = np.array([[1,2],[1.3,2.1],[1.5,2.5],[1.9,3],[2,5],
	[2.7,4],[6,7.8],[6.9,8.6],[7.2,9],[8,9.6],[2,3],[5,6],[4.5,3.2]])

markers = ["o","*",".","..","^","s"]

colors = ["g","r","c","b","k","y"]


class Mean_Shift:
	def __init__(self, radius=4):
		self.radius = radius
	
	def fit(self, data):
		# initialising the centroid dictionary
		centroids = {}

		# Take all the points as the centroids
		for i in range(len(data)):
			centroids[i] = data[i]

		# we are not gonna have max iterations,and tolerance  we are gonna run in infinite loop 
		while True:

			# put the new centroids here.
			new_centroids = []

			# looping through the centroids
			for i in centroids:

				# all the features that are in the range of the centroid
				in_bandwidth = []

				centroid = centroids[i]
        
				# looping through the featuresets and calculating the distance with the selected centroid
				for featureset in data:
					if np.linalg.norm(featureset-centroid) < self.radius:
						# saving the featureset if it is within the range of the centroid featureset
						in_bandwidth.append(featureset)

				print in_bandwidth,i,"IN_BANDWIDTH"		
				# taking the average of all the featuresets to get the new centroid 
				new_centroid = np.average(in_bandwidth,axis=0)

				print new_centroid,i,"NEW_CENTROID"

				new_centroids.append(tuple(new_centroid))
			
				print new_centroids,i,"NEW_CENTROIDS"
			
			uniques = sorted(list(set(new_centroids)))
			
			print uniques,i,"UNIQUES"

			prev_centroids = dict(centroids)

			centroids = {}

			print prev_centroids,"PREV"
			
			for i in range(len(uniques)):
				centroids[i] = np.array(uniques[i])

			print centroids,"PRESENT"	

			optimized = True
			for i in centroids:
				if not np.array_equal(centroids[i], prev_centroids[i]):
					optimized = False
				if not optimized:
					break
			if optimized:
				break

			self.centroids = centroids



clf = Mean_Shift()
clf.fit(x)

centroids = clf.centroids

plt.scatter(x[:,0], x[:,1], s=150)

for c in centroids:
    plt.scatter(centroids[c][0], centroids[c][1], color='k', marker='*', s=150)

plt.show()
