import numpy as np 
import matplotlib.pyplot as plt 

from sklearn.linear_model import LinearRegression

# 

x = np.array([1,1.8,2,2.2,2.5,3,3.6,4.9,5.5,6.7]).reshape(-1,1)
y = np.array([2,2.3,2.5,4,4.6,4.9,4.4,5.4,4.6,7])


#  --------  SKLEARN WAY OF DOING LINEAR REGRESSION -------

model = LinearRegression()


# Training the data operation
model.fit(x,y)

regression_line = []

for xs in x:
	regression_line.append(model.predict(np.array(xs).reshape(1,-1)))


test_value = np.array([3]).reshape(1,-1)

predicted_y_value = model.predict(test_value)

print predicted_y_value


plt.scatter(x,y)
plt.scatter(test_value,predicted_y_value,color="r")
plt.plot(x,regression_line,"c")
plt.show()


