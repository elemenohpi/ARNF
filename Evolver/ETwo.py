from Evolver.AbstractEvolver import AbstractEvolver
import configparser
import copy
import random
import Utility.Config as Config

# A more advanced evolver. Starts with simple networks and adds genes to them if there is not much improvement. Faster mutation operator.
class ETwo(AbstractEvolver):

	def __init__(self, network, genomeClass, taskClass, runs, elitism):
		configParser = configparser.ConfigParser()
		configParser.read("config.ini")
		self.popSize = int(configParser[("Evolver."+type(self).__name__).upper()]['populationSize'])
		self.mutationPortion = float(configParser[("Evolver."+type(self).__name__).upper()]['mutationPortion'])
		self.complexificationRate = float(configParser[("Evolver."+type(self).__name__).upper()]['complexificationRate'])
		self.showOutput = configParser[("Evolver."+type(self).__name__).upper()]['showOutput']
		if self.showOutput == "True":
			self.showOutput = True
		else:
			self. showOutput = False
		self.pop = [] # population of whole genomes
		self.genomeClass = genomeClass 
		self.taskClass = taskClass
		self.runs = runs
		self.elitism = elitism
		self.grn = network
		self.mode = Config.read(self, "Evolver", "mode")
		# self.saveBestModel = Config.read(self, "Evolver", "saveBestModel")
		self.fitnessLog = [] # We track the average fitness of the population for a few generations to know when we should complexify the network
		print("ARNF: Creating a population of ARNs with size: {}".format(self.popSize))
		for i in range(self.popSize):
			individual = self.genomeClass()
			individual.initialize(self.taskClass().requirements())
			self.pop.append(individual)

	def evolve(self):
		print("ARNF: Starting the evolution for {} rounds.".format(self.runs))
		for generation in range(self.runs):
			complexification = False
			maxFitness = [-1, None, None]
			totFitness = 0.
			totNodes = 0
			# Calculate the fitness and find the maximum
			for index, individual in enumerate(self.pop):
				individual.reinitialize(self.taskClass().requirements())
				task = self.taskClass()
				self.grn.setGenes(individual.getGenes())
				self.grn.build()
				task.setGRN(self.grn)
				fitness = task.start()
				totFitness += fitness
				individual.setFitness(fitness)
				if self.mode == "maximize":
					if maxFitness[1] == None or maxFitness[1] < fitness:
						# print("best changed old fitness: {} new fitness {}".format(maxFitness[1], fitness))
						maxFitness[0] = index
						maxFitness[1] = fitness
						maxFitness[2] = len(individual.genes)
				elif self.mode == "minimize":
					if maxFitness[1] == None or maxFitness[1] > fitness:
						# print("best changed old fitness: {} new fitness {}".format(maxFitness[1], fitness))
						maxFitness[0] = index
						maxFitness[1] = fitness
						maxFitness[2] = len(individual.genes)
				totNodes += len(individual.genes)
			if generation % 10 == 0:
				self.fitnessLog.append(maxFitness[1])
				if len(self.fitnessLog) > 3:
					self.fitnessLog.pop(0)
			averageFitness = totFitness/len(self.pop)
			averageNodes = totNodes / len(self.pop)
			if self.showOutput:
				print("Generation: {} Average Fitness: {} Average Gene Count: {} Best Fitness: {} Gene Count: {} ".format(generation, round(averageFitness,4), round(averageNodes, 4), round(maxFitness[1],4), maxFitness[2]))
		
			# Elitism
			if self.elitism:
				elite = copy.deepcopy(self.pop[maxFitness[0]])
				if self.popSize == len(self.pop):
					self.pop.append(elite)
				elif len(self.pop) == self.popSize + 1:
					self.pop[len(self.pop)-1] = elite
				else:
					print("ERROR: Illegal population size. Exiting!")
					exit(1)

			# Check the complexification condition
			if len(self.fitnessLog) == 3:
				if self.fitnessLog[0] == self.fitnessLog[2]:
					complexification = True

			# # if generation > 394:
			# for shomar, ind in enumerate(self.pop):
			# 	print("{} - DNA size: {}".format(shomar, (len(ind.DNA))/224))
			# exit()

			# Mutate
			# ToDo:: This mutation algorithm is the worst ever computationaly. Many faster algorithms are there. 
			for i in range(len(self.pop)):
				if self.elitism and i == len(self.pop)-1:
					continue
				if complexification:
					self.complexify(i)
				self.mutate(i)
		pass

	def complexify(self, i):
		if random.random() < self.complexificationRate:
			self.pop[i].addGene()
		pass

	def mutate(self, i):
		mutationCount = random.randint(0, int(len(self.pop[i].getDNA()) * self.mutationPortion))
		for j in range(mutationCount):
			index = random.randint(0, len(self.pop[i].getDNA())-1)
			base = self.pop[i].getDNA()[index]
			if base == 0:
				self.pop[i].getDNA()[index] = 1
			else:
				self.pop[i].getDNA()[index] = 0
		pass

	@staticmethod
	def gConfig():
		conf = {
			"mutationPortion": 0.01, # Differently defined
			"complexificationRate": 0.1,
			"populationSize": 100,
			"showOutput": True,
			"logEvolution": False,
			"mode": "minimize"
		}
		return conf

	

