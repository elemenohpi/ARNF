from Task.AbstractTask import AbstractTask
import configparser

class ClosedWorld(AbstractTask):

	def __init__(self):
		configParser = configparser.ConfigParser()
		configParser.read("config.ini")
		self.GRN = None
		self.regulations = int(configParser[("Task."+type(self).__name__).upper()]['regulations'])
		if configParser[("Task."+type(self).__name__).upper()]['showOutput'] == "False":
			self.showOutput = False
		else:
			self.showOutput = True
		if configParser[("Task."+type(self).__name__).upper()]['logRegulations'] == "False":
			self.logRegulations = False
		else:
			self.logRegulations = True

	# This is the task's main function. 
	def start(self):
		print("ARNF: Starting the task...")
		self.GRN.regulate(self.regulations, self.showOutput, self.logRegulations)
		pass

	def setGRN(self, grn):
		self.GRN = grn

	def requirements(self):
		# first element is input count and the second element is the output count
		req = {
			"inputs": 0,
			"outputs": 0,
			"evolution": False
		}
		return req

	def gConfig():
		conf = {
			"regulations": 1000,
			"showOutput": True,
			"logRegulations": False
		}
		return conf
