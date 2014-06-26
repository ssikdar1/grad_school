import numpy as np
import array
import contextlib
import wave
import math


def readwav(fname):
    with contextlib.closing(wave.open(fname)) as f:
        params = f.getparams()
        frames = f.readframes(params[3])
    return array.array("h", frames), params


def peak_picking(X,M,G,L):
    print "peak_picking"
    for i in range(M,len(X)):
        if(X[i-1] < X[i] > X[i+1]):
            if(X[i] > G and X[i] > (L + np.mean(X[i-M:i+M]))):
                print "pick ",i
                return i  #return the first auto correlation no.   
    return 0

def lowpassfilter(signal):
	result = []
	length = len(signal)
	for i in range(length):
		if i <= 91:
			result.append(signal[i])
		else:
			temp = 0.0
			for j in range(91):
				temp += filter_taps[j] * signal[i-91+j]
			result.append(temp)
	return result
	
def auto_correlation(X,Y):
    X = np.array(X)
    Y = np.array(Y)
    #calculate mu and sigma for the two signals
    xmean = np.mean(X)
    ymean = np.mean(Y)
    xstd = np.std(X)
    ystd = np.std(Y)
    return np.mean(((X - xmean)*(Y - ymean))/(xstd*ystd))

def pitch(data):
    deltaTime = .25  #Get a segment of the signal(0.25second)
    time_stamp = raw_input("Please Enter Time Stamp: ")
    start = int(float(time_stamp)* 44100) #calculate the start no. of the sample
    length = int(deltaTime*44100)
    print len(data)
    signal = lowpassfilter(data)

    Z = [0]*1000  #the list of corelation values, initialized it with 0
    period = 0
    # t is width of period in samples; this gives a range of frequencies from 44.1 to 4000
    for t in range(11,1000):
        Z[t] = auto_correlation(signal[start:start+length],signal[start+t:start+t+length])
    result= peak_picking(Z,40,0.5,0.1)  #I set M=40,G=0.5,L=0.1
    print result
    print(signal[start+result])
    print Z[result]
    print"The pitch frequency is :", 44100.0/result


filter_taps = [
  -0.009089011175360007,                   
  -0.010966547421213816,                 
  -0.015078165397379715,
  -0.017805673508754144,
  -0.01815103119769253,
  -0.015459737770557582,
  -0.00984513643011805,
  -0.00211946054230909,
  0.006167565401196312,
  0.013246455435226012,
  0.0174479472600178,
  0.01785275994034983,
  0.014459704181789748,
  0.00840599210268457,
  0.0015414678274348894,
  -0.003932107107380872,
  -0.006284293198261678,
  -0.004665818415892383,
  0.0004244905304238232,
  0.007382755690908084,
  0.013809242841450027,
  0.017421469433675996,
  0.016669213331047213,
  0.011470286470599497,
  0.00320889023894959,
  -0.005459575015135154,
  -0.011559615683304256,
  -0.012627503999129028,
  -0.007770193163856454,
  0.0020054033283729037,
  0.013772881556565721,
  0.023590364505745632,
  0.027551571518017803,
  0.023296616738804704,
  0.010816899382011755,
  -0.006932840499966107,
  -0.0247137604126788,
  -0.03606137561785161,
  -0.035164388418078285,
  -0.018438862026238567,
  0.014023801853967847,
  0.05825969312327917,
  0.1068999165549689,
  0.1509052893995529,
  0.18150510111844617,
  0.1924777681472577,
  0.18150510111844617,
  0.1509052893995529,
  0.1068999165549689,
  0.05825969312327917,
  0.014023801853967847,
  -0.018438862026238567,
  -0.035164388418078285,
  -0.03606137561785161,
  -0.0247137604126788,
  -0.006932840499966107,
  0.010816899382011755,
  0.023296616738804704,
  0.027551571518017803,
  0.023590364505745632,
  0.013772881556565721,
  0.0020054033283729037,
  -0.007770193163856454,
  -0.012627503999129028,
  -0.011559615683304256,
  -0.005459575015135154,
  0.00320889023894959,
  0.011470286470599497,
  0.016669213331047213,
  0.017421469433675996,
  0.013809242841450027,
  0.007382755690908084,
  0.0004244905304238232,
  -0.004665818415892383,
  -0.006284293198261678,
  -0.003932107107380872,
  0.0015414678274348894,
  0.00840599210268457,
  0.014459704181789748,
  0.01785275994034983,
  0.0174479472600178,
  0.013246455435226012,
  0.006167565401196312,
  -0.00211946054230909,
  -0.00984513643011805,
  -0.015459737770557582,
  -0.01815103119769253,
  -0.017805673508754144,
  -0.015078165397379715,
  -0.010966547421213816,
  -0.009089011175360007
]		
	
if __name__ == '__main__':
    infileName = raw_input("Enter the name of the input .wav file: ")
    data, params = readwav(infileName)
    #print len(filter_taps)
    pitch(data)
   # drawGraph(data[:500])