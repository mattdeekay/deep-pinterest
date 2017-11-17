import collections

def parseDefaultdict():
	with open("test.txt", "rb") as f:
		currDict = collections.defaultdict(int)
		for line in f:
			s = line.find("{")
			line = line[s+1:-3]
			line = line.split(",")
			for entry in line:
				entry = entry.split(":")
				currDict[int(entry[0])] = int(entry[1])
				
			print currDict

