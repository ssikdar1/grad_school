from cmath import exp
import math
from math import cos, sin, pi
import array
import contextlib
import wave
import cmath

def readwav(fname):
    with contextlib.closing(wave.open(fname)) as f:
        params = f.getparams()
        frames = f.readframes(params[3])
        numFrames=len(frames)
    #return array.array("h", frames), params
    return frames


def fft(x):   #x is assumed to be of length 2^k
	N= len(x)
	print N
	if(len(x)==1):
		return x
	even=fft(x[0::2])
	odd=fft(x[1::2])
	return ([(even[k] + exp(-2j*pi*k/N)*odd[k])/2 for k in range(N/2)] + [(even[k] - exp(-2j*pi*k/N)*odd[k])/2 for k in range(N/2)])
	


#run exaples


def getspectrogram(x):
	ansList=[]
	samples=len(x)
	N=2048
	W=4096
	for i in range(0,int(math.floor(samples/N))):
		# inp= x[i*N:(i*N)+W]
		inp = [1,1,1,1]
		ans= fft(inp)
		print(ans)
		ansList.append(ans)

	return ansList



def main():

	#ask user for input
    infileName = raw_input("Enter the name of the input .wav file: ")
    #ask for window size

    data = readwav(infileName)
    #print (len(data))

    getspectrogram(data)





main()