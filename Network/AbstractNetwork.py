from abc import ABC, abstractmethod

class AbstractNetwork(ABC):
	
	# To automatically generate the config file for this class
	@abstractmethod
	def gConfig():
		pass

	