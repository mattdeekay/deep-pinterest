'''
This module is to preprocess the pin data to get pin characteristics 
'''

import networkx as nx
import pickle
import dill
import collections

class config:
	board_token = "b"
	pin_token = "p"

def loadData(file, path = "../Datasets/parsedData/"):
	with open(path + file, "rb") as f:
		return pickle.load(f)

#gets the degree of nodes in a graph
def getGraphDegree(graph, indicator):
	degreeMap = collections.defaultdict(int)
	for node in list(graph.nodes()):
		if 'b' not in node: continue

		degreeMap[graph.degree(node)] += 1
	return degreeMap

#update the graph with new nodes/edges
#created from boards pins
def addToGraph(graph, timeDict, boardSet, pinSet):
	for time in timeDict:
		for tup in timeDict[time]:
			board_id, pin_id = tup

			pin_id = config.pin_token + pin_id
			board_id = config.board_token + board_id
			
			graph.add_node(board_id)
			graph.add_node(pin_id)

			graph.add_edge(board_id, pin_id)
			graph.add_edge(pin_id, board_id)
	


	return graph, boardSet, pinSet


def createTimeAnalysis():
	boardDict = loadData("boardDict.pkl")
	pin1 = loadData("boardPin0.pkl")

	boardPinGraph = nx.Graph()
	boardSet = set()
	pinSet = set()
	boardPinGraph, boardSet, pinSet = addToGraph(boardPinGraph, pin1, boardSet, pinSet)



def main():
	createTimeAnalysis()





if __name__ == "__main__":
	main()