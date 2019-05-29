from Genome.AbstractGenome import AbstractGenome
import random, configparser
import gene as G

class Discrete(AbstractGenome):

	def __init__(self):
		config = configparser.ConfigParser()
		config.read("config.ini")
		self.protSize = int(config[("Genome."+type(self).__name__).upper()]['protSize'])
		self.inhSize = int(config[("Genome."+type(self).__name__).upper()]['inhSize'])
		self.enhSize = int(config[("Genome."+type(self).__name__).upper()]['enhSize'])
		self.protSeqMult = int(config[("Genome."+type(self).__name__).upper()]['protSeqMult'])
		self.internalGenesCount = int(config[("Genome."+type(self).__name__).upper()]['internalGenesCount'])
		self.DNA = []
		self.genes = []
		self.fitness = 0
		self.geneLength = self.inhSize + self.enhSize + (self.protSize * self.protSeqMult)

	# This is to automatically generate the config file for this class
	@staticmethod
	def gConfig():
		conf = {
			"internalGenesCount" : 5,
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
		DNAlength = self.internalGenesCount * self.geneLength
		# enhancer inhibitor prot seq => DNA
		self.DNA = [random.randint(0,1) for b in range(0,DNAlength)]
		self.findGenes()

		# for all the inputs add an input gene. Inputs regulate but don't get regulated. We want all the inputs to have the same impact and for the concentrations to play the main role. We don't care about the promoter, enhancer or inhibitor regions. So, the only thing we want is the same protein sequence for the inputs which means that they effect eachother as low as possible and effect the other genes equally as much. 
		
		configParser = configparser.ConfigParser()
		configParser.read("./inputs.ini")
		counter = 0
		for i in range(inputCount):
			enhancer_tmp = configParser['INP'][repr(counter)]
			inhibitor_tmp = configParser['INP'][repr(counter+1)]
			protein_tmp = configParser['INP'][repr(counter+2)]
			enhancer = [int(a) for a in enhancer_tmp]
			inhibitor = [int(a) for a in inhibitor_tmp]
			protein = [int(a) for a in protein_tmp]
			counter += 3
			self.genes.append(G.Gene("11111111", enhancer, inhibitor, protein, "I"))
		# for all the outputs add an output gene. Outputs don't regulate but get regulated. We want all the genes to have different impacts on the outputs. So, we want them to be as different as possible. 
		for i in range(outputCount):
			enhancer_tmp = configParser['INP'][repr(counter)]
			inhibitor_tmp = configParser['INP'][repr(counter+1)]
			protein_tmp = configParser['INP'][repr(counter+2)]
			enhancer = [int(a) for a in enhancer_tmp]
			inhibitor = [int(a) for a in inhibitor_tmp]
			protein = [int(a) for a in protein_tmp]
			counter += 3
			self.genes.append(G.Gene("00000000", enhancer, inhibitor, protein, "O"))

		self.resetConcentrations()
		# for gene in self.genes:
		# 	gene.print()
		pass

	def addGene(self):
		self.DNA += [random.randint(0,1) for b in range(0,self.geneLength)]
		self.internalGenesCount += 1
		self.findGenes()
		pass


	def reinitialize(self, requirements):
		self.findGenes()
		# for all the inputs add an input gene. Inputs regulate but don't get regulated. We want all the inputs to have the same impact and for the concentrations to play the main role. We don't care about the promoter, enhancer or inhibitor regions. So, the only thing we want is the same protein sequence for the inputs which means that they effect eachother as low as possible and effect the other genes equally as much. 

		self.resetConcentrations()

	def resetConcentrations(self):
		for gene in self.genes:
			gene.concentration = 1 / len(self.genes)

	# Finds genes in a DNA. Format: [Promoter -> Enhancer -> Inhibitor -> n * protSize]
	def findGenes(self):
		tmp_genes = []
		for index, gene in enumerate(self.genes):
			if gene.type != "TF":
				tmp_genes.append(gene)
		self.genes = tmp_genes

		for i in range(self.internalGenesCount):
			index = i * self.geneLength
			enhancer = self.DNA[index : index + self.enhSize] 
			index += self.enhSize
			inhibitor = self.DNA[index : index + self.inhSize] 
			index += self.inhSize
			protein = []
			for j in range(self.protSize):
				tempArray = []
				for k in range(self.protSeqMult):
					try:
						tempArray.append(self.DNA[index + k * self.protSize])
					except:
						print("DNA size: {} gene length: {} protsize: {} index: {} k: {}".format(len(self.DNA), self.geneLength, self.protSize, index, k))
						exit()
				zeroes = 0
				for l in tempArray:
					if l == 0:
						zeroes+=1
				if zeroes < len(tempArray) / 2:
					protein.append(1)
				else:
					protein.append(0)
			# print ("enhancer: {} inhibitor: {} protein: {}".format(enhancer, inhibitor, protein))
			self.genes.append(G.Gene("10101010", enhancer, inhibitor, protein, "TF"))

	# Returns the genes
	def getGenes(self):
		return self.genes

	def setFitness(self, fitness):
		self.Fitness = fitness 

	def getFitness(self):
		return self.fitness
		
	def getDNA(self):
		return self.DNA

