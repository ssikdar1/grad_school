# Example of creating a mono WAV file using the Python wave library

from struct import pack           # This creates the binary data structure for frames
from math import sin, pi
import wave                       # The main library for manipulating wave files

# Significant parameters
fileName = 'sinusoid.wav'
numberChannels = 1     # mono
sampleWidth = 2        # in bytes, so this is a 16-bit int (a short in C)
sampleRate = 44100
#frequency = 440.0     # keep this a float so calculation below is floating-point
lengthSeconds = 6      # how long the file is in seconds

# dependent variables

#maximum amplitude is 2**15 - 1  = 0111 1111 1111 1111 = 32767 
maxAmplitude = 2**(8*sampleWidth - 1) - 1.0      # keep this a float

# open wave file for writing
waveFile = wave.open(fileName, 'w')

#    setparams(nchannels, sampleWidth (in bytes), sampleRate, numFrames, compressionType, nameOfCompressionType) 
#      last two parameters not supported, leave as shown
#      numFrames is 0 for now and will be updated later
waveFile.setparams((numberChannels, sampleWidth, sampleRate, 0, 'NONE', 'not compressed'))

waveData=""       # this holds the data to be written to file in binary form


for i in range( 0, sampleRate * lengthSeconds ):
     
        #  2 * pi * frequency is the angular velocity in radians/sec
        #  multiplying this by i / sampleRate incrementally creates angle at each sample
        #  and then sin ( angle ) => amplitude at this sample
	
#	a sinusoid composed of the sum of four sine waves of frequency 440, 880, 1760, and 3520, in which the amplitude of the 440 wave is half the maximum amplitude, 880 is 1/4th, 1760 is 1/8th, and 3520 is 1/8th. 

        frame = (maxAmplitude/2) * sin( 2 * pi * 440.0 * i / sampleRate ) + (maxAmplitude/4) * sin( 2 * pi * 880.0 * i / sampleRate ) + (maxAmplitude/8) * sin( 2 * pi * 1760 * i / sampleRate )  + (maxAmplitude/8) * sin( 2 * pi * 3520 * i / sampleRate )      
        waveData += pack( 'h', frame )
   
    
# write the frames; this will automatically update the number of frames in numFrames       
waveFile.writeframes(waveData)
waveFile.close()

    
