# Programmable Artificial Regulatory Network 
# Author Iliya Miralavy, Michigan State University

from Network.AbstractNetwork import AbstractNetwork
import numpy as np
import math
import configparser
import Utility.Logger as L
import Utility.Config as Config

# Modes: binary

class PARN(AbstractNetwork):
	def __init__(self):
		self.beta = Config.readFloat(self, "Network", "beta")
		self.delta = Config.readFloat(self, "Network", "delta")
		self.mode = Config.read(self, "Network", "mode")
		self.genes = None
		self.outputs = []
		self.outputCount = 0

	def __init__(self, genes):
		self.beta = Config.readFloat(self, "Network", "beta")
		self.delta = Config.readFloat(self, "Network", "delta")
		self.mode = Config.read(self, "Network", "mode")
		self.genes = genes
		self.outputs = []
		self.outputCount = 0
	
	def build(self):
		# find u_max and u_i
		# print("ARNF: Building the Gene Regulatory Network...")
		self.outputCount = 0
		for g_i in self.genes:
			if g_i.type == "O":
				g_i.ID = self.outputCount
				self.outputCount += 1
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
		self.normalize()
		# The time loop
		for itter in range(iterations):
			for i, gene in enumerate(self.genes):
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
				enh /= (len(self.genes) - self.outputCount)
				inh /= (len(self.genes) - self.outputCount)
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

			# Regulation ends

	def normalize(self):
		tot = 0.
		for gene in self.genes:
			tot += gene.concentration
		if tot == 0:
			for gene in self.genes:
				# print(gene.concentration)
				self.reset()
				for gene in self.genes:
					tot += gene.concentration
			# raise Exception("the inevitable occured")

		for gene in self.genes: 
			gene.concentration /= tot
		pass
		# #softmax
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
					gene.concentration = value
					return
		raise Exception("Input index out of range")

	def reset(self):
		for gene in self.genes:
			gene.concentration = 1. / len(self.genes)

	def getOutput(self, index=-1):
		if self.mode == "binary":
			outputs = [-1, -1]
			for gene in self.genes:
				if gene.ID == 0 and gene.type == "O":
					outputs[0] = gene
				elif gene.ID == 1 and gene.type == "O":
					outputs[1] = gene
			if outputs[0] == None or outputs[1] == None:
				raise Exception("Could not find the output genes")
			if outputs[0].concentration > outputs[1].concentration:
				return 0
			else: 
				return 1
		elif self.mode == "index":
			outputGenes = []
			for gene in self.genes:
				if gene.type == "O":
					outputGenes.append(gene)
			# print(" {} {} {} ".format(outputGenes[0].concentration,outputGenes[1].concentration,outputGenes[2].concentration))
			maxGene = outputGenes[0]
			for gene in outputGenes:
				if maxGene.concentration < gene.concentration:
					maxGene = gene
			return maxGene.ID


		else:
			raise Exception("Unknown mode")



	@staticmethod
	def gConfig():
		conf = {
			"beta" : 1,
			"delta" : 1,
			"mode" : "binary"
		}
		return conf
