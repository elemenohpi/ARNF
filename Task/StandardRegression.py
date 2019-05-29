from Task.AbstractTask import AbstractTask
import random
import Utility.Config as Config

class StandardRegression(AbstractTask):
	def __init__(self):
		# self.file = Config.read(self, "Task", "file")
		# self.networkTime = Config.read(self, "Task", "networkTime")
		# self.showOutput = Config.readBool(self, "Task", "showOutput")
		# self.header = Config.readBool(self, "Task", "header")
		self.grn = None

	# To automatically generate the config file for this class
	def gConfig():
		conf = {
			# "file" : "./Input/StandardRegression/data.csv",
			# "showOutput" : False,
			# "networkTime" : 10,
			# "header" : False
		}
		return conf

	# This helps the core to figure out how many inputs and outputs the task needs
	def requirements(self):
		inputCount = 2
		outputCount = 1
		req = {
			"inputs": inputCount,
			"outputs": outputCount,
			"evolution": True,
		}
		return req

	def setGRN(self, grn):
		self.grn = grn
		pass

	def start(self):
		table = []
		table.append([2, 2, 4])
		table.append([1, 2, 3])
		table.append([3, 4, 7])
		table.append([1, 4, 5])
		table.append([7, 4, 11])
		table.append([1, 1, 2])
		score = 0
		string = ""
		for row in table:
			self.grn.reset()
			self.grn.setInput(0, row[0])
			self.grn.setInput(1, row[1])
			self.grn.regulate(100)
			if self.grn.getOutput(0) - row[2] == 0:
				score += 1			
			string += "{}+{}={} ".format(row[0], row[1], self.grn.getOutput(0))
		print(string)
		return score