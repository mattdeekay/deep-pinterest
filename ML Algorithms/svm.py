'''
This module is a module that runs an SVM on the predictability of number of future links
with SVM regression 
'''

import numpy as np
import pickle
import dill

from sklearn.svm import SVR

import sys
sys.path.append("./utils/")
from dataLoader import loadData

class config:
	num_timesteps = 5
	train_filename = "dev Featurized "
	dev_filename = "dev Featurized "
	test_filename = "test Featurized "


	train_filepath = "../Datasets/Deep Learning Parsed/Train/"
	dev_filepath = "../Datasets/Deep Learning Parsed/Dev/"
	test_filepath = "../Datasets/Deep Learning Parsed/Test/"



class MLAlgorithm:
	def __init__(self, train_data, train_labels, dev_data, dev_labels, test_data, test_labels):
		self.train_data = train_data
		self.train_labels = train_labels
		self.dev_data = dev_data
		self.dev_labels = dev_labels
		self.test_data = test_data
		self.test_labels = test_labels

		self.runAlgorithm()

	def runAlgorithm(self):
		self.clf = SVR()
		self.clf.fit(self.train_data, self.train_labels)
		
		train_pred = self.clf.predict(self.train_data)
		dev_pred = self.clf.predict(self.dev_data)

		print ("training accuracy is: ", np.abs(train_pred - self.train_labels))
		print ("dev accuracy is: ", np.abs(dev_pred - self.dev_labels))


def createTimestep(dataset, labels, currTimestep, nextTimestep):
	for key in currTimestep:
		dataset.append(currTimestep[key][:])
		labels.append(nextTimestep[key][0])

	return dataset, labels

def getData(filename, filepath):
	dataset = []
	labels = []
	for i in range(config.num_timesteps-1):
		print "at timestep: ", i
		currFilename = filename + str(i) + ".pkl"
		nextFilename = filename + str(i+1) + ".pkl"

		currTimestep = loadData(currFilename, filepath)
		nextTimestep = loadData(nextFilename, filepath)

		dataset, labels = createTimestep(dataset, labels, currTimestep, nextTimestep)
	return np.array(dataset), np.array(labels)

def main():
	trainDataset, trainLabels = getData(config.train_filename, config.train_filepath)
	devDataset, devLabels = getData(config.dev_filename, config.dev_filepath)
	testDataset, testLabels = getData(config.test_filename, config.test_filepath)

	print ("size of training set is: ", trainLabels.shape, trainDataset.shape)
	print ("size of dev set is: ", devLabels.shape, devDataset.shape)
	print ("size of test set is: ", testLabels.shape, testDataset.shape)

	MLAlgorithm(trainDataset, trainLabels, devDataset, devLabels, testDataset, testLabels)

if __name__ == "__main__":
	main()