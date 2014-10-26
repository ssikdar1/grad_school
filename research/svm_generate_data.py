import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn import svm
from sklearn.preprocessing import scale
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

outfile = open("SVM_answers.txt","w")

#
# Training phase
#
print 'training...'

train_data = np.genfromtxt("C:\Users\Shan\Documents\GitHub\\grad_school\\research\\datasets\\svm_train.csv", delimiter=',')
train_rows, train_cols = train_data.shape
train_labels = train_data[:,train_cols-1]						#labels are currently the last column
train_data = np.delete(train_data,train_cols-1,axis=1)		#delete the labels from the training set?
train_data = scale(train_data)

#define the svm and fit it
clf = svm.SVC(kernel='linear')
# clf = svm.SVC()
clf.fit(train_data, train_labels) 

#
# Testing phase
#
print 'testing...'

#TODO possibly scale all data before the split
test_data = np.genfromtxt("C:\Users\Shan\Documents\GitHub\\grad_school\\research\\datasets\\svm_test.csv", delimiter=',')
test_rows, test_cols = test_data.shape
test_labels = test_data[:,test_cols-1]						#labels are currently the last column
test_data = np.delete(test_data,test_cols-1,axis=1)		#delete the labels from the training set?
test_data = scale(test_data)

# # order is chosen to match the memory layout of the array instead of using a standard C or Fortran ordering
# # for x in np.nditer(a, order='F'): or 'C' for 
# testing_labels = testing_labels.tolist()
ctr = 0
print "predict" + "real answer"
outfile.write("G" + "  " + "A" + "\n")

# to hold ground truth values for confusion matrix
predictions = clf.predict(test_data)

# Compute confusion matrix
cm = confusion_matrix(test_labels, predictions)

print(cm)

# Show confusion matrix in a separate window
plt.matshow(cm)
plt.title('Confusion matrix')
plt.colorbar()
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.show()

# for i in range(0, test_rows):
	# data =  test_data[i,:]
	
	# guess = clf.predict(data)
	# predictions.append(guess[0])
	# answer = str(test_labels[i])
	
	
	# outfile.write(str(guess) + "  " + answer + "\n")
	# #
	# # TODO: recall, precision
	# #
	# if(clf.predict(test_data[i,:]).tolist()[0] == test_labels[i]):
		# ctr += 1
# accuracy = float(ctr)/test_data.shape[0]
# print accuracy






# numpy.savetxt("C:\Users\Shan\Documents\GitHub\grad_school\\research\\train.csv", a_train, delimiter=",")
# numpy.savetxt("C:\Users\Shan\Documents\GitHub\grad_school\\research\\test.csv", a_test, delimiter=",")

