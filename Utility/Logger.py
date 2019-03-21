import os

class Logger:
	def __init__(self, logType, filename, header, removeExisting=False):
		self.output = ""
		if logType == "Task":
			self.output = "./Output/Task/"
		self.output += filename
		self.header = header
		self.stream = None
		if os.path.isfile(self.output):
			if removeExisting:
				os.remove(self.output)
			self.stream = open(self.output, "a")
			for element in header:
				self.log(element+",")
			self.logln()
			self.stream.close()
		else:
			self.stream = open(self.output, "a")
			for element in header:
				self.log(element+",")
			self.logln()
			self.stream.close()

	def log(self, data):
		self.stream = open(self.output, "a")
		self.stream.write(data)
		self.stream.close()

	def logln(self, data=""):
		self.stream = open(self.output, "a")
		self.stream.write(data)
		self.stream.write("\n")
		self.stream.close()