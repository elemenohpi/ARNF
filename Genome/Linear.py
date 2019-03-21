from Genome.AbstractGenome import AbstractGenome
import random, configparser
import gene as G

class Linear(AbstractGenome):

	def __init__(self):
		config = configparser.ConfigParser()
		config.read("config.ini")
		self.length = int(config[("Genome."+type(self).__name__).upper()]['length'])
		self.promoter = config[("Genome."+type(self).__name__).upper()]['promoter']
		self.protSize = int(config[("Genome."+type(self).__name__).upper()]['protSize'])
		self.inhSize = int(config[("Genome."+type(self).__name__).upper()]['inhSize'])
		self.enhSize = int(config[("Genome."+type(self).__name__).upper()]['enhSize'])
		self.protSeqMult = int(config[("Genome."+type(self).__name__).upper()]['protSeqMult'])
		self.DNA = []
		self.genes = []
		self.fitness = 0

	# This is to automatically generate the config file for this class
	@staticmethod
	def gConfig():
		conf = {
			"length" : 5000,
			"promoter" : "01010101", 
			"enhSize" : 32,
			"inhSize" : 32,
			"protSize" : 32,
			"protSeqMult" : 5
		}
		return conf
	
	# Initializes the genome and finds the genes
	def initialize(self, requirements): 
		inputCount = requirements['inputs']
		outputCount = requirements['outputs']
		self.DNA = [random.randint(0,1) for b in range(1,self.length+1)]
		self.findGenes()
		# for all the inputs add an input gene. Inputs regulate but don't get regulated. We want all the inputs to have the same impact and for the concentrations to play the main role. We don't care about the promoter, enhancer or inhibitor regions. So, the only thing we want is the same protein sequence for the inputs which means that they effect eachother as low as possible and effect the other genes equally as much. 
		
		for i in range(inputCount):
			self.genes.append(G.Gene("11111111", [0 for b in range(self.enhSize)], [0 for b in range(self.inhSize)], [0 for b in range(self.protSize)], "I"))
		# for all the outputs add an output gene. Outputs don't regulate but get regulated. We want all the genes to have different impacts on the outputs. So, we want them to be as different as possible. 
		for i in range(outputCount):
			pattern = []
			comp_pattern = []
			for j in range(self.enhSize):
				if j >= i * (self.protSize/outputCount) and j < (i+1) * (self.protSize/outputCount):
					pattern.append(1)
					comp_pattern.append(0)
				else:
					pattern.append(0)
					comp_pattern.append(1)
			self.genes.append(G.Gene("00000000", pattern, comp_pattern, [0 for b in range(self.protSize)], "O"))
		for gene in self.genes:
			gene.concentration = 1 / len(self.genes)
		# for gene in self.genes:
		# 	gene.print()
		pass

	def reinitialize(self, requirements):
		inputCount = requirements['inputs']
		outputCount = requirements['outputs']
		self.genes = []
		self.findGenes()
		# for all the inputs add an input gene. Inputs regulate but don't get regulated. We want all the inputs to have the same impact and for the concentrations to play the main role. We don't care about the promoter, enhancer or inhibitor regions. So, the only thing we want is the same protein sequence for the inputs which means that they effect eachother as low as possible and effect the other genes equally as much. 
		
		for i in range(inputCount):
			self.genes.append(G.Gene("11111111", [0 for b in range(self.enhSize)], [0 for b in range(self.inhSize)], [0 for b in range(self.protSize)], "I"))
		# for all the outputs add an output gene. Outputs don't regulate but get regulated. We want all the genes to have different impacts on the outputs. So, we want them to be as different as possible. 
		for i in range(outputCount):
			pattern = []
			comp_pattern = []
			for j in range(self.enhSize):
				if j >= i * (self.protSize/outputCount) and j < (i+1) * (self.protSize/outputCount):
					pattern.append(1)
					comp_pattern.append(0)
				else:
					pattern.append(0)
					comp_pattern.append(1)
			self.genes.append(G.Gene("00000000", pattern, comp_pattern, [0 for b in range(self.protSize)], "O"))
		for gene in self.genes:
			gene.concentration = 1 / len(self.genes)


	# Finds genes in a DNA. Format: [Promoter -> Enhancer -> Inhibitor -> n * protSize]
	def findGenes(self):
		for i in range(len(self.DNA)-len(self.promoter)-self.protSize*self.protSeqMult-self.enhSize-self.inhSize-1): #here
			if ''.join(str(e) for e in self.DNA[i:i+len(self.promoter)]) == self.promoter:
				enhancer = self.DNA[i+len(self.promoter)+1:i+len(self.promoter)+1+self.enhSize]
				inhibitor = self.DNA[i+len(self.promoter)+1+self.enhSize:i+len(self.promoter)+1+self.enhSize+self.inhSize]
				i += len(self.promoter) + self.enhSize + self.inhSize
				# here. gotta use the majority rule to come up with the protein sequence
				protein = []
				for j in range(self.protSize):
					ones = 0
					zeroes = 0
					for k in range(self.protSeqMult):
						if self.DNA[i + j + k * self.protSize] == 0: 
							ones += 1
						else: 
							zeroes += 1 
					if ones >= zeroes: # favors 1s over 0s
						protein.append(1)
					else: 
						protein.append(0)	
				# print ("enhancer: {} inhibitor: {} protein: {}".format(enhancer, inhibitor, protein))
				i += (self.protSeqMult * self.protSize)
				self.genes.append(G.Gene(self.promoter, enhancer, inhibitor, protein, "TF"))

	# Returns the genes
	def getGenes(self):
		return self.genes

	def setFitness(self, fitness):
		self.Fitness = fitness 

	def getFitness(self):
		return self.fitness
		


