#
#HW 3 additiveSynthesis.py
#
from struct import pack
import array
import contextlib
import wave
import math
from math import sin, pi

# Global parameters
numChannels = 1                      # mono
sampleWidth = 2                      # in bytes, a 16-bit short
sampleRate = 44100

 
# Read a wave file and return the entire file as an array, and the parameters
# Parameters are:  (numChannels, sampleWidth, sampleRate, numFrames, not-used, not-used)
def readwav(fname):
    with contextlib.closing(wave.open(fname)) as f:
        params = f.getparams()
        frames = f.readframes(params[3])
    return array.array("h", frames), params

'''	
def writewav(fname, data, params):
    with contextlib.closing(wave.open(fname, "w")) as f:
        f.setparams(params)
        f.writeframes(data.tostring())
    # print(fname + " written.")
'''

def main():

	timberFileName = "bellTimber.txt"
	envelopeFileName = "Bell2.env.txt"
	outFileName = "artificial_bell.wav"
	
	
	timberFile = open(timberFileName, 'r')
	envelopeFile = open(envelopeFileName, 'r')
	outfile = wave.open(outFileName,'w')

	outfile.setparams((numChannels, sampleWidth, sampleRate,0, 'NONE', 'not compressed'))
	data = array.array("h")

	clarinetFrequency = []
	clarinetAmplitdues = []
	
	for line in timberFile:
		frequency, amplitude = line.split("\t")
		clarinetFrequency.append(float(frequency.strip()))
		clarinetAmplitdues.append(float(amplitude.strip()))

	envelopeTime = []
	envelopeAmplitudes = []
	for line in envelopeFile:
		# print(line)
		tokens = line.split(' ')
		envelopeTime.append(float(tokens[0]))
		envelopeAmplitudes.append(float(tokens[1]))
		
	
		
	count = 0
	for i in range(0,len(envelopeTime)):	
		
		if(i==0):
			deltaTime = envelopeTime[i+1]
		else:
			deltaTime = envelopeTime[i]-envelopeTime[i-1]
       	
		deltaFrames = deltaTime * sampleRate
		N = int(deltaFrames)
		# print("N = " + str(N))

		if i+1 ==len(envelopeAmplitudes):
			inc = 0
		else:
			inc = (envelopeAmplitudes[i+1] -  envelopeAmplitudes[i])/N
		
		currentAmp = envelopeAmplitudes[i]
		
		for k in range(N):
			sample = 0
			
			for j in range(0, len(clarinetFrequency)):
				sample += clarinetAmplitdues[j] * sin( 2 * pi * clarinetFrequency[j] * count / sampleRate )
			
			#scale by the envelpope amplitude
			sample = sample * currentAmp
			currentAmp = currentAmp + inc
			count = count + 1
			
			#data.append( int( sample ) )
			outfile.writeframes(pack('h',int(sample)))

	# params = [numChannels, sampleWidth, sampleRate , len(data), "NONE", None]
	# writewav(outfile, data, params)
	outfile.close()

main()
                