import networkx as nx
import numpy as np
import collections

class config:
	pinterest_filepath = "/cvgl2/u/bcui/Datasets/pinterest_data/"
	debug = False
	
	num_steps = 5
	currStop = None

	board_token = 'b'
	pin_token = 'p'



#pin_create_time, board_id, pin_id
def processPins(filename = config.pinterest_filepath + "pins.tsv", limit = 380e6, debug = config.debug):#limit = 380e6):
	pinDict = collections.defaultdict(lambda :[])
	timeList = []
	with open(filename, "rb") as f:
		for i,  line in enumerate(f):
			line = line.strip("\r\n")
			line = line.split("\t")
			pinDict[line[2]].append(line[:2])
			timeList.append(line[0])

			if i == limit and debug: break
			
	return pinDict, sorted(timeList)

#board_id, board_name, board_description, user_id, board_create_time. 
def processBoards(filename = config.pinterest_filepath + 'boards.tsv', limit = float("inf"), debug = config.debug):
    boardMap = {}
    with open(filename, "rb") as f:
        for i, line in enumerate(f):
            # if i % 1e6 == 0: print i
            line = line.strip("\r\n")
            line = line.split("\t")
            boardMap[line[0]] = line[1:]
            if i == limit and debug: break
    return boardMap

#gets the degree of nodes in a graph
def getGraphDegree(graph):
	degreeMap = collections.defaultdict(int)
	for node in list(graph.nodes):
		if 'b' not in node: continue

		degreeMap[graph.degree(node)] += 1
	return degreeMap


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

		# if pinCounter == pinLim: break
		for pinIndex, pin in enumerate(pinMap[pinId]):
			createTime, board_id = pin

			if createTime > stopTime: continue
			
			if board_id not in board_idMap: continue

			if pinIndex == 0:
				graph.add_node(config.pin_token + pinId)
			graph.add_edge(config.board_token + board_id, config.pin_token +  pinId)
			graph.add_edge(config.pin_token + pinId, config.board_token + board_id)

			pinCounter += 1

	if debug:
		print ("NUMBER OF NODES IS: ", graph.number_of_nodes())
		print ("NUMBER OF EDGES IS: ", graph.number_of_edges())
		degreeMap = getGraphDegree(graph)
		for i, key in enumerate(degreeMap):
			if i == 20: break
			print key, degreeMap[key]
		print degreeMap


def runTimeDomain():
	pinMap, timeList = processPins()
	boardMap = processBoards()

	numTimes = len(timeList)

	print "DOING TIME DOMAIN NOW"

	for i in reversed(range(1, config.num_steps + 1)):
		config.currStop = timeList[numTimes/i-1]
		createGraph(pinMap, boardMap, config.currStop, pinLim = 1e10, boardLim = 1e10)


def main():
	runTimeDomain()

if __name__ == "__main__":
	main()