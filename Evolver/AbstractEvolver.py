from abc import ABC, abstractmethod

class AbstractEvolver(ABC):
	
	# To automatically generate the config file for this class
	@abstractmethod
	def gConfig():
		pass

	@abstractmethod
	def evolve():
		pass
	
	@abstractmethod
	def mutate():
		pass