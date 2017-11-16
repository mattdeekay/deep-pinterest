import networkx as nx
import numpy as np

class config:
	pinterest_filepath = "/cvgl2/u/bcui/Datasets/pinterest_data"


#pin_create_time, board_id, pin_id
def processPins(filename = config.pinterest_filepath + "pins.tsv", limit = 1e5):#limit = 380e6):
	pinDict = collections.defaultdict(lambda :[])
	with open(filename, "rb") as f:
		for i,  line in enumerate(f):
			if i % 5e6 == 0: print i    
			line = line.strip("\r\n")
			line = line.split("\t")
			pinDict[line[2]].append(line[:2])

			if i == limit: return pinDict
			
	return pinDict

#board_id, board_name, board_description, user_id, board_create_time. 
def processBoards(filename = config.pinterest_filepath + 'boards.tsv', limit = 1e5):
    boardMap = {}
    with open(filename, "rb") as f:
        for i, line in enumerate(f):
            if i % 1e6 == 0: print i
            line = line.strip("\r\n")
            line = line.split("\t")
            boardMap[line[0]] = line[1:]
    return boardMap

def createGraph(pinMap, boardMap, pinLim = None, boardLim = None, debug = False):
	assert (pinLim is not None and boardLim is not None)
	graph = nx.Graph()

	board_idMap = {} #maps 
	nodeCounter = 0
	for i, key in enumerate(boardMap):
		if i == boardLim: break
		board_idMap[key] = i
		graph.add_node(i)
		nodeCounter += 1

	pinCounter = 0
	for key in pinMap:
		if pinCounter == pinLim: break
		for pin in pinMap[key]:
			createTime, board_id = pin
			
			if board_id not in board_idMap: continue


			graph.add_node(nodeCounter)
			graph.add_edge(nodeCounter, int(board_idMap[board_id]))
			graph.add_edge(int(board_idMap[board_id]), nodeCounter)

			nodeCounter += 1
			pinCounter += 1

	if debug:
		print ("NUMBER OF NODES IS: ", len([node for node in Graph.Nodes()]))
		print ("NUMBER OF EDGES IS: ", len([edge for edge in Graph.Edges()]))


def runTimeDomain():
	pinMap = processPins()
	boardMap = processBoards()
	createGraph()


def main():
	runTimeDomain()

if __name__ == "__main__":
	main()