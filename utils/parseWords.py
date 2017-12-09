import pickle
import dill
import numpy as np


def loadBoardDict(filename = "../Datasets/parsedData/boardDict.pkl"):
	with open(filename, "rb") as f:
		return pickle.load(f)

def separate_words_and_punctuation(text):
	punctuation_symbols = ['.', ',', '?', '!', '(', ')', '"', '/', '#', '@', '~', ';']
	for symbol in punctuation_symbols:
		text = text.replace(symbol, ' ' + symbol + ' ')
	return text

def parseString():
	pass

#board_id, board_name, board_description, user_id, board_create_time
def parseBoard(board):
	pass



def main():
	boardDict = loadBoardDict()
	print boardDict.values()[:10]

if __name__ == "__main__":
	main()