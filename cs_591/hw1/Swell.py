#Problem 3: Write a program Swell.py which prompts the user for the name of a mono input file, and produces a mono output file which takes the musical signal from the input file and changes the amplitude in the following way: the signal will start at amplitude 0, increase linearly until exactly half way through the file, at which point it should be at the same amplitude as the original signal, and then decrease linearly until it becomes 0 at the end of the file. It should work no matter how long the input file is. (Hint: You can find the number of frames in the input file, and hence the length; you just need to scale the amplitude using a factor which changes at each iteration through the loop.)

import array
from struct import pack           # This creates the binary data structure for frames
from math import sin, pi
import wave                       # The main library for manipulating wave files

#prompt user for input file
inputFile =  raw_input("Enter name of input file: ")

# open wave file for reading
inWaveFile = wave.open(inputFile, 'r')

# get the parameters
(numChannels, sampleWidth, sampleRate, numFrames, compressionType, nameOfCompression) = inWaveFile.getparams()

#output file
outputFile = "Swell_mono_ouput_file.wav"
outWaveFile = wave.open(outputFile, 'w')
outWaveFile.setparams((numChannels, sampleWidth, sampleRate, 0, 'NONE', 'not compressed'))

waveData=""       # this holds the data to be written to file in binary form


print("Number of Channels: " + str(numChannels))
print("# of frames:" + str(numFrames))


# how many frames to read each loop iteration?
numFramesToRead = 1


midpoint = numFrames/2

for i in range( 0, numFrames ):
	#in mono, frame will have one sample, in stereo, two
	frame = inWaveFile.readframes( numFramesToRead )    
     
	# unpack binary string into array of ints
	data = array.array('h',frame)

	if(i <= numFrames/2):
		amplitude = float(i)/midpoint

	if(i > numFrames/2):
		amplitude = float(numFrames-1-i)/numFrames

	newAmplitude =  data[0]*amplitude

	#write the frame to wavedata
	waveData += pack( 'h', newAmplitude)

	#write everything else back
	for i in range(1, len(data)):
		waveData += pack( 'h', data[i])

#write wavefile to the outfile
outWaveFile.writeframes(waveData)
outWaveFile.close()
inWaveFile.close()

