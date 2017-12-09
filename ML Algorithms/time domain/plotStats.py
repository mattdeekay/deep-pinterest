import matplotlib.pyplot as plt
import pickle
import numpy as np
import dill

import sys
sys.path.append("../utils/")
print sys.path
# import dataLoader
from dataLoader import loadData

class config:
	filename = "dev Featurized "

def runTimeDomainClusterAnalysis():
	timeClusterValMean = []
	timeClusterStdev = []
	for i in range(50):
		print "at timestep: ", i
		currFilename = config.filename + str(i) + ".pkl"

		currDict = loadData(currFilename)
		clusterAnalysis = [value[5] for value in currDict.values()]

		timeClusterValMean.append(np.mean(np.array(clusterAnalysis)))
		timeClusterStdev.append(np.std(np.array(clusterAnalysis)))

	print timeClusterStdev, timeClusterValMean
	plt.plot(range(len(timeClusterValMean)), timeClusterValMean)
	plt.plot(range(len(timeClusterStdev)), timeClusterStdev)
	plt.legend(["Time Cluster Mean", "Time Cluster Stdev"])
	plt.xlabel("Timestep Number")
	plt.ylabel("Mean Clustering Coefficient")
	plt.show()

def main():
	runTimeDomainClusterAnalysis()
		


if __name__ == "__main__":
	main()