from Task.AbstractTask import AbstractTask
import configparser
import random

class GenerateTheInput(AbstractTask):
	def __init__(self):
		configParser = configparser.ConfigParser()
		configParser.read("config.ini")
		self.outputCount = int(configParser[("Task."+type(self).__name__).upper()]['outputCount'])
		self.networkTime = int(configParser[("Task."+type(self).__name__).upper()]['networkTime'])
		self.grn = None
		pass

	# To automatically generate the config file for this class
	def gConfig():
		conf = {
			"outputCount" : 5,
			"showOutput" : False,
			"networkTime" : 10,
		}
		return conf

	# This helps the core to figure out how many inputs and outputs the task needs
	def requirements(self):
		req = {
			"inputs": 1,
			"outputs": self.outputCount,
			"evolution": True,
		}
		return req

	def setGRN(self, grn):
		self.grn = grn
		pass

	def start(self):
		maxScore = float(self.outputCount * 2)
		score = 0.
		self.grn.setInput(0, 1)
		self.grn.regulate(self.networkTime)
		outputSeq = ""
		for i in range(self.outputCount):
			if self.grn.getOutput(i) == 1:
				score += 1
			outputSeq += repr(self.grn.getOutput(i)) 
		# self.grn.reset()
		self.grn.setInput(0, 0)
		self.grn.regulate(self.networkTime)
		for i in range(self.outputCount):
			if self.grn.getOutput(i) == 0:
				score += 1 
			outputSeq += repr(self.grn.getOutput(i)) 
		# print(outputSeq)
		return float(score/maxScore)