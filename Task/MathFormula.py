from Task.AbstractTask import AbstractTask
import Utility.Config as Config
import math

class MathFormula(AbstractTask):

	def __init__(self):
		self.GRN = None

	# This is the task's main function. 
	def start(self):
		averageerror = 0
		# print("New Gene\n")
		for i in range(10):
			self.GRN.setInput(0, i)
			self.GRN.regulate(100)
			output = self.GRN.getOutput(0)
			averageerror += abs(output - i*i)
			# print("{} ^ 2 = {}".format(i,output))
		return averageerror/10

	def setGRN(self, grn):
		self.GRN = grn

	def requirements(self):
		# first element is input count and the second element is the output count
		req = {
			"inputs": 1,
			"outputs": 1,
			"evolution": True
		}
		return req

	def gConfig():
		conf = {
		}
		return conf
