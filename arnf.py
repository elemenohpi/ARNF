import argparse
import configparser
import os
import core 
import random
import Utility.Plotter as PL

# Main function! Runs the program!
def main():
	print ("\n\n######################################################\n")
	print ("ARNF V1.0b \n")
	print ("######################################################\n")	

	print ("Parsing the arguements...\n")

	argParser = argparse.ArgumentParser(description="A tool to study Artificial Regulatory Networks.")
	argParser.add_argument('-gc', '--generateConfig',
		help="Generates the default config.ini file. Note: removes the existing file.", action="store_true")
	argParser.add_argument('-gus', '--generateUniqueSeq',
		help="Generates the default inputs.ini file. Note: removes the existing file.", action="store_true")
	argParser.add_argument('-sp', '--simplePlot',
		help="Plots the files on the output folder. Can have these values: Task, Evolution")
	args = argParser.parse_args()

	if args.generateConfig:
		generateConfig()
		print("ARNF: config.ini generated. Exiting!\n")
		exit(1)

	if args.generateUniqueSeq:
		generateUniqueSeq()
		print("ARNF: inputs.ini generated. Exiting!\n")
		exit(1)

	if args.simplePlot:
		Plotter = PL.Plotter()
		Plotter.simplePlot(args.simplePlot)
		print("ARNF: Plot generated. Exiting!\n")
		exit(1)	

	print ("Running the core...\n")

	if not os.path.isfile("config.ini"):
		print("ARNF: config.ini file does not exist! Exiting!\n")
		exit(1)

	configParser = configparser.ConfigParser()
	configParser.read("config.ini")
	random.seed(configParser['CORE']['seed'])
	coreObj = core.Core()
	coreObj.run()

# Core configuration. It's here cause we don't have a seperate directory for the application core for the sake of simplicity
def gConfig():
	conf = {
			"runs": "10",
			"task": "ClosedWorld",
			"genome" : "Linear",
			"seed" : 100,
			"network" : "ARNB",
			"evolver" : "EOne",
			"elitism" : True,
		}
	return conf

	
# Dynamically generates the config file
def generateConfig():
	dirList = ["Genome", "Task", "Evolver", "Network"]

	parser = configparser.ConfigParser()
	parser['CORE'] = gConfig()

	for eachDir in dirList:
		for subdirs, dirs, files in os.walk(eachDir):
			for file in files:
				name = file.split('.') 
				if name[1] == "py" and not (file[0:8] == "Abstract"):
					module = __import__(eachDir + "." + name[0])
					my_class = getattr(getattr(module, name[0]), name[0])
					parser[(eachDir + '.' +name[0]).upper()] = my_class.gConfig()

	with open('config.ini', 'w') as configfile:
		parser.write(configfile)
	pass

def generateUniqueSeq():
	parser = configparser.ConfigParser()
	results = {}
	for i in range(1000):
		string = ""
		for j in range(32):
			string += str(random.randint(0,1))
		results[i] = string
	temp = {}
	counter = 0
	for index, seq in results.items():
		found = 0
		for key, value in temp.items():
			if value == seq:
				found = 1
				break
		if found == 0:
			temp[counter] = seq
			counter += 1

	parser["INP"] = temp

	with open('inputs.ini', 'w') as configfile:
		parser.write(configfile)
	pass

main()