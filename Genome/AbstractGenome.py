from abc import ABC, abstractmethod


class AbstractGenome(ABC):
	
	# To automatically generate the config file for this class
	@abstractmethod
	def gConfig():
		pass

	# Initializes the genome for the first time
	@abstractmethod
	def initialize():
		pass

	# Sets the fitness tied to the genome
	@abstractmethod
	def setFitness():
		pass

	# Gets the fitness associated with the genome
	@abstractmethod
	def getFitness():
		pass

	# In case we want to re-initalize just a portion of the genome and not all
	@abstractmethod
	def reinitialize():
		pass