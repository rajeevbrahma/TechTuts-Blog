import pandas as pd
import numpy
import matplotlib

path = r"iris123.csv"

names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'Class']

dataset = pd.read_csv(path, names=names)

print(dataset)

X = dataset.iloc[:,:-1].values  
y = dataset.iloc[:,4].values

print(X)
print(y)
    
from sklearn.model_selection import train_test_split  
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)


from sklearn.neighbors import KNeighborsClassifier  
classifier = KNeighborsClassifier(n_neighbors=5)  
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

#print(y_pred)

from sklearn.metrics import classification_report, confusion_matrix  
print(confusion_matrix(y_test, y_pred))  
#print(classification_report(y_test, y_pred))  



from sklearn import metrics

print("Accuracy:",metrics.accuracy_score(y_test, y_pred))






                                                    










                                                    



