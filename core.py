import configparser
import numpy as np
import network as N

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
		if (self.elitism).upper() == "TRUE":
			self.elitism = True
		else:
			self.elitism = False

		# List of the instances we need to run the core
		self.taskObj = None
		self.genomeObj = None
		self.evolverObj = None
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
		
	def run(self):
		# ToDo:: Make the requirements method static and move the following two lines to the if statement
		self.taskObj = self.taskClass()
		self.taskRequirements = self.taskObj.requirements()
		if not self.taskRequirements["evolution"]:
			self.genomeObj = self.genomeClass()
			self.genomeObj.initialize(self.taskRequirements)
			self.genes = self.genomeObj.getGenes()
			grn = N.Network(self.genes)
			grn.build()

			self.taskObj.setGRN(grn)
			self.taskObj.start()
		else:
			# Task requires evolution of the artificial gene regulatory networks. So, we need to call the optimizer/evolver here
			self.evolverObj = self.evolverClass(self.genomeClass, self.taskClass, self.runs, self.elitism)
			self.evolverObj.evolve()

