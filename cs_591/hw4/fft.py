#
#HW 3 fourier transform
#

import array
import contextlib
import wave
import math
from math import sin, pi, cos
import cmath
from numpy import diff, sign

# Global parameters
numChannels = 1                      # mono
sampleWidth = 2                      # in bytes, a 16-bit short
sampleRate = 44100

I = complex(0,1)
E = complex(2.718281,0)
 
f = open('output.csv', 'w')
 
 
# Read a wave file and return the entire file as an array, and the parameters
# Parameters are:  (numChannels, sampleWidth, sampleRate, numFrames, not-used, not-used)
def readwav(fname):
    with contextlib.closing(wave.open(fname)) as f:
        params = f.getparams()
        frames = f.readframes(params[3])
    return array.array("h", frames), params
 
def writewav(fname, data, params):
    with contextlib.closing(wave.open(fname, "w")) as f:
        f.setparams(params)
        f.writeframes(data.tostring())
    # print(fname + " written.")

#
# DFT Code from last time
#	
def DFT(x):
	N = len(x) 					#get the length of x
	X = [0]*N 						#a place to store reusults
	mI2pidN = -I*2.0*pi/N		#combine
	
	for k in range(0,N):		#for every frequency
		for n in range(0,N):	#prepare to accumulate
			xn = complex(x[n],0.0)	#for every phase
			X[k] = X[k] + xn* cmath.exp(mI2pidN * n *k) #cast Real input to complex
		X[k] = X[k] /N			#normalize
	return X

#
# function implementing Hann window.
#
def w(n,N):
	if(0 <= n <= N):
		return (1-.5) * cos(2*pi*(float(n)/N) + pi) + .5
	else:
		return 0
	
#
# DFT With Hann Window
#	
def DFThann(x):
	N = len(x) 					#get the length of x
	X = [0]*N 						#a place to store reusults
	mI2pidN = -I*2.0*pi/N		#combine
	
	for k in range(0,N):		#for every frequency
		for n in range(0,N):	#prepare to accumulate
			xn = complex(x[n],0.0)	#for every phase
			X[k] = X[k] + xn* w(k,N)*cmath.exp(mI2pidN * n *k) #cast Real input to complex
		X[k] = X[k] /N			#normalize
	return X
	
	
def FFT(x):
    N = len(x)
    if N <= 1: return x
    even = FFT(x[0::2])
    odd =  FFT(x[1::2])
    return [(even[k] + cmath.exp(-2j*pi*k/N)*odd[k])/2 for k in xrange(N/2)] + \
           [(even[k] - cmath.exp(-2j*pi*k/N)*odd[k])/2 for k in xrange(N/2)]
	
# Add to your FFT.py file a method that takes an arbitrary array, 
#and expands it to the next higher power of 2 by adding 0's to the
# end of the array.
def padding(x):
	length = len(x)	#length	
	binary = bin(length)[2:]	# binary representation as string '0b1001'
	nextMultof2 = 2**(len(binary))
	padNumber = nextMultof2 - length
	
	for i in range(0, padNumber):
		x.append(0)
		
	return x
	
	
def createWave(n,a,f,p):
	realList = []
	for i in range(0,n):
		k = a*math.cos((2*pi*f*i/n)+p)
		realList.append(k)
	return realList

def addWaves(a, b):
	c = []
	for i in range (0,len(b)):
		c.append(a[i] + b[i])
	return c

def printRawSpectrum(X,type):
	if(type == 'DFT'):
		print 'DFT'
		output = DFT(X)
	elif(type == 'HANN'):
		print 'Hann Solo shot first'
		output = DFThann(X)
	else:
		print 'FFT'
		output = FFT(X)
	count = 0
	for i in output:
		# print(str(count) + ": ( " + str(round(cmath.polar(i)[0],2)) + ", "  + str(round(cmath.polar(i)[1],2)) + " )")
		f.write((str(count) + ",  " + str(round(cmath.polar(i)[0],2)) + ", "  + str(round(cmath.polar(i)[1],2)) + " ") + '\n')
		count += 1
		
def printFullSpectrum(X,type):
	if(type == 'DFT'):
		print 'DFT'
		K = DFT(X)
	else:
		print 'FFT'
		K = FFT(X)
		
	# K = FFT(X)
	for i in range(int(len(K)/2)+1, len(K)):
		f.write((str(i-len(K)) + " , " + str(round(cmath.polar(K[i])[0],2)) + ", "  + str(round(cmath.polar(K[i])[1],2)) + " ") + '\n')
		# f.write((str(i-len(K)) + " , " + str(round(cmath.polar(K[i])[0],2)) + ", "  + str(round(cmath.polar(K[i])[1],2)) + " ") + '\n' )
		
	f.write((str(0) + ": , " + str(round(cmath.polar(K[int(len(K)/2)])[0],2)) + ", "  + str(round(cmath.polar(K[int(len(K)/2)])[1],2)) + " )") + '\n')
	
	for i in range(0,int(len(K)/2)-1):
		f.write((str(i+1) + " , " + str(round(cmath.polar(K[i])[0],2)) + ", "  + str(round(cmath.polar(K[i])[1],2)) + " ") + '\n' )

def printSpectrum(X,type):
	if(type == 'DFT'):
		print 'DFT'
		output = DFT(X)
	else:
		print 'FFT'
		output = FFT(X)
		
	count = 0
	for i in output:
		# print(str(count) + ": ( " + str(2*round(cmath.polar(i)[0],2)) + ", "  + str(round(cmath.polar(i)[1],2)) + " )")
		f.write((str(count) + " , " + str(2*round(cmath.polar(i)[0],2)) + ", "  + str(round(cmath.polar(i)[1],2)) + " \n"))
		count += 1
		if(count > len(output)/2 - 1):
			break


def main():
	
	print('I have commented out all the test cases to make the output more readable while doing the writeup...buts its all still in the code.')
	
	#Problem 1
	# a = createWave(8,1.0,1.0,0)
	# printFullSpectrum(a,'DFT')
	# printFullSpectrum(a,'FFT')
	# x = [1,2,3,4,5,6,7,8]
	# print FFT(x)
	# print DFT(x)
	
	# printSpectrum(x,'DFT')
	# printSpectrum(x,'FFT')
	
	# #Problem 2
	# # a = createWave(9, 1.0, 1.0, -1.57) 
	# # a = createWave(12, 1.0, 1.0, -1.57) 
	# a = createWave(15, 1.0, 1.0, -1.57) 
	# a = padding(a)
	# a = createWave(16, 1.0, 1.0, -1.57) 
	# printSpectrum(a,'DFT')
	# # printFullSpectrum(a,'FFT')

	
	# # Problem 3
	# # a = createWave(11, 1.0, 1.0, -1.57) 
	# # a = padding(a)	
	# # # printRawSpectrum(a,'DFT')
	# # printRawSpectrum(a,'HANN')
	
	# Problem 4
	data, params = readwav('Bell2.wav')
	samples = []
	N = 800
	#params[2] is the sample rate
	startPoint = int(.5*params[2])
	
	for i in range(startPoint, startPoint + N):
			samples.append(data[i])
	
	
	printRawSpectrum(samples,'HANN')
	
	#
	# Used Matlab to get the maximums
	#  harmonic , amplitude, actual frequency
	# 52,  184.41, 2866.5
	# 314,  195.3, 17309.25
	# 348,  890.45, 19183.5

	# conversion factor to get actual frequency k*44100/N 
	# 184.41 + 195.3  + 890.45 = 1270.16
	
	#
	# Used Additive Synthesis and envelope generator from last hw to create my artificail bell. 
	#
	# Used this as my timber file
	#
		
main()
                


