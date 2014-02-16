# File: readWave.py
# Author: Wayne Snyder
# Date: 1/5/14
# Description: This is a prototypical Python 3 program for reading and processing
#   a wave file. It reads in the entire input file into an array of shorts, which can then be
#   analyzed or processed as needed.
#   If you want to use this with Python 2.7, just change the input to raw_input in main().
# Citation: This is a modified version of a program from A Concise Introduction
#    to Programming in Python.
 
 
import array
import contextlib
import wave
import math
 
# Read a wave file and return the entire file as an array, and the parameters
# Parameters are:  (numChannels, sampleWidth, sampleRate, numFrames, not-used, not-used)
 
def readwav(fname):
	with contextlib.closing(wave.open(fname)) as f:
		params = f.getparams()
		frames = f.readframes(params[3])
	return array.array("h", frames), params
 
def main():
 
	infileName = raw_input("Enter the name of the input .wav file: ")
 
# Next, get all the samples as an array of short, and the parameters as a
# tuple (numChannels, sampleWidth, sampleRate, numFrames, not-used, not-used)
 
	data, params = readwav(infileName)
	print (len(data))
	N = 882
	K = 441
 
	count=0
	windowCount=0
 
#  Example: find the maximum value in the samples
 
	#go through all the frames in the window
	#math.ceil(len(data)/K) is the number of times we will need to shift
	for i in range(0,math.ceil(len(data)/K)):
		max1 = 0
		mean=0
		if(count + N > len(data)):
		#edge case said we could ignore in class
			for j in range(count,len(data)):
				if abs(data[j]) > max1:
					max1 = abs(data[j])
					maxabsans.append(max1)
				mean=(mean + data[j])
			meanans.append(mean/(len(data) - count))
			print (mean/(len(data) - count))
			stddev = (sum((mean/N - value) ** 2 for value in data[count:len(data)]) / N) ** .5
			print("Window:" + str(windowCount) + " , max: " + str(max1) + ",mean: " + str(mean/N) + "sd:" + str(stddev))
		else:
			for j in range(count,N+count):
				if abs(data[j]) > max1:
					max1 = abs(data[j])
					maxabsans.append(max1)
				mean=(mean + data[j])
			stddev = (sum((mean/N - value) ** 2 for value in data[count:N+count]) / N) ** .5
		print("Window:" + str(windowCount) + " , max: " + str(max1) + ",mean: " + str(mean/N) + "sd:" + str(stddev))
		#Move window by shift
		count= count + K
		windowCount+=1 
 
main()

