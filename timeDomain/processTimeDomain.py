import snap
import numpy as np
import matplotlib.pyplot as plt
import collections

class config:
	erdos_graph = "../Datasets/SIR_erdos_renyi.txt"
	preferential_graph = "../Datasets/SIR_preferential_attachment.txt"
	num_simulations = 98

def loadOtherGraphs(filename):
	with open(filename, "rb") as f:
		graph = snap.PUNGraph.New() #creating a new graph that can handle multiple edges

		for i, line in enumerate(f):
			if i < 4: continue
			n1, n2 = line.strip("\n").split("\t")
				
			if not graph.IsNode(int(n1)): graph.AddNode(int(n1))
			if not graph.IsNode(int(n2)): graph.AddNode(int(n2))
			
			graph.AddEdge(int(n1), int(n2))
	return graph

def loadData(filename = "timedomain100stepspartialdataset.txt"):
	def parseDefaultdict(lineParse):
		currDict = collections.defaultdict(int)
		s = lineParse.find("{")
		lineParse = lineParse[s+1:-3]
		lineParse = lineParse.split(",")
		for entry in lineParse:
			entry = entry.split(":")
			currDict[int(entry[0])] = int(entry[1])
		return currDict

	with open(filename, "rb") as f:
		timeStepDict = {}
		counter = 0
		for i, line in enumerate(f):
			if i < 30: continue
			if (i + 12) % 23 == 0:
				currTimestep = parseDefaultdict(line)
				timeStepDict[config.num_simulations - counter] = currTimestep
				counter += 1
		return timeStepDict

#plotting timesteps 
def plotTimesteps(timeStepDict, timeList = [i for i in [2, 3, 4, 10, 45, 98]]):
	def plotCurrDict(currTimestep):
		tot = sum([currTimestep[key] for key in currTimestep.keys() if key != 0])

		pairwise = [(val, 1. * currTimestep[val]/tot) for val in currTimestep.keys() if val != 0]

		pairwise = sorted(pairwise)

		xaxis = [val[0] for val in pairwise]
		yaxis = [val[1] for val in pairwise]

		plt.plot(xaxis, yaxis)


	for i in timeStepDict:
		if i in timeList:
			print "plotted: ", i
			plotCurrDict(timeStepDict[i])
			plt.xscale('log')
			plt.yscale('log')

	print timeStepDict.keys()


	plt.xlabel("Node Degree")
	plt.ylabel("Probability")

	plt.legend(["erdos", "preferential"] + ["i = " + str(val-1) for val in timeList])
	# plt.legend(["i = " + str(val) for val in timeList])
	plt.savefig('Time Domain Distribution')

class plotGraphs:
	def __init__(self):
		for filename in [config.erdos_graph, config.preferential_graph]:
			self.loadAndPlot(filename)


	def loadAndPlot(self, filename):
		currGraph = loadOtherGraphs(filename)
		xCurrGraph, yCurrGraph = self.getDataPointsToPlot(currGraph)
		plt.plot(xCurrGraph, yCurrGraph)
		print "FINISHED PLOTTING"


	

	def getDataPointsToPlot(self, Graph):
		"""
		:param - Graph: snap.PUNGraph object representing an undirected graph
		
		return values:
		X: list of degrees
		Y: list of frequencies: Y[i] = fraction of nodes with degree X[i]
		"""
		############################################################################
		# TODO: Your code here!
		X, Y = [], []
		
		degree_vec = snap.TIntPrV() #degree vector
		snap.GetOutDegCnt(Graph, degree_vec)
		
		X = [item.GetVal1() for item in degree_vec]
		counts = [item.GetVal2() for item in degree_vec]

		degree_tot = sum(counts)
		Y = [item.GetVal2()/(1.0 * degree_tot) for item in degree_vec]

		############################################################################
		return X, Y


def main():
	timeStepDict = loadData()
	plotGraphs()
	plotTimesteps(timeStepDict)


if __name__ == "__main__":
	main()