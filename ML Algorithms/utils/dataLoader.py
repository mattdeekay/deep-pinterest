import numpy as np
import dill
import pickle

def loadData(filename = "dev Featurized 0.pkl", filepath = "../../Datasets/Deep Learning Parsed/Train/"):
	with open(filepath + filename, "rb") as f:
		currFile = pickle.load(f)
	# print currFile
	return currFile

def main():
	loadData()

if __name__ == "__main__":
	main()