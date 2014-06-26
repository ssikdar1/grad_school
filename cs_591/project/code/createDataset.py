#
# Create Dataset
#
#
import os, os.path
import csv
# import featureExtraction as features
from pymir import AudioFile
import numpy

# directory = "C:\Users\Shan\Documents\GitHub\grad_school\cs_591\project\\birds\chicken"
directory = "C:\Users\Shan\Downloads\Canada Goose\warbler_test"

with open('BirdsDataset.csv', 'w') as csvfile:
	outwriter = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
	# header = ['File','SC_mu','SC_sigma','Bandwidth_mean', 'Bandwidth_sigma','ZCR', 'STE','Weiner']
	# outwriter.writerow(header)
	for root, _, files in os.walk(directory):
		print "# of files: " + str(len(files))
		ctr = 0
		for f in files:
			print str(ctr) + " :" + f
			ctr += 1
			fullpath = os.path.join(root, f)
			row = []
			row.append(f)
		
			wavData = AudioFile.open(fullpath)
			
			windowFunction = numpy.hamming
			fixedFrames = wavData.frames(1024, windowFunction)
			
			
			
			#
			# Temporal Features
			#
			#
						
			ZCR = []
			for i in range(0,len(fixedFrames)):
				zcr = fixedFrames[i].zcr()
				if numpy.isnan(numpy.min(zcr)):
					zcr = 0
				ZCR.append(zcr)
			row.append(numpy.mean(ZCR))
			row.append(numpy.std(ZCR))				

			RMS = []
			for i in range(0,len(fixedFrames)):
				rms = fixedFrames[i].rms()
				if numpy.isnan(numpy.min(rms)):
					rms = 0				
				RMS.append(rms)
			row.append(numpy.mean(RMS))
			row.append(numpy.std(RMS))				
			
			
			
			#
			# Spectral Features
			#
			#
			
			
			# Compute the spectra of each frame
			spectra = [f.spectrum() for f in fixedFrames]
			
			# Spectral Centroid
			centroid = []
			for i in range(0,len(spectra)):
				cent = spectra[i].centroid()
				if numpy.isnan(numpy.min(cent)):
					cent = 0
				centroid.append(cent)
			
			row.append(numpy.mean(centroid))
			row.append(numpy.std(centroid))
				
			#Spectral Mean
			smean = []
			for i in range(0,len(spectra)):
				smean.append(spectra[i].mean())
			row.append(numpy.mean(smean))
			row.append(numpy.std(smean))					
				
			# Spectral Variance
			svar = []
			for i in range(0,len(spectra)):
				var = spectra[i].variance()
				if numpy.isnan(numpy.min(var)):
					c = 0				
				svar.append(var)
			row.append(numpy.mean(svar))
			row.append(numpy.std(svar))			

			#Spectral Crest()
			screst = []
			for i in range(0,len(spectra)):
				crest = spectra[i].crest()
				if numpy.isnan(numpy.min(crest)):
					crest = 0
				screst.append(crest)
			
			row.append(numpy.mean(screst))
			row.append(numpy.std(screst))			
			
			# Spectral Kurtosis
			skurtosis = []
			for i in range(0,len(spectra)):
				kurt = spectra[i].kurtosis()
				if numpy.isnan(numpy.min(kurt)):
					kurt = 0
				skurtosis.append(kurt)
			row.append(numpy.mean(skurtosis))
			row.append(numpy.std(skurtosis))				

			# Spectral Rolloff
			srolloff = []
			for i in range(0,len(spectra)):
				roll = spectra[i].rolloff()
				if numpy.isnan(numpy.min(roll)):
					roll = 0
				srolloff.append(roll)
			row.append(numpy.mean(srolloff))


			# Spectral Spread
			spread = []
			for i in range(0,len(spectra)):
				spr = spectra[i].spread()
				if numpy.isnan(numpy.min(spr)):
					spr = 0	
				spread.append(spr)
			row.append(numpy.mean(spread))
					

			outwriter.writerow(row)