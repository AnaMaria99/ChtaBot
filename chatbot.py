from random import randint
from utils import FileReader, parsefloat

DOMENII = {'chimie', 'cultura-generala', 'geografie', 'istorie', 'matematica'}
DOMENIU_DE_BAZA = 'baza'

class Store:
	def __init__(self, data={}, index=0, domeniu=''):
		self.__data = data
		self.__index = index
		self.__domeniu = domeniu
		
	def get_domeniu(self):
		return self.__domeniu
		
	def adauga_intrebare(self, intrebare, raspuns, domeniu):
		if domeniu not in self.__data:
			self.__data[domeniu] = []
		self.__data[domeniu].append({
			'intrebare': intrebare,
			'raspuns': raspuns
		})
	
	def get_numar_intrebari(self, domeniu=None):
		if domeniu and domeniu in self.__data:
			return len(self.__data[domeniu])
		num = 0
		for i in self.__data.values():
			num += len(i)
		return num
		
	def alege_intrebare(self, domeniu=None):
		if domeniu and domeniu not in self.__data:
			return None
		if not domeniu:
			domeniu = self.__domeniu
		else:
			self.__domeniu = domeniu
		self.__index = randint(0, len(self.__data[domeniu])-1)
		return self.__data[domeniu][self.__index]
		
	def sterge_intrebarea_curenta(self):
		try:
			del self.__data[self.__domeniu][self.__index]
			return True
		except (KeyError, IndexError):
			return False


class Chat:
	def __init__(self):
		self.store = Store()
		
	def initializeaza_date(self):
		for d in list(DOMENII) + ['baza']:
			fr = FileReader(d + '.txt')
			date = fr.citire_date()
			for i in date:
				self.store.adauga_intrebare(i[0], i[1], d)
	
	def alege_domeniu(self):
		try:
			data = self.store.alege_intrebare('baza')
		except ValueError:
			return None
		self.store.sterge_intrebarea_curenta()
		DOMENII.remove(data['raspuns'])
		print(data['intrebare'])
		raspuns = input(">")
		if self.raspuns_pozitiv(raspuns):
			return data['raspuns']
		else:
			return self.alege_domeniu()
	
	def raspuns_pozitiv(self, raspuns):
		cuvinte_pozitive = ['bine', 'ador', 'iubesc', 'foarte priceput','da', 'destul', 'place', 'priceput']
		cuvinte_negative = ['rau', 'deloc', 'urasc', 'deloc priceput', 'nu foarte priceput', 'nu']
		for cuvant in cuvinte_pozitive:
			if cuvant in raspuns:
				return True
		for cuvant in cuvinte_negative:
			if cuvant in raspuns:
				return False
		return False
		
	def afiseaza_intrebare(self):
		domeniu = self.store.get_domeniu()
		if not domeniu or self.store.get_numar_intrebari(domeniu) is 0 or domeniu is DOMENIU_DE_BAZA:
			domeniu = self.alege_domeniu()
			if not domeniu:
				print("Acestea au fost toate domeniile")
				return
		if self.store.get_numar_intrebari():
			print()
			intrebare = self.store.alege_intrebare(domeniu)
			print(intrebare['intrebare'])
			self.intreaba(intrebare)
		else:
			print("Felicitari! Ati raspuns corect la toate intrebarile")
			
	def intreaba(self, intrebare):
		raspuns = input('> ')
		if raspuns.lower() == 'stop':
			print("Pa, m-am distrat")
			return
		if parsefloat(raspuns.split(' ')[0]):
			raspuns_int = parsefloat(raspuns.split(' ')[0])
			corect_int = parsefloat(intrebare['raspuns'].split(' ')[0])
			raspuns_corect = intrebare['raspuns'].split(' ')[1:]
			if self.evalueaza_num(raspuns_int, corect_int) == False or \
				self.evalueaza_str(raspuns.split('')[1:], raspuns_corect) == False:
					self.intreaba(intrebare)
		elif parsefloat(raspuns.split(' ')[-1]):
			raspuns_int = parsefloat(raspuns.split(' ')[-1])
			corect_int = parsefloat(intrebare['raspuns'].split(' ')[-1])
			raspuns_corect = intrebare['raspuns'].split(' ')[:-1]
			if self.evalueaza_num(raspuns_int, corect_int) == False or \
				self.evalueaza_str(raspuns.split(' ')[:-1], raspuns_corect) == False:
					self.intreaba(intrebare)
		else:
			if not self.evalueaza_str(raspuns.split(' '), intrebare['raspuns'].split(' '), True):
				self.intreaba(intrebare)
		print("Raspunsul este corect")
		self.store.sterge_intrebarea_curenta()
		self.afiseaza_intrebare()
	
	# D : Compara raspunsul de tip numar primit cu cel adevarat si da indicatii in dependnta de diferenta "\n"
	# de esantion dintre nr corect si ala gresit si de cuvantulintrodus
	# 
	def evalueaza_num(self, raspuns_int, corect_int):
		try:
			esantion = 10/100 * corect_int
		except TypeError:
			return False
		if raspuns_int == corect_int:
			return True
		else:
			if raspuns_int > corect_int:
				if raspuns_int - corect_int < esantion:
					print("Raspunsul tau este un pic prea mult")
				else:
					print("Raspunsul tau este mult prea mare")
			if raspuns_int < corect_int:
				if corect_int - raspuns_int < esantion:
					print("Varianta corecta este un pic mai mare")
				else:
					print("Raspunsul tau este mult prea mic")
			return False

	# D: Evalueaza raspunsul de tip string

	def evalueaza_str(self, raspuns, raspuns_corect, only_string=False):
		if ''.join(raspuns_corect).lower() == ''.join(raspuns).lower():
			return True
		else:
			if only_string:
				print("Mai incearca!")
			else:
				print("Partea numerica a raspunsului este buna! Cealalta incepe cu " +
					  raspuns_corect[0][0] + " si este formata din " +
					  str(len(raspuns_corect)) + " cuvinte. Mai incearca!")
			return False

if __name__ == "__main__":
	bot = Chat()
	bot.initializeaza_date()
	bot.afiseaza_intrebare()
