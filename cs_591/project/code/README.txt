README:

Shan Sikdar
Chang Liu
Yike Xue


Below contains README for all code for feature extraction and mahcine learning

Languages Used:
Matlab
Python

Libraries Used:
pymir
pydub - used to conver mp3's to wav
speech features.


Feature Extraction:

getMp3's: a script we used to download songs from an online dataset in mp3 format

Spectral and Temporal Features
createDataset.py - creates the spectral and temporal features for a set of songs
featureExtraction.py - an implementation for calculating features given a window
pymir - python music information retrevial library used to extract certain features
----------------------------------
-Uses the PyMIR library found at https://github.com/jsawruk/pymir
-open createDataset.py
-choose what directory your audio files are located in
-run createDataset.py

MFCC's
mfcc.py - calculates the MFCC's
-----------------
-Utilizes Python speech features that can be found at  https://github.com/jameslyons/python_speech_features
mfcc.py - calculates the average for every MFCC's for every sound clip

Pitch Detector
-------------------
pitchDetector.py - genereates file of several rows of 9 numbers that are a pitchs for 9 seconds at each second. Each row is for one bird.


SVM
multisvm - a matlab extension to svm for mutliple classes using 1vs all
svm_attempt - short matlab script to run multisvm
--------
-open svm_attempt.m and mutlisvm.m in matlab.
-load the training and testing set.
-decide what funcition you want to choose in multisvm
- run svm_attempt.

PCA
--------
Reduces the dimension of the data set
run pca_dimen_reduc.m


NN
-------------
-Used NN toolbox, the dataset we used is called 'datasetNew.csv', the label file is called 'labelNew.csv'. The samples are 'Matrix rows'.
 Setting the #units in hidden layer to be 10, and 70% as training data, 15% as validation data, 15% as testing data.

KNN
------
- was run using Weka
