#Shan Sikdar
#HW 2
# problem 2
#python 3.3
 
 
# Global parameters
numChannels = 1                      # mono
sampleWidth = 2                      # in bytes, a 16-bit short
sampleRate = 44100
 
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
	#print (len(data))
	N = int(raw_input("Enter your window size N:"))
	K = N


	f = open(infileName[0:len(infileName)-4] + '.env.txt', 'w')
	#  Example: find the maximum value in the samples

	#go through all the frames in the window
	#math.ceil(len(data)/K) is the number of times we will need to shift
	count=0
	for i in range(0,int(math.ceil(len(data)/K))):
		#record the time
		max1 = 0
		if(count + N > len(data)):
			for j in range(count,len(data)):
				if abs(data[j]) > max1:
					max1 = abs(data[j])
		else:  
			for j in range(count,N+count):
				if abs(data[j]) > max1:
					max1 = abs(data[j])

		#record the amplitude
		string = str(float(count)/sampleRate) + ' ' + str(max1) + '\n' 
		f.write(string)
		#Move window by shift
		count= count + K

main()

           
                