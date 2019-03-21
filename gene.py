class Gene:
	def __init__(self, promoter, enhancer, inhibitor, protein, geneType, concentration=0.):
		self.promoter = promoter
		self.enhancer = enhancer
		self.inhibitor = inhibitor
		self.protein = protein
		self.concentration = concentration
		self.matchingDegreesE = []
		self.matchingDegreesI = []
		self.maximumMatchE = 0
		self.maximumMatchI = 0
		self.enhImpacts = []
		self.inhImpacts = []
		self.type = geneType
	
	def print(self):
		print("\nPromoter: {}\nEnhancer: {}\nInhibitor: {}\nProtein: {}\nConcentration: {}\nType: {}\n".format(self.promoter, self.enhancer, self.inhibitor, self.protein, self.concentration, self.type))