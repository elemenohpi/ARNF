from Network.AbstractNetwork import AbstractNetwork
import numpy as np
import math
import configparser
import Utility.Logger as L
import Utility.Config as Config

# Modes: binaryIncremental, continuous. An concentration-alteration type of brain based on the original ARN

class ARNB(AbstractNetwork):
	def __init__(self):
		self.beta = Config.readFloat(self, "Network", "beta")
		self.delta = Config.readFloat(self, "Network", "delta")
		self.genes = None
		self.mode = Config.read(self, "Network", "mode")
		self.outputs = []

	def __init__(self, genes):
		self.beta = Config.readFloat(self, "Network", "beta")
		self.delta = Config.readFloat(self, "Network", "delta")
		self.mode = Config.read(self, "Network", "mode")
		self.genes = genes
		self.outputs = []
	
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
		self.outputs = []
		oldOutputs = []
		# ToDo:: Computational cost can be reduced if we save a list of inputs/outputs
		if self.mode == "binaryIncremental":
			for gene in self.genes:
				if gene.type == "O":
					oldOutputs.append(gene.concentration)
		elif self.mode == "continuous":
			pass
		else:
			print("ERROR! Mode does not exist!")
			exit(1)

		for itter in range(iterations):
			self.normalize()
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
				if gene.concentration < 0:
					gene.concentration = 0
			self.normalize()
			# ToDo:: Probably need to change this format for logging and outputting for simplifying the network
			if output:
				print("Iteration {}".format(itter))
				for i, gene in enumerate(self.genes):
					print("Gene: {} Type: {} Concentration: {}".format(i, gene.type, gene.concentration))
			if log: 
				if itter == 0:
					header = ['time']
					for i, gene in enumerate(self.genes):
						header.append("{}.{}".format(gene.type, i))
					LOG = L.Logger("Task", "regulation.csv", header, True)
				data = "{},".format(itter)
				for gene in self.genes:
					data += "{},".format(gene.concentration)
				LOG.logln(data)
					# ToDo:: To reduce the computational cost, maybe add this to the normalize function? Or even saving a list of outputs might help.
		if self.mode == "binaryIncremental":
			outputIndex = -1
			for gene in self.genes:
				if gene.type == "O":
					outputIndex += 1
					# ExpValue: The equal part for not changing is an experimental value. But this makes sense cause it's the same as rounding up maybe? I don't know this at this point.
					# if doesn't change or increases
					if gene.concentration >= oldOutputs[outputIndex]:
						self.outputs.append(1)
					else:
						# if becomes less
						self.outputs.append(0)
		else:
			print("ERROR! Mode not coded -.- :( Exiting!")
			exit(1)
			pass

	def normalize(self):
		tot = 0.
		for gene in self.genes:
			tot += gene.concentration
		for gene in self.genes: 
			gene.concentration /= tot
		pass
		#softmax
		# tot = 0.
		# for gene in self.genes:
		# 	tot += math.exp(gene.concentration)
		# for gene in self.genes: 
		# 	gene.concentration = math.exp(gene.concentration) / tot
		# pass

	def setInput(self, index, value):
		# ToDo:: This can be done in a way that reduces computational cost i.e. store the input genes and output genes seprately. The current state is highly order-based so it might cause problems. It defenitely causes complications at the moment
		inputIndex = -1
		for i, gene in enumerate(self.genes):
			if gene.type == "I":
				inputIndex += 1
				if inputIndex == index:
					# Check the mode and change the concentration accordingly
					# ExpValue: 2 is an experimental value here
					if self.mode == "binaryIncremental":
						if value == 1:
							gene.concentration += gene.concentration/2 
						elif value == 0:
							gene.concentration -= gene.concentration/2 
							if gene.concentration < 0:
								gene.concentration = 0
						else:
							# Invalid input value
							print("ARNF: Wrong input format with regards to the network mode! Exiting!")
							exit(1)
					elif self.mode == "proportional":
						print("ARNF: This is not coded yet. Exiting!")
						exit(1)
						pass
					else:
						print("ARNF: Unknown network mode. Exiting!")
						exit(1)
					return
		print("ARNF: Input index mismatch! Exiting!")
		exit(1)

	def reset(self):
		for gene in self.genes:
			gene.concentration = 1. / len(self.genes)

	def getOutput(self, index):
		# ToDo:: This can be done in a way that reduces computational cost i.e. store the input genes and output genes seprately. The current state is highly order-based so it might cause problems. It defenitely causes complications at the moment
		try:
			if self.mode == "binaryIncremental":
				return self.outputs[index]
		except:
			print("ARNF: Error in retrieving outputs. Possibly an index out of range error? Exiting anyway!")
			exit(1)
		pass

	@staticmethod
	def gConfig():
		conf = {
			"beta" : 1,
			"delta" : 1,
			"mode" : "binaryIncremental"
		}
		return conf
