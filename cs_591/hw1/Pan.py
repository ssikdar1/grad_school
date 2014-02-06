import array
from struct import pack  # This creates the binary data structure for frames
from math import sin, pi
import wave  # The main library for manipulating wave files

#prompt user for input file
inputFile =  raw_input("Enter name of input file: ")

# open wave file for reading
inWaveFile = wave.open(inputFile, 'r')

# get the parameters
(numChannels, sampleWidth, sampleRate, numFrames, compressionType, nameOfCompression) = inWaveFile.getparams()

#output streo , 2 channels
outputFile = "Pan_stero_ouput_file.wav"
outWaveFile = wave.open(outputFile, 'w')
outWaveFile.setparams((2, sampleWidth, sampleRate, 0, 'NONE', 'not compressed'))

waveData=""       # this holds the data to be written to file in binary form



# how many frames to read each loop iteration?
numFramesToRead = 1

for i in range( 0, numFrames ):


	# unpack binary string into array of ints
	frame = inWaveFile.readframes( numFramesToRead )       
	data = array.array('h',frame)

	#
	# Initally was goin to use two functions: x and -x + 2.5 to coordinate the panning values
	# to multiply the cofficent with but Dan mentioned to me to just use sin and cos functions which
	# would lead to a more smooth transition
	left  = abs(sin( 2 * pi * i * 1.0/(sampleRate * 10) )) *data[0]
	right = abs(sin( 2 * pi * i* 1.0/(sampleRate * 10) + pi/2 )) *data[0]

	# pack frame into short int (format 'h') in binary
	# stereo frame has two samples, first left then right
	#print(left)
	#print(right)
	waveData += pack('h', left)
	waveData += pack('h', right)

#write wavefile to the outfile
outWaveFile.writeframes(waveData)
outWaveFile.close()
inWaveFile.close()

