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
		for poke in self.raw['memory_pokes']:
			self.memory_pokes.append(MemoryPoke(poke))

class MemoryPoke():
	def __init__(self, dataDict):
		self.raw = dataDict
		self.name = self.raw['name']
		self.address = self.raw['address']
		self.value = self.raw['value']