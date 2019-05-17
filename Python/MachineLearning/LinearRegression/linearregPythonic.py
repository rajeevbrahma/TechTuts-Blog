import numpy as np
from matplotlib import pyplot as plt
from statistics import mean

x=np.array([1,2,3,4,5])
y=np.array([2,4,5,6,7])

# plt.scatter(x,y)
# plt.show()

def slope_intercept(xs,ys):
	# calculating slope
	m = ( (mean(xs)*mean(ys)) - (mean(xs*ys)) ) / ( (mean(xs)*mean(xs)) - (mean(xs*xs)) )

	# calculating intercept 
	c = mean(ys) - m*mean(xs)


	return m,c

m,c = slope_intercept(x,y)

regression_line = []

# for val in x:
for i in range(0,len(x)):
	print x[i]

	result = (m*x[i])+c
	regression_line.append(result)


	# print val



plt.scatter(x,y)
plt.plot(x,regression_line)
plt.show()

print m
print c

