#
# Quick Cheat Sheet
# test[1,:]
#

import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn import svm

my_data = np.genfromtxt('C:\Users\Shan\Documents\GitHub\grad_school\cs_591\project\svm_dataset.csv', delimiter=',')

rows, cols = my_data.shape

a_train, a_test = train_test_split(my_data)

#labels are currently the last column
training_labels = a_train[:,29]
testing_labels = a_test[:,29]

#delete the labels from the training and testing set?
a_train = np.delete(a_train,29,axis=1)
a_test = np.delete(a_test,29,axis=1)

# SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=3,
# gamma=0.0, kernel='rbf', max_iter=-1, probability=False, random_state=None,
# shrinking=True, tol=0.001, verbose=False)

print 'training...'
clf = svm.SVC(kernel='poly')
clf.fit(a_train, training_labels) 

# # order is chosen to match the memory layout of the array instead of using a standard C or Fortran ordering
# # for x in np.nditer(a, order='F'): or 'C' for 
# testing_labels = testing_labels.tolist()
print 'testing...'
ctr = 0
for i in range(0, a_test.shape[0]):
	data =  a_test[i,:]
	clf.predict(data)
	if(clf.predict(a_test[i,:]).tolist()[0] == testing_labels[i]):
		ctr += 1
	# print ctr/a_test.shape[0]

accuracy = float(ctr)/a_test.shape[0]
print accuracy


# # After being fitted, the model can then be used to predict new values:

# >>> clf.predict([[2., 2.]])
# array([1])

