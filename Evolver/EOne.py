from Evolver.AbstractEvolver import AbstractEvolver
import network as N
import configparser
import copy
import random

# Basic Evolver that only does mutation with a constant chance and uses Tournament Selection
class EOne(AbstractEvolver):

	def __init__(self, genomeClass, taskClass, runs, elitism):
		configParser = configparser.ConfigParser()
		configParser.read("config.ini")
		self.popSize = int(configParser[("Evolver."+type(self).__name__).upper()]['populationSize'])
		self.mutationRate = float(configParser[("Evolver."+type(self).__name__).upper()]['mutationRate'])
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
		print("ARNF: Creating a population of ARNs with size: {}".format(self.popSize))
		for i in range(self.popSize):
			individual = self.genomeClass()
			individual.initialize(self.taskClass().requirements())
			self.pop.append(individual)
		pass

	def evolve(self):
		print("ARNF: Starting the evolution for {} rounds.".format(self.runs))
		for generation in range(self.runs):
			maxFitness = [-1, None, None]
			totFitness = 0.
			# Calculate the fitness and find the maximum
			for index, individual in enumerate(self.pop):
				individual.reinitialize(self.taskClass().requirements())
				task = self.taskClass()
				grn = N.Network(individual.getGenes())
				grn.build()
				task.setGRN(grn)
				fitness = task.start()
				totFitness += fitness
				individual.setFitness(fitness)
				if maxFitness[1] == None or maxFitness[1] < fitness:
					# print("best changed old fitness: {} new fitness {}".format(maxFitness[1], fitness))
					maxFitness[0] = index
					maxFitness[1] = fitness
					maxFitness[2] = len(individual.genes)

			if self.showOutput:
				print("Generation: {} Average Fitness: {} Best Fitness: {} Gene Count: {}".format(generation, round(totFitness/len(self.pop),2), round(maxFitness[1],2), maxFitness[2]))
			
			# Elitism
			if self.elitism:
				elite = copy.deepcopy(self.pop[maxFitness[0]])
				if self.popSize == len(self.pop):
					self.pop.append(elite)
				else:
					self.pop[len(self.pop)-1] = elite
			# Mutate
			# ToDo:: This mutation algorithm is the worst ever computationaly. Many faster algorithms are there. 
			for i in range(len(self.pop)):
				if self.elitism and i == len(self.pop)-1:
					continue
				self.mutate(i)
		pass

	def mutate(self, i):
		for j, base in enumerate(self.pop[i].DNA):
			if random.random() < self.mutationRate:
				if base == 0:
					self.pop[i].DNA[j] = 1
				else:
					self.pop[i].DNA[j] = 0
		pass

	@staticmethod
	def gConfig():
		conf = {
			"mutationRate": 0.01,
			"populationSize": 100,
			"showOutput": True,
			"logEvolution": False
		}
		return conf

	

