import numpy 
from sklearn.cross_validation import train_test_split

# my_data = numpy.genfromtxt('C:\Users\Shan\Documents\GitHub\grad_school\\cs_591\project\dimension_10.csv', delimiter=',')
my_data = numpy.genfromtxt('C:\Users\Shan\Documents\GitHub\grad_school\\cs_591\project\\svm_datasetStandardized.csv', delimiter=',')

rows, cols = my_data.shape

a_train, a_test = train_test_split(my_data,test_size =.20)

numpy.savetxt("C:\Users\Shan\Documents\MATLAB\CS542_591_project\\train.csv", a_train, delimiter=",")
numpy.savetxt("C:\Users\Shan\Documents\MATLAB\CS542_591_project\\test.csv", a_test, delimiter=",")

