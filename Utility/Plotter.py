import matplotlib.pyplot as plt
import pandas as pd

class Plotter:
	def __init__(self):
		pass

	def simplePlot(self, dataType):
		if (dataType).upper() == "TASK":
			file = "./Output/Task/regulation.csv"
			data = pd.read_csv(file)
			# data = dataframe.values
			x = data['time'].tolist()

			for i in range(1, len(data.columns)-2):	
				plt.plot(x, data[data.columns[i]], label=data.columns[i])

			plt.xlabel('Time')
			plt.ylabel('Concentrations')

			plt.title("Regulations")

			plt.legend()

			plt.show()
		elif (dataType).upper() == "EVOLUTION":
			#ToDo:: self-explanatory
			pass
		elif (dataType).upper() == "OUTPUT":
			file = "./Output/Task/outputs.csv"
			data = pd.read_csv(file)
			# data = dataframe.values
			x = data['time'].tolist()

			for i in range(1, len(data.columns)-2):	
				plt.plot(x, data[data.columns[i]], label=data.columns[i])

			plt.xlabel('Time')
			plt.ylabel('Values')

			plt.title("Regulations")

			plt.legend()

			plt.show()
		else:
			print("ARNF: Unknown simple plot! Exiting!")
			exit(1)
		pass