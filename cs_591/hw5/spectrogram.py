from math import sin, cos, pi, log
import wave                       # The main library for manipulating wave files
import cmath
import time
import FFT
import array

#define imaginary number
I = complex(0.0,1.0)

#important parameters
windowSize = 4096   #Window size
overlap = 2048   #Overlapping number


def getEnv(inputWave):
    # open wave file for reading
    inputWaveFile = wave.open(inputWave, 'r')

    # get the parameters
    (numChannels, sampleWidth, sampleRate, numFrames, compressionType, nameOfCompression) = inputWaveFile.getparams()
 
    # generate the envelope for stereo file
    waves = []
    for i in range(0,numFrames):
         frame = inputWaveFile.readframes(1)   # read 1 frame each loop iteration
     
         # unpack binary string into array of ints
         data = array.array('h',frame)
         #env.append((data[0], data[1]))   # for stereo, left then right
         waves.append(data[0])   # for mono
    
    inputWaveFile.close()
    return waves


def getSpectrogram(x):
    spectrums = []
    i = 0
##    print len(x)
    while i < len(x)-windowSize-1:   # I ignore the last incomplete window, or we could deal with it using padding technique
        # For a new window, initiate a list
        waves = []
        for j in range(0,windowSize):
            waves.append(x[i+j])
        win = FFT.FFT(waves)
        spectrums.append(win)
        i = i + overlap
    return spectrums

def generatePair(x):
    pairs = []
    length = len(x)
    for i in range(0,length):
        maxAbs = (len(x[i])-1)/2
        pair = []
        for j in range(0,maxAbs+1):
            # Maybe we can make a filter here later, only record those amp > a(a>0)
            pair.append(str(round(2.0*log(cmath.polar(x[i][j])[0]),2)))
        pairs.append(pair)
    return pairs

def saveResults(filename,results):
    outputFile = open(filename,'w')
    # every row in the file is the records of amplitudes for a window
    for i in range(0,len(results)):
        line = ''
        for j in range(0,len(results[i])):
            line += str(results[i][j]) + ' '
        outputFile.writelines(line+'\n')
    outputFile.close()

if __name__ == '__main__':
    ###Rockrunner
    ##s = getSpectrogram(getEnv("birds/test.wav"))

    ###Warbler
    ##wavName = "birds/test3.wav"
    ##s = getSpectrogram(getEnv(wavName))
        
##    #Northern Goshawk
##    wavName = "birds/test2.wav"

    wavName = raw_input("Please enter the name of the input .wav file name:")
    
    s = getSpectrogram(getEnv(wavName))
    result = generatePair(s)
    outputFile = wavName.replace('.wav','.txt')
    saveResults(outputFile,result)
    print "Finished!"

