# process.py

import sys
import csv


#For real valued features just replace missing values with the label-conditioned mean
# (i.e mu(x|+) for instances labeled as positive.

def getLabeledConditonMeans(column,labelColumn, index):
	value = column[index]
	label = labelColumn[index]
	sum = 0
	count = 1 
	for i in range(0,len(column)):
		if(label == labelColumn[i] ):
		#No question marks in the label column so don't have to check.
			if('?' not in column[i]):
				sum = sum + float(column[i])
				count = count + 1
	mean = (float(sum)/ count)
	# print(mean)
	return mean

def getStdOfColumn(column,mean):
	#get a squared column, find its expected value
	std = 0.0
	for k in range(0,len(column)):
		#get squared difference from the mean
		std	= (std + (float(column[k]) - mean)**2)
	#divide by N
	std = std/len(column)
	#square root
	std = (std**.5)
	return std
		

def getMeanOfColumn(column):
	# print(column)
	sum = 0
	for i in range(0,len(column)):
		sum = sum + float(column[i])
	mean = float(sum)/len(column)
	return mean
	
def zScale(dataset,schema):
	#Loop through all columns
	for i in range(0,len(dataset)):
		column = dataset[i]

		#For each column that is continuous get the mean, std 
		if(schema[i] == False):
			#get mean
			mean = getMeanOfColumn(column)
			std = getStdOfColumn(column, mean)
			
			for j in range(0, len(column)):
				# if(i == 1):
					# print('x,mean, std:  ' + str(column[j]) + ' , ' + str(mean) + ' , ' +str(std))
			#	for each value in the column, scale it.
				x = float(column[j])
				column[j] = float(x - mean)/std

	print("zscale complete.")

def output(name,dataset):
	outfile = open(name,'w')
		#for each row	
	for j in range(0, len(dataset[0])):
		string = ""
		string = str(dataset[0][j])
		#go through every column get value and write
		for i in range(1, len(dataset)):
			string = string + "," + str(dataset[i][j])
			
		outfile.write(string + '\n')
	print("file written")

def replaceQuestionMarks(dataset,replaceValue,schema):
	for i in range(0,len(dataset)):
	#loop through all columns
		
		column = dataset[i]
		
		for j in range(0,len(column)):
		#go through the values in columns 
			value = column[j]
			if('?' in value):
				if(schema[i] == True):
				#then it is a category 	
					for value in column:
						value = replaceValue[i]
				else:
				#For real valued features, just replace missing values with the label conditioned mean (i.e. for instances labeled as positive)
					for value in column:
						if('?' in value):
						#pass in label and column column
							labelColumn = dataset[len(dataset) -1]
							value = getLabeledConditonMeans(column,labelColumn,j)
	
			column[j] = value
			
	print("Question Marks Replaced")
	
def main():
	
	print('Process Data:')
	print ('Argument List:', str(sys.argv))

	#True means Category, False means continuous
	schema = [True, False, False, True, True, True, True, False, True, True, False, True, True, False, False, True]
	
	# where i got these values are explained in the documentation.
	replaceValues =['b',0,0,'u','g','c','v',0,'t','f',0,'f','g',0,0,'+'];
	
	trainingSetName = sys.argv[1]
	testingSetName = sys.argv[2]
		
	#Use this to get the column value mean and modes
	trainingSetcolumns= [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
	
	#Create the Database and Testing Set
	with open(trainingSetName, 'rb') as trainingSetFile:
		trainingReader = csv.reader(trainingSetFile, delimiter=',', quotechar='|')
		for row in trainingReader:
		
			for i in range(0,len(row)):
			#get the coressponding list and append the value
				trainingSetcolumns[i].append(row[i])

	print("trainingSet")		
	print(len(trainingSetcolumns))
	print(len(trainingSetcolumns[0]))
	
	
	#replace Question marks
	replaceQuestionMarks(trainingSetcolumns,replaceValues,schema)
	
	#zscale
	zScale(trainingSetcolumns,schema)
	
	#output files as processed
	output("crx.training.processed",trainingSetcolumns)
	
	
	testingSetcolumns= [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
	
	#Create the Database and Testing Set
	with open(testingSetName, 'rb') as testingSetFile:
		testingReader = csv.reader(testingSetFile, delimiter=',', quotechar='|')
		for row in testingReader:
			for i in range(0,len(row)):
				#get the coressponding list and append the value
				testingSetcolumns[i].append(row[i])
	print("Testing Set")
	print(len(testingSetcolumns))
	print(len(testingSetcolumns[0]))
	
	#replaceQuestionMarks
	replaceQuestionMarks(testingSetcolumns,replaceValues,schema)
	
	#zScale
	zScale(testingSetcolumns,schema)
	
	#output
	output("crx.testing.processed",trainingSetcolumns)
	

main()