from features import mfcc
from features import logfbank
import scipy.io.wavfile as wav
import numpy

#birdName = 'Laysan Albatross'
birdName = 'WilsonWarbler'
numOfFile = 82
	

def generateMFCC(filename):
	(rate,sig) = wav.read(filename)
	mfcc_feat = mfcc(sig,rate)
	#fo = open(filename[:-4]+'.txt','w')
	numOfRow = 0
	sum = [0]*13
	for row in mfcc_feat:
		if numpy.isnan(numpy.min(row[1])):
			continue
		numOfRow += 1
		for i in range(13):
			sum[i] += row[i]

	fo.write(filename+',')
	for item in sum:
		fo.write(str(item/numOfRow)+',')
	fo.write('\n')
	#		fo.write(str(feat)+' ')
	#	fo.write('\n')
	#fo.close()


if __name__ == '__main__':
	fo = open('Features of '+birdName+'.csv','w')
	for i in range(0,numOfFile):
		fileName = birdName+str(i)+'.wav'
		print 'Generating '+fileName+' ...'
		try:
			generateMFCC(fileName)
		except:
			print "Error"
	fo.close()
	print 'Done'