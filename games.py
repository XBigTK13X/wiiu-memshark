import os
import json

class Games():
	def __init__(self, gamesPath):
		self.games = []
		self.game_lookup = {}		
		for root,dirs,files in os.walk(gamesPath):
			for file in files:
				gamePath = os.path.join(root,file)			
				game = Game(file, gamePath)
				self.games.append(game)
				self.game_lookup[game.name] = game

class Game():
	def __init__(self, gameFileName, gameFilePath):
		with open(gameFilePath) as json_file:    
			self.raw = json.load(json_file)
		self.slug = gameFileName.replace('.json','')
		self.name = self.raw['name']
		self.memory_pokes = []
		self.version = 'unknown'
		if 'version' in self.raw:
			self.version = self.raw['version']
		for poke in self.raw['memory_pokes']:
			self.memory_pokes.append(MemoryPoke(poke))

class MemoryPoke():
	def __init__(self, dataDict):
		self.raw = dataDict
		self.name = self.raw['name']
		self.address = int(self.raw['address'], 16)
		val = self.raw['value']
		if isinstance(val, int):
			self.value = val
			self.base = 10
		else:
			if '0x' in val:
				self.base = 16
				self.value = int(val, self.base)
			elif 'base' in self.raw:
				self.value = int(val, self.raw['base'])
				self.base = self.raw['base']
			else:
				self.base = 10
				self.value = int(val, self.base)
		self.pretty_address = self.raw['address']
		self.pretty_value = self.raw['value']
