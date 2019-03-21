from abc import ABC, abstractmethod

class AbstractTask(ABC):

	# To automatically generate the config file for this class
	@abstractmethod
	def gConfig():
		pass

	# This helps the core to figure out how many inputs and outputs the task needs
	@abstractmethod
	def requirements():
		pass

	@abstractmethod
	def setGRN():
		pass

	@abstractmethod
	def start():
		pass