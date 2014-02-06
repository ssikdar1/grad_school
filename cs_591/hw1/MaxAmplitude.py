# Example of reading a WAV file using the Python wave library

import array
import wave                       # The main library for manipulating wave files


# Significant parameters
fileName =  raw_input("Enter name of file: ")
maxMagnitude = 0
minMagnitude = 0

# open wave file for reading
waveFile = wave.open(fileName, 'r')

# get the parameters
(numChannels, sampleWidth, sampleRate, numFrames, compressionType, nameOfCompression) = waveFile.getparams()
 
# how many frames to read each loop iteration?
numFramesToRead = 1
 
for i in range( 0, numFrames ):

     # in mono, frame will have one sample, in stereo, two
     frame = waveFile.readframes( numFramesToRead )    
     
     # unpack binary string into array of ints
     data = array.array('h',frame)
     
     for i in range(0,numChannels):
          if data[i] > maxMagnitude:
               maxMagnitude = data[i]

          if data[i] < minMagnitude:
               minMagnitude = data[i]

print("Number of channels: " + str(numChannels))

print("largest magnitude positive sample:" + str(maxMagnitude))

print(" largest magnitude negative sample value:" + str(minMagnitude))
    
waveFile.close()

    
