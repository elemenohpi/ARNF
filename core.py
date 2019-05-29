import configparser
import numpy as np

# This class ties everything together
class Core:

	def __init__(self):
		configParser = configparser.ConfigParser()
		configParser.read("config.ini")
		self.runs = int(configParser[(type(self).__name__).upper()]['runs'])
		self.genomeType = configParser[(type(self).__name__).upper()]['genome']
		self.taskName = configParser[(type(self).__name__).upper()]['task']
		self.evolverType = configParser[(type(self).__name__).upper()]['evolver']
		self.elitism = configParser[(type(self).__name__).upper()]['elitism']
		self.networkType = configParser[(type(self).__name__).upper()]['network']
		if (self.elitism).upper() == "TRUE":
			self.elitism = True
		else:
			self.elitism = False

		# List of the instances we need to run the core
		self.taskObj = None
		self.genomeObj = None
		self.evolverObj = None
		self.networkObj = None
		self.genes = []

		print("ARNF: Running the system for the {} task".format(self.taskName))
		# ToDo:: Task not found exit condition
		module = __import__("Task." + self.taskName)
		self.taskClass = getattr(getattr(module, self.taskName), self.taskName)

		# Load the Genome model and initialize it. 
		module = __import__("Genome." + self.genomeType)
		self.genomeClass = getattr(getattr(module, self.genomeType), self.genomeType)

		# Load the evolver object
		module = __import__("Evolver." + self.evolverType)
		self.evolverClass = getattr(getattr(module, self.evolverType), self.evolverType)

		module = __import__("Network." + self.networkType)
		self.networkClass = getattr(getattr(module, self.networkType), self.networkType)
		
	def run(self):
		# ToDo:: Make the requirements method static and move the following two lines to the if statement
		self.taskObj = self.taskClass()
		self.taskRequirements = self.taskObj.requirements()
		self.genomeObj = self.genomeClass()
		self.genomeObj.initialize(self.taskRequirements)
		self.genes = self.genomeObj.getGenes()
		self.networkObj = self.networkClass(self.genes)
		self.networkObj.build()
		if not self.taskRequirements["evolution"]:
			self.taskObj.setGRN(self.networkObj)
			self.taskObj.start()
		else:
			# Task requires evolution of the artificial gene regulatory networks. So, we need to call the optimizer/evolver here
			self.evolverObj = self.evolverClass(self.networkObj, self.genomeClass, self.taskClass, self.runs, self.elitism)
			self.evolverObj.evolve()

