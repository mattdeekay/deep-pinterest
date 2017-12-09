'''
This module is to preprocess the pin data to get pin characteristics 
'''
import numpy as np
import networkx as nx
import pickle
import dill
import collections
import time

class config:
	board_token = "b"
	pin_token = "p"

	# outPath = "../Datasets/Deep Learning Parsed/Dev/"
	outPath = "/cvgl2/u/bcui/CS 224w/Datasets/Deep Learning Parsed/Train/"
	num_timesteps = 50

	currFile = "train "

def loadData(file, path = "/cvgl2/u/bcui/CS 224w/Datasets/ML Dataset/Train/"):#"../Datasets/ML Dataset/Dev/"):
	with open(path + file, "rb") as f:
		return pickle.load(f)

#gets the degree of nodes in a graph
#mean neighbor degree for board and pins
def getGraphDegree(graph):
	assert(nx.is_frozen(graph))
	# pinNeighbors = collections.defaultdict(lambda: []) #pinId : list(pint node degrees)
	# boardNeighbors = collections.defaultdict(lambda: []) #pinId : list(board node degrees)

	pinOut = collections.defaultdict(lambda: [])
	# boardOut = collections.defaultdict(int)

	for k, node in enumerate(list(graph.nodes())):
		if config.pin_token not in node: continue #only count pins

		currPinList = []
		currBoardList = []

		for i, neighbor in enumerate(nx.all_neighbors(graph, node)):
			#this line of code shouldn't ever hit, keeping it here for sanity sake
			if config.board_token not in neighbor: 
				assert(False)
				continue #only count boards
			# boardNeighbors[node].append(graph.degree(pin_neighbors))
			currBoardList.append(graph.degree(neighbor))

			for j, pin_neighbors in enumerate(nx.all_neighbors(graph, neighbor)):
				#this condition should also never trigger
				if config.pin_token not in pin_neighbors: 
					assert(False)
					continue #only count second degree pins
				currPinList.append(graph.degree(pin_neighbors))
				# pinNeighbors[node].append(graph.degree(pin_neighbors))

		currPinList = np.array(currPinList)
		currBoardList = np.array(currBoardList)
		pinOut[node] = [graph.degree(node),
						currPinList.mean(), currPinList.std(),\
		 				currBoardList.mean(), currBoardList.std()]

		# if k == 10:
			# break

	return pinOut

#input a default dict that we append the node clustering coefficient to the nodeDictionary
def getClusterCoef(graph, nodeDict):
	assert(nx.is_frozen(graph))
	#we can do this because the graph is static 
	neighborDict = {} #cache of all such boards 

	for k, node in enumerate(list(graph.nodes())):
		if config.pin_token not in node: continue

		boardList = set()
		k_i = 0.

		for i, neighbor in enumerate(nx.all_neighbors(graph, node)):
			#this condition sohuldn't ever trigger
			if config.board_token not in neighbor: 
				assert(False)
				continue
			boardList.add(neighbor)
			k_i += graph.degree(neighbor)

		if k_i == 1 or k_i == 0:
			nodeDict[node].append(0.)
			continue

		e_i = 0. #computing e_i here

		neighborList = list(nx.all_neighbors(graph, node))

		# for i, neighbor_b1 in enumerate(nx.all_neighbors(graph, node)):
			# for j, neighbor_b2 in enumerate(nx.all_neighbors(graph, node)):
				# if neighbor_b1 == neighbor_b2: continue
		for i in range(len(neighborList)):
			neighbor_b1 = neighborList[i]
			if neighbor_b1 in neighborDict:
				b1_neighbors = neighborDict[neighbor_b1]
			else:
				b1_neighbors = set(nx.all_neighbors(graph, neighbor_b1))
				neighborDict[neighbor_b1] = b1_neighbors 

			for j in range(len(neighborList[i+1:])):
				neighbor_b2 = neighborList[j]
				if neighbor_b2 in neighborDict:
					b2_neighbors = neighborDict[neighbor_b2]
				else:
					b2_neighbors = set(nx.all_neighbors(graph, neighbor_b2))
					neighborDict[neighbor_b2] = b2_neighbors

				#this code is SOOO slow
				# e_i += len(set(list(nx.all_neighbors(graph, neighbor_b1)) + list(nx.all_neighbors(graph, neighbor_b2))))-1


				union = b1_neighbors.union(b2_neighbors)

				# if len(union) < 1: 
					# assert(len(union)>0)

				e_i += len(union)-1
		# print "e_i is: ", e_i

			# for j, pin_neighbors in enumerate(nx.all_neighbors(graph, neighbor)):
				#condition shouldn't trigger
				# if config.pin_token not in pin_neighbors:
					# assert(False)
					# continue

				# for l, board_pin_neighbor in enumerate(nx.all_neighbors(graph, pin_neighbors)):
					# if board_pin_neighbor in boardList:
						# e_i += 1


		clust_coef = e_i / (2. *k_i * (k_i-1))
		# if clust_coef >=1. or clust_coef<=0.:
			# assert(clust_coef <=1. and clust_coef >= 0.)
		nodeDict[node].append(clust_coef)
	return nodeDict


#update the graph with new nodes/edges
#created from boards pins
def addToGraph(graph, timeDict):
	for i, time in enumerate(timeDict):
		if i == 20000:
			break
		for tup in timeDict[time]:
			board_id, pin_id = tup

			pin_id = config.pin_token + pin_id
			board_id = config.board_token + board_id
			
			graph.add_node(board_id)
			graph.add_node(pin_id)

			graph.add_edge(board_id, pin_id)
			# graph.add_edge(pin_id, board_id)

	return graph

def writeFeatures(featureDict, outFile, outPath = config.outPath):
	with open(outPath + outFile, "wb") as f:
		pickle.dump(featureDict, f)

def createTimeAnalysis():
	# boardDict = loadData("boardDict.pkl")
	# pin0 = loadData("boardPin0.pkl")

	boardPinGraph = nx.Graph()
	for i in range(config.num_timesteps):
		currTime = time.clock()
		currFile = loadData(config.currFile + str(i) + ".pkl")
		boardPinGraph = nx.Graph(boardPinGraph)
		boardPinGraph = addToGraph(boardPinGraph, currFile)
		boardPinGraph = nx.freeze(boardPinGraph)

		featureMap = getGraphDegree(boardPinGraph)
		featureMap = getClusterCoef(boardPinGraph, featureMap)
		# for j, key in enumerate(featureMap):
			# print key, featureMap[key]
			# if j == 100: break
		writeFeatures(featureMap, "dev Featurized " + str(i) + ".pkl")
		print "At timestep: ", i, len(featureMap), " amount of time it took was: ", (time.clock() - currTime)



	print "number of pins is: ", len(featureMap)



def main():
	createTimeAnalysis()

if __name__ == "__main__":
	main()