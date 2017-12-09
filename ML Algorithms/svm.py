'''
This module is a module that runs an SVM on the predictability of number of future links
with SVM regression 
'''

import numpy as np
import pickle
import dill
import copy

from sklearn.svm import SVR

import sys
sys.path.append("./utils/")
from dataLoader import loadData
import matplotlib.pyplot as plt

class config:
	num_timesteps = 2
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


	def calculateError(self, preds, labels):
		return np.mean(np.abs(preds - labels)/labels)

	def runAlgorithm(self):
		self.clf = SVR()
		self.clf.fit(self.train_data, self.train_labels)
		
		train_pred = self.clf.predict(self.train_data)
		dev_pred = self.clf.predict(self.dev_data)
		test_pred = self.clf.predict(self.test_data)

		print ("train label mean is: ", np.mean(self.train_labels))
		print ("dev label mean is: ", np.mean(self.dev_labels))
		print ("test label mean is: ", np.mean(self.test_labels))

		train_error, dev_error, test_error = self.calculateError(train_pred, self.train_labels), self.calculateError(dev_pred, self.dev_labels),\
		 									self.calculateError(test_pred, self.test_labels)

		print ("training error is: ", train_error)
		print ("dev error is: ", dev_error)
		print ("test error is: ", test_error)

		return train_error, dev_error, test_error

		#this metric doesn't work 
		# print ("training error is: ", np.mean(train_pred/self.train_labels))
		# print ("dev error is: ", np.mean(dev_pred/self.dev_labels))


def createTimestep(dataset, labels, currTimestep, nextTimestep):
	for key in currTimestep:
		dataset.append(currTimestep[key][:])
		labels.append(nextTimestep[key][0])

	return dataset, labels

def getData(filename, filepath, dataset, labels, timestep = None):
	assert(timestep is not None)
	print "at timestep: ", timestep
	currFilename = filename + str(timestep) + ".pkl"
	nextFilename = filename + str(timestep+1) + ".pkl"

	currTimestep = loadData(currFilename, filepath)
	nextTimestep = loadData(nextFilename, filepath)

	dataset, labels = createTimestep(list(dataset), list(labels), currTimestep, nextTimestep)
	return np.array(dataset), np.array(labels)

def runTimeAnalysis():
	def plotError(error):
		trainError = [currErr[0] for currErr in error]
		devError = [currErr[1] for currErr in error]
		testError = [currErr[2] for currErr in error]

		print trainError, devError, testError

		num_timesteps = len(trainError)

		plt.plot(range(num_timesteps), trainError)
		plt.plot(range(num_timesteps), devError)
		plt.plot(range(num_timesteps), testError)

		plt.xlabel("Timestep Number")
		plt.ylabel("Error")

		plt.legend(['Training Set', 'Dev Set', 'Test Set'])
		plt.savefig('Time Domain Complete SVM')

	error = []
	trainDataset, trainLabels = ([], [])
	devDataset, devLabels = ([], [])
	testDataset, testLabels = ([], [])
	for i in range(config.num_timesteps):
		trainDataset, trainLabels = getData(config.train_filename, config.train_filepath, trainDataset, trainLabels, timestep = i)
		devDataset, devLabels = getData(config.dev_filename, config.dev_filepath, devDataset, devLabels, timestep = i)
		testDataset, testLabels = getData(config.test_filename, config.test_filepath, testDataset, testLabels, timestep = i)

		print ("size of training set is: ", trainLabels.shape, trainDataset.shape)
		print ("size of dev set is: ", devLabels.shape, devDataset.shape)
		print ("size of test set is: ", testLabels.shape, testDataset.shape)

		currMLRun = MLAlgorithm(trainDataset, trainLabels, devDataset, devLabels, testDataset, testLabels)

		error.append(copy.copy(currMLRun.runAlgorithm()))
	plotError(error)



def main():
	runTimeAnalysis()

if __name__ == "__main__":
	main()