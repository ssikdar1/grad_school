import numpy
import math
import wave
import array
import contextlib
from math import sin, pi, cos
import cmath
import MFCC

# Global parameters
numChannels = 1                      # mono
sampleWidth = 2                      # in bytes, a 16-bit short
sampleRate = 44100

I = complex(0,1)
E = complex(2.718281,0)
 
 
# Read a wave file and return the entire file as an array, and the parameters
# Parameters are:  (numChannels, sampleWidth, sampleRate, numFrames, not-used, not-used)
def readwav(fname):
    with contextlib.closing(wave.open(fname)) as f:
        params = f.getparams()
        frames = f.readframes(params[3])
    return array.array("h", frames), params

#
# Fast Fourier Transform
#
#
def FFT(x):
    N = len(x)
    if N <= 1: return x
    even = FFT(x[0::2])
    odd =  FFT(x[1::2])
    return [(even[k] + cmath.exp(-2j*pi*k/N)*odd[k])/2 for k in xrange(N/2)] + \
           [(even[k] - cmath.exp(-2j*pi*k/N)*odd[k])/2 for k in xrange(N/2)]

#
# Taken from https://www.physics.rutgers.edu/~masud/computing/WPark_recipes_in_python.html
# TODO -- double check it gives the correct results.
#
#Inverse DFT with normalization by N, so that x == idft(dft(x)) within round-off errors.
def idft(X): 
	N, x = len(X), dft(X, sign=1) # e^{j2\pi/N}
	for i in range(N): 
		x[i] = x[i] / float(N) 
	return x
		   
#
# http://stackoverflow.com/questions/5835568/how-to-get-mfcc-from-an-fft-on-a-signal
#
def MFCC(signal):
	MFCC.MFCC()
		   
#
# Spectral Centroid
# It is calculated as the weighted mean of the frequencies present in the signal, determined using a Fourier transform, with their magnitudes as the weights:[2]
#
#where x(n) represents the weighted frequency value, or magnitude, of bin number n, and f(n) represents the center frequency of that bin.
#
# Ask Snyder about this?
#
def spectral_centroid(X):
	numerator = 0
	denominator = 0
	for n in range(0,len(X)):
		amplitude = round(cmath.polar(X[n])[0],2) 
		# frequency = round(cmath.polar(X[n])[1],2)
		frequency = n
		numerator = numerator + (frequency*amplitude**2)
		denominator = denominator + (amplitude**2)
	try:
		return (float(numerator)/denominator)
	except:
		return 0
		
def bandwidth(X,spectralCentroid):
	numerator = 0
	denominator = 0
	for n in range(0,len(X)):
		amplitude = round(cmath.polar(X[n])[0],2) 
		# frequency = round(cmath.polar(i)[1],2)
		frequency = n
		numerator = numerator + ((frequency-spectralCentroid)**2*amplitude**2)
		denominator = denominator + (amplitude**2)
	try:
		return math.sqrt(float(numerator)/denominator)
	except:
		return 0
		
#
# Spectral Standard Deviation and Mean of harmonic amplitudes from spectal envelope
# @param the signal and windowSize?
# @returns spectral mean, spectral std
def spectral_mean_std(data,windowSize,overlap):
	#Go through the signal for every window size calculate the spectral centroids
	spectralCentroids = []
	i = 0		
	while i < len(data)-windowSize-1:   # Ignoring the last incomplete window
		waves = []
		for j in range(0,windowSize):
			waves.append(data[i+j])

		i = i + overlap														# change i to the new overlap position
		spectrum = FFT(waves)												#Get the FFT results
		centroid = spectral_centroid(spectrum)								#Get the Spectral Centroid of the spectrum
		spectralCentroids.append(centroid)									#append to list
	# print spectralCentroids
	return numpy.mean(spectralCentroids),numpy.std(spectralCentroids)	

#
# Spectral Standard Deviation and Mean of harmonic amplitudes from spectal envelope
# @param the signal and windowSize?
# @returns normalized spectral mean, spectral std
#
# Using X - mu /std for standardizing
#
def normalized_spectral_mean_std(data,windowSize,overlap):
	#Go through the signal for every window size calculate the spectral centroids
	spectralCentroids = []
	i = 0		
	while i < len(data)-windowSize-1:   # Ignoring the last incomplete window
		waves = []
		for j in range(0,windowSize):
			waves.append(data[i+j])

		i = i + overlap														# change i to the new overlap position
		spectrum = FFT(waves)												#Get the FFT results
		centroid = spectral_centroid(spectrum)								#Get the Spectral Centroid of the spectrum
		spectralCentroids.append(centroid)									#append to list
	# print spectralCentroids
	mean = numpy.mean(spectralCentroids)
	std = numpy.std(spectralCentroids)
	normalizedCentroids = []
	for SC in spectralCentroids:
		SC = float(SC - mean)/std
		normalizedCentroids.append(SC)
	return numpy.mean(normalizedCentroids),numpy.std(normalizedCentroids)	
	
#
# Calculate the metrics for the bandwidth?
# @params 
#
def bandwidths_mean_std(data,windowSize,overlap):
	bandwidths = []
	i = 0		
	while i < len(data)-windowSize-1:   # Ignoring the last incomplete window
		waves = []
		for j in range(0,windowSize):
			waves.append(data[i+j])

		i = i + overlap														# change i to the new overlap position
		spectrum = FFT(waves)												#Get the FFT results
		centroid = spectral_centroid(spectrum)								#Get the Spectral Centroid of the spectrum
		bw = bandwidth(spectrum, centroid)							#Get the bandwidth
		bandwidths.append(bw)
	# print spectralCentroids
	return numpy.mean(bandwidths),numpy.std(bandwidths)	
#
# Calculate the metrics for the bandwidth?
# Normalization: using (X - mu)/std
#
def normalized_bandwidths_mean_std(data,windowSize,overlap):
	bandwidths = []
	i = 0		
	while i < len(data)-windowSize-1:   # Ignoring the last incomplete window
		waves = []
		for j in range(0,windowSize):
			waves.append(data[i+j])

		i = i + overlap														# change i to the new overlap position
		spectrum = FFT(waves)												#Get the FFT results
		centroid = spectral_centroid(spectrum)								#Get the Spectral Centroid of the spectrum
		bw = bandwidth(spectrum, centroid)							#Get the bandwidth
		bandwidths.append(bw)
	# print spectralCentroids
	return numpy.mean(bandwidths),numpy.std(bandwidths)	
#
#
# Short Time Energy
# 
#
def STE(X):
	sum = 0
	N = len(X)
	for n in range(0,N):
		sum += (X[n])**2
	return float(sum)/N
	
def average_STE(data,windowSize,overlap):
	#Go through the signal for every window size calculate the spectral centroids
	energy = []
	i = 0		
	while i < len(data)-windowSize-1:   # Ignoring the last incomplete window
		waves = []
		for j in range(0,windowSize):
			waves.append(data[i+j])

		i = i + overlap														# change i to the new overlap position
		energy.append(STE(X))
	return numpy.mean(energy)


#
# Cepstral Coefficients
# c(k) = IDFT({log(|DFT{X(n)}|)})
# TODO- Confirm on matlab or somehow that this is correct?
# ASK snyder about the M cofficients?
def cepstral_coefficients(X):
	pass 


def sign(x):
	if x > 1:
		return 1
	elif x == 0:
		return 0
	else: 				#x < 0
		return -1
#
# Zero Crossing Rate
#	@params the signal
#	@returns the zero crossing rate
def zero_crossing_rate(X):
	N = len(X)
	accum = 0
	for n in range(2,N):
		accum = accum + abs(sign(X[n]) - sign(X[n-1]))
	return float(accum)/N 


#
# Weiner entropy:
# Spectral flatness or tonality coefficient,[1][2] also known as Wiener entropy,[3][4] is a measure used in digital signal processing to characterize an audio spectrum. 
# Spectral flatness is typically measured in decibels, and provides a way to quantify how tone-like a sound is, as opposed to being noise-like.
# The spectral flatness is calculated by dividing the geometric mean of the power spectrum by the arithmetic mean of the power spectrum
# @params The sample of the signal
# @returns a number representing the tonality coefficient
def weiner_entropy(signal):
	complexSpectrum = numpy.fft.fft(signal)
	powerSpectrum = abs(complexSpectrum) ** 2
	
	numerator = 0
	denominator = 0
	N = len(powerSpectrum)
	for n in range(0,N):
		numerator += math.log(powerSpectrum[n])
		denominator += powerSpectrum[n]
	numerator = math.exp(float(numerator)/N)
	denominator = float(denominator)/N
	return float(numerator)/denominator
	
	
if __name__ == '__main__':
	wavName = raw_input("Please enter the name of the input .wav file name:")
	data, params = readwav(wavName)
	windowSize = 4096
	overlap = 2048
	mean,std = spectral_mean_std(data,windowSize,overlap)
	print 'Spectral Centroid mu:' + str(mean)
	print 'Spectral Centroid sigma:' + str(std)
	mean,std =  bandwidths_mean_std(data,windowSize,overlap)

