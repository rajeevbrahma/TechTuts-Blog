import matplotlib.pyplot as plt 
from matplotlib import style
style.use('ggplot')
import numpy as np

x = np.array([[1,2],[1.3,2.1],[1.5,2.5],[1.9,3],[2,5],
	[2.7,4],[6,7.8],[6.9,8.6],[7.2,9],[8,9.6]])

markers = ["o","*",".","..","^","s"]

colors = ["g","r","c","b","k","y"]


# tol - how much the centeroid is gonna move
# max_iter -

class K_Means:
	def __init__(self,k=2,tol=0.01,max_iter=300):
		self.k = k
		self.tol = tol
		self.max_iter = max_iter

	def fit(self,data):

		# step 1:
		# Taking one of the Featureset as the centroid
		# Note : Depends on the number of the clusters(i.e., k) you have taken 
		# you will take that many centroids


		self.centeroids = {}
		
		# step 2:
		# Assigning the First "k" features as the centroids

		for i in range(self.k):
			self.centeroids[i] = data[i]

		print self.centeroids	

		
		# step 3: Running the loop 300 times till we get the optimized centroids for our clusters

		for i in range(self.max_iter):
			
			# Initialising the classifications dictionary
			# where we will store the featureset those are closer to the 
			# centroids we have chosen in the above step 
			self.classifications = {}

			

			for i in range(self.k):
				
				# Initialising the classifications dictionary with the empty list 
				self.classifications[i] = []

			# Iterating over the data to get the distances from the centroids			 
			for featureset in data:
				# calculating the distance b/w centroids and the featureset
				# this will result the distances like below
				# ['0.0', '0.316227766016838']
				# ['0.316227766016838', '0.0']
				# since we have two clusters.

				distances = [np.linalg.norm(featureset-self.centeroids[centeroid]) for centeroid in self.centeroids]		

				# getting the index of the minimum distance we got in the distance calculation

				classification = distances.index(min(distances))
				
				# using the index we got above we can decide under which cluster we can
				# place our featureset

				self.classifications[classification].append(featureset)
				
				# Note : since clusters will always be like 0,1,2 ... etc taking index is just enough


			
			prev_centroids = dict(self.centeroids)
			
			# run through each cluster(i.e., 0,1) in the classifications dictionary. 
			for classification in self.classifications:

				# [array([1., 2.])] -  cluster 0 classified featureset
				# [1. 2.] -  average of the featureset when done column wise

				# [array([1.3, 2.1]), array([1.5, 2.5]), array([1.9, 3. ]), array([2., 5.]), 
				# array([2.7, 4. ]), array([6. , 7.8]), array([6.9, 8.6]), 
				# array([7.2, 9. ]), array([8. , 9.6])] - cluster 1 classified featureset

				# [4.16666667 5.73333333] - average of the featureset when done column wise

				# Taking those average values as the new centroids.
				self.centeroids[classification] = np.average(self.classifications[classification],axis=0)	

				# Note : we are doing like this because we have to optimize the centroids


			optimized =True
			
			for c in self.centeroids:
				original_centroid = prev_centroids[c]
				current_centroid = self.centeroids[c]
				if np.sum((current_centroid-original_centroid)/original_centroid*100.0) > self.tol:
					optimized = False

			if optimized:
				break			


		pass

	def predict(self,data):
		distances = [np.linalg.norm(data-self.centeroids[centeroid]) for centeroid in self.centeroids]		
		classification = distances.index(min(distances))
		return classification

clf = K_Means()
clf.fit(x)

for centeroid in clf.centeroids:
	plt.scatter(clf.centeroids[centeroid][0],clf.centeroids[centeroid][1],
		marker="o",color="k",s=150,linewidth=5)

for classification in clf.classifications:
	
	color = colors[classification]

	for featureset in clf.classifications[classification]:
		plt.scatter(featureset[0],featureset[1],marker="x",color=color,s=150,linewidth=5)


newvalues = np.array([[2.2,1],[3.4,3],[8.9,7.8],[2.221,4.33],[5.66,5.44]])

for newval in newvalues:
	classification = clf.predict(newval)
	color = colors[classification]
	plt.scatter(newval[0],newval[1],marker="*",color=color,s=150,linewidths=5)



plt.show()









