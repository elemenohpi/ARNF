from Network.AbstractNetwork import AbstractNetwork
import numpy as np
import math
import Utility.Logger as L
import Utility.Config as Config

# ARN-R: Artificial Regulatory Network for Regression

class ARNR(AbstractNetwork):
	def __init__(self):
		self.beta = Config.readFloat(self, "Network", "beta")
		self.delta = Config.readFloat(self, "Network", "delta")
		self.minIn = Config.readFloat(self, "Network", "minIn")
		self.minOut = Config.readFloat(self, "Network", "minOut")
		self.maxIn = Config.readFloat(self, "Network", "maxIn")
		self.maxOut = Config.readFloat(self, "Network", "maxOut")
		self.intMode = Config.read(self, "Network", "intMode")
		self.genes = None

	def __init__(self, genes):
		self.beta = Config.readFloat(self, "Network", "beta")
		self.delta = Config.readFloat(self, "Network", "delta")
		self.minIn = Config.readFloat(self, "Network", "minIn")
		self.minOut = Config.readFloat(self, "Network", "minOut")
		self.maxIn = Config.readFloat(self, "Network", "maxIn")
		self.maxOut = Config.readFloat(self, "Network", "maxOut")
		self.intMode = Config.read(self, "Network", "intMode")
		self.genes = genes
	
	def build(self):
		# find u_max and u_i
		# print("ARNF: Building the Gene Regulatory Network...")
		for g_i in self.genes:
			g_i.matchingDegreesE = np.zeros(len(self.genes))
			g_i.matchingDegreesI = np.zeros(len(self.genes))
			for j, g_j in enumerate(self.genes):
				g_i.matchingDegreesE[j] = self.findMatchingDegree(g_i.enhancer, g_j.protein)
				g_i.matchingDegreesI[j] = self.findMatchingDegree(g_i.inhibitor, g_j.protein)
			g_i.maximumMatchI = max(g_i.matchingDegreesI)
			g_i.maximumMatchE = max(g_i.matchingDegreesE)
		for i, g_i in enumerate(self.genes):
			# all the constant variables are calculated. rest can be calculated during the regulation process
			for j, g_j in enumerate(self.genes):
				g_i.enhImpacts.append(math.exp(self.beta * (g_i.matchingDegreesE[j] - g_i.maximumMatchE)))
				g_i.inhImpacts.append(math.exp(self.beta * (g_i.matchingDegreesI[j] - g_i.maximumMatchI)))
		self.reset()


	def setGenes(self, genes):
		self.genes = genes
	
	def findMatchingDegree(self, list1, list2):
		if len(list1) != len(list2):
			print("ARNF: Error! The size of the lists to compare is not the same! Exiting!")
			exit(1)
		matchingDegree = 0
		for index, elemen in enumerate(list1):
			if elemen != list2[index]:
				matchingDegree += 1
		return matchingDegree


	def regulate(self, iterations, output=False, log=False):
		self.normalize()
		for itter in range(iterations):
			for i, gene in enumerate(self.genes):
				# Save the old output values 
				# We don't want to regulate the input genes
				if gene.type == "I":
					continue	
				enh = 0.
				inh = 0.
				for j, g_j in enumerate(self.genes):
					# We don't want to regulate with the output genes
					if g_j.type == "O":
						continue
					enh += gene.enhImpacts[j] * g_j.concentration
					inh += gene.inhImpacts[j] * g_j.concentration
				enh /= len(self.genes)
				inh /= len(self.genes)
				# print("Gene: {} enh: {} inh: {} impact: {}".format(i, enh, inh, enh-inh))
				# update the concentrations
				impact = gene.concentration * self.delta * (enh - inh)
				# print("old: {} impact: {} new: {}".format(gene.concentration, impact, gene.concentration + impact))
				gene.concentration += impact
				#ToDo:: I hate this
				if gene.concentration < 0:
					gene.concentration = 0
			self.normalize()
			self.mapValues()
			# ToDo:: Probably need to change this format for logging and outputting for simplifying the network
			if output:
				print("Iteration {}".format(itter))
				for i, gene in enumerate(self.genes):
					print("Gene: {} Type: {} Concentration: {}".format(i, gene.type, gene.concentration))
			log = True
			if log: 
				if itter == 0:
					header = ['time']
					for i, gene in enumerate(self.genes):
						header.append("{}.{}".format(gene.type, i))
					LOG = L.Logger("Task", "regulation.csv", header, True)
					LOG2 = L.Logger("Task", "outputs.csv", header, True)
				data = "{},".format(itter)
				data2 = "{},".format(itter)
				for gene in self.genes:
					data += "{},".format(gene.concentration)
					try:
						data2 += "{},".format(gene.extra[0])
					except:
						raise Exception("can't find extra information about the gene")
				LOG.logln(data)
				LOG2.logln(data2)
				# ToDo:: To reduce the computational cost, maybe add this to the normalize function? Or even saving a list of outputs might help.
			

	def mapValues(self):
		rangeT = self.maxOut - self.minOut
		for gene in self.genes:
			try:
				gene.extra[0] = gene.concentration
			except:
				gene.extra.append(gene.concentration)
			# print("initial value: {}".format(gene.concentration))
			gene.extra[0] *= rangeT
			gene.extra[0] += self.minOut
			if self.intMode.upper() == "TRUE":
				gene.extra[0] = round(gene.extra[0], 0)
			# print("output value: {}".format(gene.concentration))

	def mapInput(self, value):
		if value > self.maxIn or value < self.minIn:
			raise Exception("ARN-R: value is out of the specified/calculated range in the config file.")
		rangeT = self.maxIn - self.minIn
		value = value + (-1 * self.minIn)
		value = value / rangeT
		value = value / len(self.genes)
		return value

	# We need to keep the total amount of concentrations the same. Sum of the concentrations should be 1 but we want to allow negative numbers as well. so, basically, we have two options. one is to not to care about the range of the values as long as the sum is one. the other is to keep everything in the -1 to 1 range without forcing the sign.   
	def normalize(self):
		#softmax
		tot = 0.
		for gene in self.genes:
			tot += math.exp(gene.concentration)
		for gene in self.genes: 
			gene.concentration = math.exp(gene.concentration) / tot
		pass

	def setInput(self, index, value):
		for i, gene in enumerate(self.genes):
			if gene.type == "I" and i == index:
				gene.concentration = self.mapInput(value)
				break

	#ToDo:: I don't think if I need to reset the concentrations anywhere else. specially in the genome.
	def reset(self):
		for gene in self.genes:
			gene.concentration = 1. / len(self.genes)

	def getOutput(self, index):
		# print("index: {}".format(index))
		counter = -1
		for i, gene in enumerate(self.genes):
			if gene.type == "O":
				counter += 1
				if counter == index:
					try:
						if self.intMode.upper() == "TRUE":
							return round(gene.extra[0], 0)
						else:
							return gene.extra[0]
					except:
						raise Exception("no extra information found in the gene")

	@staticmethod
	def gConfig():
		conf = {
			"beta" : 1,
			"delta" : 1,
			"minIn" : -1,
			"maxIn" : 1,
			"minOut" : -1,
			"maxOut" : 1,
			"intMode" : "False"
		}
		return conf
