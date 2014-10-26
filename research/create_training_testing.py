# Create training and testing sets with good data and bad data
import numpy as np
from sklearn.cross_validation import train_test_split

SAE = False; #flag to distinguish between Sparse autoencoder and SVM

good_data = np.genfromtxt('C:\Users\Shan\Documents\GitHub\\grad_school\\research\\datasets\\good_traffic.csv', delimiter=',')
bad_data = np.genfromtxt('C:\Users\Shan\Documents\GitHub\\grad_school\\research\\datasets\\bad_traffic.csv', delimiter=',')

good_rows, good_cols = good_data.shape
bad_rows, bad_cols = bad_data.shape

if(good_cols != bad_cols):
	raise Exception("Dimensions don't agree with the dataset" + str(good_data.shape) + "   " + str(bad_data.shape)) 

good_train, good_test = train_test_split(good_data,train_size =.026)
bad_train, bad_test = train_test_split(bad_data,test_size =.25)

print "GOOD TRAFFIC: "
print "Train: " + str(good_train.shape)
print "Test: " + str(good_test.shape) + "\n"

print "BAD TRAFFIC: "
print "Train: " + str(bad_train.shape)
print "Test: " + str(bad_test.shape) + "\n"


full_train = np.concatenate((good_train, bad_train),axis=0)
full_test = np.concatenate((good_test, bad_test),axis=0)

print "FINAL dimensions:"
print "Train: " + str(full_train.shape)
print "Test: " + str(full_test.shape) + "\n"

#shuffle the rows of the matrix around, so that not all of the classes are in chunks
#no need to do this for test.
np.random.shuffle(full_train)

if(SAE):
	#labels are currently the last column
	#right now remove this until I figure out how to use the sparse autoencoder to classify.
	# training_labels = full_train[:,cols-1]
	cols = good_cols		#can do this b/c of check above.
	full_train = np.delete(full_train,cols-1,axis=1)
	full_test = np.delete(full_test,cols-1,axis=1)
	np.savetxt("C:\Users\Shan\Documents\GitHub\\grad_school\\research\\datasets\\sparseAuto_train.csv", full_train, delimiter=",")
	np.savetxt("C:\Users\Shan\Documents\GitHub\\grad_school\\research\\datasets\\sparseAuto_test.csv", full_test, delimiter=",")
	
else:
	#SVM
	#Want the label columns so don't delete anything
	np.savetxt("C:\Users\Shan\Documents\GitHub\\grad_school\\research\\datasets\\svm_train.csv", full_train, delimiter=",")
	np.savetxt("C:\Users\Shan\Documents\GitHub\\grad_school\\research\\datasets\\svm_test.csv", full_test, delimiter=",")
	