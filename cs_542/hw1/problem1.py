import numpy
from numpy import genfromtxt
from numpy import matrix as m 

def phi(x):
	return [x[0],x[1],x[2],x[0]*x[1],x[0]*x[2],x[1]*x[2]]

def weights(M):
	return m.getT(M)
	# return m.getI( * M)*m.getT(M)*targetVector
	
	
detroit = genfromtxt("C:\Users\Shan\Downloads\Detroit.csv", delimiter=',')

targetVector =  detroit[:,9]

PHI + numpy.array()

PHI = numpy.array(PHI)
print PHI
print weights(PHI)
# for row in detroit:
	# print phi(row)
	
