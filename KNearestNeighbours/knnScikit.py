import numpy as np
from matplotlib.pyplot import pyplot

from math import sqrt

dataset = {'b':[[1,2],[2,3]],'c':[[5,7],[8,9]]}

test_features = [2.3,4]

for group in dataset:
	for features in dataset[group]:
		plt.scatter(features[0],features[1],s=100,color=group)

# onliner
# [[(plt.scatter(features[0],features[1]))]for features in dataset[group] for group in dataset]

# plt.show()	
# ----------------- KNN -------------------------
clf = KNearestNeighbors()

clf.fit(dataset)
print clf.predict(test_features)


def k_nn(data,predict,k=2):

	for group in dataset:
		for features in dataset[group]:
			euclidean_distance = np.linalg.norm(np.array(features)-np.array(predict))
			distances.append([euclidean_distance,group])


	votes = [val[1] for val in sorted(distances)[:k]] # since 1 is the group
	print Counter(votes).most_common(1)


k_nn(dataset,test_features,k=2)	

