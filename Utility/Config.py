import configparser

configParser = configparser.ConfigParser()
configParser.read("config.ini")

def read(obj, section, item):
	return configParser[(section+"."+type(obj).__name__).upper()][item]

def readInt(obj, section, item):
	return int(configParser[(section+"."+type(obj).__name__).upper()][item])

def readFloat(obj, section, item):
	return float(configParser[(section+"."+type(obj).__name__).upper()][item])

def readBool(obj, section, item):
	if configParser[(section+"."+type(obj).__name__).upper()][item].upper() == "TRUE":
		return True
	else: 
		return False