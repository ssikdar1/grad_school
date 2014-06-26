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
directory = "C:\Users\Shan\Downloads\Canada Goose\goose_test"

with open('BirdsDataset.csv', 'w') as csvfile:
	outwriter = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
	# header = ['File','SC_mu','SC_sigma','Bandwidth_mean', 'Bandwidth_sigma','ZCR', 'STE','Weiner']
	# outwriter.writerow(header)
	for root, _, files in os.walk(directory):
		print "# of files: " + str(len(files))
		i = 0
		for f in files:
			print str(i) + " :" + f
			i += 1
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
				ZCR.append(fixedFrames[i].zcr())
			row.append(numpy.mean(ZCR))
			row.append(numpy.std(ZCR))				

			RMS = []
			for i in range(0,len(fixedFrames)):
				RMS.append(fixedFrames[i].rms())
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
				centroid.append(spectra[i].centroid())
			row.append(numpy.mean(centroid))
			row.append(numpy.std(centroid))
				
			# # Spectral Flatness
			# flatness = []
			# for i in range(0,len(spectra)):
				# flatness.append(spectra[i].flatness())
			# row.append(numpy.mean(flatness))
			# row.append(numpy.std(flatness))		
			
			#Spectral Mean
			smean = []
			for i in range(0,len(spectra)):
				smean.append(spectra[i].mean())
			row.append(numpy.mean(smean))
			row.append(numpy.std(smean))					
				
			# Spectral Variance
			svar = []
			for i in range(0,len(spectra)):
				svar.append(spectra[i].variance())
			row.append(numpy.mean(svar))
			row.append(numpy.std(svar))			

			#Spectral Crest()
			screst = []
			for i in range(0,len(spectra)):
				screst.append(spectra[i].crest())
			row.append(numpy.mean(screst))
			row.append(numpy.std(screst))			
			
			# Spectral Kurtosis
			skurtosis = []
			for i in range(0,len(spectra)):
				skurtosis.append(spectra[i].kurtosis())
			row.append(numpy.mean(skurtosis))
			row.append(numpy.std(skurtosis))				

			# Spectral Rolloff
			srolloff = []
			for i in range(0,len(spectra)):
				srolloff.append(spectra[i].rolloff())
			row.append(numpy.mean(srolloff))
			row.append(numpy.std(srolloff))				

			# Spectral Skewness
			skewness = []
			for i in range(0,len(spectra)):
				srolloff.append(spectra[i].skewness())
			row.append(numpy.mean(skewness))
			row.append(numpy.std(skewness))	
			
			# Spectral Spread
			spread = []
			for i in range(0,len(spectra)):
				srolloff.append(spectra[i].spread())
			row.append(numpy.mean(spread))
			row.append(numpy.std(spread))				
						



			outwriter.writerow(row)