class FileReader:
	def __init__(self, filename):
		self.__filename = filename
		
	def citire_date(self):
		date = []
		with open(self.__filename) as f:
			for intrebare in f:
				raspuns = f.readline().strip('\n')
				date.append((intrebare, raspuns))
		return date
		
def parsefloat(string):
	try:
		return float(''.join([x for x in string if x.isdigit() or x == '.']).strip('.'))
	except:
		return None
