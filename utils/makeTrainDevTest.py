'''
Split every timestep into a timestep for tarin/dev/test
'''


import pickle
import numpy as np
import dill
import collections
import random

class config:
	mainPath = "../Datasets/ML Dataset/"

	trainPath = "train/"
	devPath = "dev/"
	testPath = "test/"

	devPercent = 0.1
	testPercent = 0.1

def dumpFile(flattenedList, filename):
	currDict = collections.defaultdict(lambda: [])
	for tup in flattenedList:
		time, board_id, pin_id = tup
		currDict[time].append((board_id, pin_id))

	with open(config.mainPath + filename + ".pkl", "wb") as f:
		pickle.dump(currDict, f)


def splitFile(filename, outNum, filepath = "../Datasets/parsedData/"):
	random.seed(10) 
	with open(filepath + filename, "rb") as f:
		timePinBoard = pickle.load(f)
	flattenedList = []
	for time in timePinBoard:
		for tup in timePinBoard[time]:
			board_id, pin_id = tup
			flattenedList.append((time, board_id, pin_id))
	# print flattenedList[:10]
	random.shuffle(flattenedList)
	# print flattenedList[:10]

	num_entries = len(flattenedList)

	numDev = int(config.devPercent * num_entries)
	numTest = int(config.testPercent * num_entries)

	devSet = flattenedList[:numDev]
	testSet = flattenedList[numDev: numDev + numTest]
	trainSet = flattenedList[numDev + numTest:]

	dumpFile(devSet, config.devPath + "dev " + str(outNum))
	dumpFile(testSet, config.testPath + "test " + str(outNum))
	dumpFile(trainSet, config.trainPath + "train " + str(outNum))

def makeDatasets():
	for i in range(50):
		splitFile("boardPin" + str(i) + ".pkl", i)

	# splitFile("boardPin0.pkl", 0)


def main():
	makeDatasets()

if __name__ == "__main__":
	main()