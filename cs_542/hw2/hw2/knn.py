# Shan Sikdar
# HW2 K Nearest Neighbor
#k - nearest neighbor algorithm

#http://www.math.le.ac.uk/people/ag153/homepage/KNN/OliverKNN_Talk.pdf
# The algorithm (as described in [1] and [2]) can be summarised as:
# 1. A positive integer k is specifed, along with a new sample
# 2. We select the k entries in our database which are closest to the new sample -- In my case 
# 3. We Find the most common classification of these entries
# 4. This is the classification we give to the new sample

import sys
import math
import numpy
import csv
# from collections import Counter
from collections import defaultdict
from operator import itemgetter

#
# L2 Distance
# inputs:
#	vector a
#	vector b
#	schema for the data set
#
# Note: Since the data has been standardized from part (i)
# and the datapoints have a mixture of categorical and continuous variables
# 
# define:
# Dl2 Category
# Component wise value of 1 for categorical attributes that disagree 0 if they do agree
#
# Dl2 Continouous
#  (Sum{(a[i] - b[i])^2})^.5
#
# NOTE: MAKE SURE NOT CALCULATE THE CLASS LABEL INTO THE DISTANCE!
#
def l2_distance(a,b,schema):
	sum = 0
	for i in range(0, len(a) - 1):
		#check if a category:
		if schema[i] == True:
			#Category
			if(a[i] != b[i]):
				sum = sum + 1
			else:
				sum = sum + 0		
		else:
			#its continuous
			sum = sum + (float(a[i]) - float(b[i]))**2
	return math.sqrt(sum)

def max_occurrences(seq):
    "dict iteritems"
    c = dict()
    for item in seq:
        c[item] = c.get(item, 0) + 1
    return max(c.iteritems(), key=itemgetter(1))

	

def main():
	print ('K Nearest Neighbor Classifier:')

	K = int(sys.argv[1])
	print( 'K: ' + str(K))
	trainingSetName = sys.argv[2]
	testingSetName = sys.argv[3]
	
	database = []			#training set
	testingSet = []			#testing set
	answerSet = []			#my determined answers
	
	#Create the Database and Testing Set
	with open(trainingSetName, 'rb') as trainingSet:
		trainingReader = csv.reader(trainingSet, delimiter=',', quotechar='|')
		for row in trainingReader:
			database.append(row)

	print("# of Training Set Points: " + str(len(database)))

	with open(testingSetName, 'rb') as testSet:
		testingReader = csv.reader(testSet, delimiter=',', quotechar='|')
		for row in testingReader:
			testingSet.append(row)
					
	print( "# of Testing Set Points: " + str(len(testingSet)))
			
	#Use this to keep track of which fields are Categorical and which ar continuous
	# True = Categories False = Continuous
	schema = [] 
	if 'lenses' in trainingSetName.lower():
		#Schema taken from lenses.names
		print('Lenses Dataset:')
		schema = [True,True,True,True,True]
	else:
		#schema taken from crx.names
		print( 'CRX Dataset:')
		schema = [True, False, False, True, True, True, True, False, True, True, False, True, True, False, False, True ]
		
	#Loop through all the new samples, aka the testing set.
	for newDataPoint in testingSet:
	
		distances = []	#List holding the k nearest neighbor distances
		labels = []		#List holding the label of coresponding to the distance
		
		#Loop through our database of points
		for databasePoint in database:
			#For each sample calculate all the possible distances, the find the k smallest distances
			distance = l2_distance(newDataPoint,databasePoint,schema)
			if(len(distances) != K):
				distances.append(distance)
				labels.append(databasePoint[len(databasePoint)-1])
			else:
				# we already have k distances calculated, if out new distance is smaller than the maximum of the K smallest distances
				maximum = max(distances)
				index = distances.index(maximum)
				if distance < maximum:
					distances[index] = distance
					labels[index] = databasePoint[len(databasePoint)-1]

		#out of those distances find the most common classification of those entries
		
		
		# most_common,num_most_common = Counter(labels).most_common(1)[0] # 4, 6 times
		most_common,num_most_common = max_occurrences(labels) # 4, 6 times

		determinedLabel = most_common
		
		#give this classification to the sample
		newDataPoint.append(determinedLabel)
		answerSet.append(newDataPoint)

	#The output of your program should be a testing file with an additonal coma seperated field 
	# so append my guess to the end of the data set.
	with open(testingSetName + '.knnOuput', 'w') as csvfile:
		outwriter = csv.writer(csvfile, delimiter=',',
										quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for row in answerSet :
			outwriter.writerow(row)
			
	#calculate accuracy 
	ctr = 0
	for answer in answerSet:
		if(answer[-1] == answer[-2]):
			ctr = ctr + 1
	print('number correct: ' + str(ctr) + "/" + str(len(answerSet)))
	print('accuracy: ' + str(float(ctr)/ len(answerSet)))
	print( 'done.')
main()