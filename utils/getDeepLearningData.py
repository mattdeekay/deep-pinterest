import heapq
import networkx as nx
import numpy as np
import collections
import pickle
import dill

class config:
	pinterest_filepath = "/cvgl2/u/bcui/CS 224W/Datasets/pinterest_data/"
	# pinterest_filepath = "../Datasets/pinterest_data/"
	debug = True
	
	num_steps = 50
	currStop = None
	topNodeNum = 1e2

	board_token = 'bbb'
	pin_token = 'ppp'

#pin_create_time, board_id, pin_id
def processPins(filename = config.pinterest_filepath + "pins.tsv", limit = 9e6, debug = config.debug):#limit = 380e6):
	# pinDict = collections.defaultdict(lambda :[])
	timeDict = collections.defaultdict(lambda: [])
	# timeList = []
	with open(filename, "rb") as f:
		for i,  line in enumerate(f):
			if i % 5e5 == 0: print "pins", i
			line = line.strip("\r\n")
			line = line.split("\t")
			# pinDict[line[2]].append(line[:2])
			timeDict[line[0]].append(line[1:])
			# timeList.append(line[0])

			if i == limit and debug:
				print "BROKE"
				break
	return timeDict
	# return pinDict, sorted(timeList)

#board_id, board_name, board_description, user_id, board_create_time. 
def processBoards(filename = config.pinterest_filepath + 'boards.tsv', limit = 1e4, debug = config.debug):
    boardMap = {}
    with open(filename, "rb") as f:
        for i, line in enumerate(f):
            # if i % 1e6 == 0: print i
            line = line.strip("\r\n")
            line = line.split("\t")
            boardMap[line[0]] = line[1:]
            if i == limit and debug: break
    print "Number of boards is: ", len(boardMap)
    return boardMap


def createTimestep(pinTimeDict, boardMap, timeSteps, timeStepNum, dataLoc = "../Datasets/parsedData/"):
	# boardPinList = []
	timeBoardPinList = collections.defaultdict(lambda : [])
	for time in pinTimeDict:
		if time not in timeSteps: continue
		# print pinTimeDict[time]
		# board_id, pin_id = pinTimeDict[time]
		for tup in pinTimeDict[time]:
			timeBoardPinList[time].append(tup)
			# board_id, pin_id = tup
			# boardPinList.append((pin_id, board_id))

	with open(dataLoc + "boardPin" + str(timeStepNum) + ".pkl", "wb") as f:
		pickle.dump(timeBoardPinList, f)

	# with open(dataLoc + "boardPin" + str(timeStepNum) + ".txt", "wb") as f:
		# f.write("pin_id, board_id\n")
		# for tup in boardPinList:
			# pin_id, board_id = tup
			# f.write(str("p" + pin_id) + "," +  str("b" + board_id) + "\n")

def outputUsedBoards(pinTimeDict, boardMap, dataLoc = "../Datasets/parsedData/boardDict.pkl"):
	usedBoardIds = set()
	for time in pinTimeDict:
		for tup in pinTimeDict[time]:
			board_id, pin_id = tup
			if board_id in boardMap:
				usedBoardIds.add(board_id)

	usedDict = {key: boardMap[key] for key in usedBoardIds}

	with open(dataLoc, "wb") as f:
		pickle.dump(usedDict, f)


def parseData():
	pinTimeDict = processPins()
	boardMap = processBoards()

	timeList = sorted(pinTimeDict.keys())
	numTimes = len(pinTimeDict.keys())
	pinsPerTimestep = numTimes/config.num_steps

	print "length of timeList is: ", numTimes
	print "numPerTimestep is: ", pinsPerTimestep

	outputUsedBoards(pinTimeDict, boardMap)

	for i in range(config.num_steps):
		createTimestep(pinTimeDict, boardMap, set(timeList[i * pinsPerTimestep:(i+1) * pinsPerTimestep]), i)


	# print "DOING TIME DOMAIN NOW"

	# createGraph(pinMap, boardMap, float("-inf"), pinLim = 1e10, boardLim = 1e10)

	# for i in reversed(range(1, config.num_steps + 1)):
		# config.currStop = timeList[numTimes/i-1]
		# print "at timestep: ", 	i, "NEW timestep should include: ", numTimes/i
		# createGraph(pinMap, boardMap, config.currStop, pinLim = 1e10, boardLim = 1e10)


def main():
	parseData()

if __name__ == "__main__":
	main()


'''
def createGraph(pinMap, boardMap, stopTime, pinLim = None, boardLim = None, debug = config.debug):
	assert (pinLim is not None and boardLim is not None)
	graph = nx.Graph()

	board_idMap = {} #maps 
	for i, key in enumerate(boardMap):
		if i == boardLim: break
		board_idMap[key] = i
		graph.add_node(config.board_token + key)

	pinCounter = 0
	for pinId in pinMap:
		for pinIndex, pin in enumerate(pinMap[pinId]):
			createTime, board_id = pin

			# if createTime > stopTime: continue
			
			# if board_id not in board_idMap: continue

			if pinIndex == 0:
				graph.add_node(config.pin_token + pinId)
			graph.add_edge(config.board_token + board_id, config.pin_token +  pinId)
			graph.add_edge(config.pin_token + pinId, config.board_token + board_id)

			pinCounter += 1

	if debug:
		print ("NUMBER OF NODES IS: ", graph.number_of_nodes())
		print ("NUMBER OF EDGES IS: ", graph.number_of_edges())
		degreeMap = getGraphDegree(graph)
		saveHighestNodes(graph)
		for i, key in enumerate(degreeMap):
			if i == 20: break
			print key, degreeMap[key]
		print degreeMap

#prints and outputs the degree within the graph 
def getGraphDegree(graph):
	degreeMap = collections.defaultdict(int)
	notInCounter = 0
	for node in list(graph.nodes()):
		if config.board_token not in node:
			notInCounter += 1
		 	continue

		degreeMap[graph.degree(node)] += 1
	print "WORKED ON ", notInCounter
	return degreeMap

def saveHighestNodes(graph, nodeNum = config.topNodeNum):
	heap = []
	for node in list(graph.nodes()):
		if config.board_token not in node: continue

		currTuple = (graph.degree(node), node)
		heapq.heappush(heap, currTuple)
	print len(heap)
	# print heap[-50:]
'''