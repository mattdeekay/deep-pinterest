import collections
import matplotlib.pyplot as plt
from processTimeDomain import loadData, plotGraphs, loadOtherGraphs

class config:
	erdos_graph = "../Datasets/SIR_erdos_renyi.txt"
	preferential_graph = "../Datasets/SIR_preferential_attachment.txt"
	num_simulations = 98	


class getGraphData(plotGraphs):
	def __init__(self):
		for filename in [config.preferential_graph]:
			self.loadAndPlot(filename)

	def loadAndPlot(self, filename):
		currGraph = loadOtherGraphs(filename)
		self.xCurrGraph, self.yCurrGraph = self.getDataPointsToPlot(currGraph)

def plotDict(inputDict):
	pairwise = [(key, inputDict[key]) for key in inputDict]
	xaxis = [pair[0] for pair in pairwise]
	yaxis = [pair[1] for pair in pairwise]
	plt.plot(xaxis, yaxis)

def plotTimestepComparison(timeDict, comparison, normalize = True):
	def runNormal(comparison, currTimestep, i):
		stepMax = max(currTimestep.keys())
		compMax = max(comparison.keys())
		newDict = collections.defaultdict(int)
		for key in comparison:
			newDict[int(1. * stepMax * key/ compMax)] = comparison[key]
		print sorted(newDict.keys()), "\n\n"

		# if i == 0 or i == 98:
			# plotDict(newDict)
			# plotDict(currTimestep)

		# if i == 98:
			# plt.xscale("log")
			# plt.yscale("log")
			# plt.show()

		return newDict

	def runComparison(currDict, i):
		currComparison = comparison
		if normalize:
			currComparison = runNormal(comparison, currDict, i)

		keyList = list(set(timeDict.keys() + currComparison.keys()))
		diff = sum([(currDict[key]- currComparison[key]) **2 for key in keyList])
		# print diff
		return diff

	def timestepNorm(currStep):
		tot = sum([currStep[key] for key in currStep.keys() if key != 0])
		normalizedDict = collections.defaultdict(int)
		for val in currStep:
			if val == 0: continue
			normalizedDict[val] = 1. * currStep[val]/tot
		return normalizedDict

	comparisonDict = {}
	for i in timeDict:
		currStep = timeDict[i]
		currStep = timestepNorm(currStep)

		comparisonDict[i] = runComparison(currStep, i)

	pairwise = sorted([(key, comparisonDict[key]) for key in comparisonDict])

	xaxis = [key[0] for key in pairwise]
	yaxis = [key[1] for key in pairwise]

	plt.plot(xaxis, yaxis, "o")
	plt.xlabel("i value")
	plt.ylabel("loss")
	# plt.savefig("Normalized Difference")
			


def main():
	timeStepDict = loadData()
	graphData = getGraphData()
	nodeDegree, distribution = graphData.xCurrGraph, graphData.yCurrGraph
	preferentialMap = collections.defaultdict(int)

	for i in range(len(nodeDegree)):
		preferentialMap[nodeDegree[i]] = distribution[i]

	plotTimestepComparison(timeStepDict, preferentialMap, normalize = True)


if __name__ == "__main__":
	main()