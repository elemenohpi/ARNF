from abc import ABC, abstractmethod

class AbstractNetwork(ABC):
	
	# To automatically generate the config file for this class
	@abstractmethod
	def gConfig():
		pass

	@abstractmethod
	def build():
		pass

	@abstractmethod
	def regulate():
		pass

	@abstractmethod
	def setGenes():
		pass
	