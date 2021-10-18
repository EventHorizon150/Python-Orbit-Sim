# Nathaniel Morin
# 10/18/2021

import random

class Seed:
	# the ascii values of which characters can be included in a generated seed
	# 35 - 38, 48 - 57, 64 - 90, 97 - 122
	components = [35, 36, 37, 38]+list(range(48, 58))+list(range(64, 91))+list(range(97, 123))
	length = 6
	def __init__(self, seed=None):
		if seed is None or len(seed) < 1:
			seed = Seed.generateRandom()
		self.raw = seed
		self.seed = Seed.parse(seed)
	@ staticmethod
	def parse(seedString):
		numString = ""
		for i in range(len(seedString)):
			intVal = seedString[i] if seedString[i].isdigit() else str(ord(seedString[i]))
			numString += intVal
		return int(numString)
	@staticmethod
	def generateRandom():
		seedString = ""
		for i in range(Seed.length):
			seedString += chr(Seed.components[random.randint(0, len(Seed.components)-1)])
		return seedString
